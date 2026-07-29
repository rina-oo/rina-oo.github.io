#!/usr/bin/env python3
"""논문 원문을 가장 충실한 형식으로 가져온다.

3단계 폴백 전략(위쪽이 더 정확):

  Tier 1  arXiv LaTeX 원본 (`/e-print/`)
          → 수식은 원본 LaTeX 그대로, 표는 \\textbf/\\uline 마커까지 보존,
            그림은 저자가 넣은 원본 벡터 파일. 손실이 전혀 없다.
  Tier 2  arXiv HTML (LaTeXML 변환, `/html/<id>v1`)
          → MathML에 원본 TeX가 annotation으로 붙어 있다.
  Tier 3  PDF 텍스트 추출 + 페이지 이미지 렌더링
          → 수식이 깨지므로 최후 수단. 대신 페이지를 이미지로도 뽑아
            사람(혹은 비전 모델)이 눈으로 확인할 수 있게 한다.

산출물(<workdir>):
    manifest.json   어떤 tier를 썼는지, figure/table 목록
    source/         Tier 1일 때 LaTeX 원본 트리
    body.tex|.html|.txt   본문 텍스트
    figures/*.png   렌더링된 그림 (캡션은 manifest에)
    pages/*.png     Tier 3일 때 페이지 이미지

사용법:
    python scripts/fetch_paper.py 2607.24653 --out /tmp/paper
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

import requests

UA = {"User-Agent": "paper-review-bot/1.0 (+https://rina-oo.github.io)"}
TIMEOUT = 90


# --------------------------------------------------------------------------
# Tier 1: LaTeX 원본
# --------------------------------------------------------------------------

def try_latex_source(arxiv_id: str, work: Path) -> bool:
    """arXiv e-print에서 LaTeX 원본 tarball을 받아 푼다."""
    url = f"https://arxiv.org/e-print/{arxiv_id}"
    try:
        r = requests.get(url, headers=UA, timeout=TIMEOUT)
        r.raise_for_status()
    except Exception as e:
        print(f"[tier1] e-print 실패: {e}", file=sys.stderr)
        return False

    blob = work / "eprint.tar.gz"
    blob.write_bytes(r.content)
    src = work / "source"
    src.mkdir(exist_ok=True)
    try:
        with tarfile.open(blob) as tf:
            tf.extractall(src, filter="data")
    except Exception as e:
        # 단일 .tex 파일을 gzip만 한 경우가 있다
        print(f"[tier1] tar 아님, 단일 파일로 시도: {e}", file=sys.stderr)
        try:
            import gzip
            (src / "main.tex").write_bytes(gzip.decompress(blob.read_bytes()))
        except Exception:
            return False

    if not list(src.rglob("*.tex")):
        print("[tier1] .tex 없음", file=sys.stderr)
        return False
    return True


def find_main_tex(src: Path) -> Path | None:
    """\\documentclass가 있는 루트 tex 파일을 찾는다."""
    candidates = list(src.rglob("*.tex"))
    for f in candidates:
        try:
            if "\\documentclass" in f.read_text(errors="ignore"):
                return f
        except Exception:
            continue
    return candidates[0] if candidates else None


def inline_inputs(tex_path: Path, src: Path, depth: int = 0) -> str:
    r"""\input{}/\include{}를 재귀적으로 펼쳐 본문 전체를 하나로 만든다."""
    if depth > 6:
        return ""
    try:
        text = tex_path.read_text(errors="ignore")
    except Exception:
        return ""

    def repl(m):
        name = m.group(1).strip()
        for cand in (src / name, src / f"{name}.tex", tex_path.parent / f"{name}.tex"):
            if cand.is_file():
                return inline_inputs(cand, src, depth + 1)
        return m.group(0)

    return re.sub(r"\\(?:input|include)\{([^}]+)\}", repl, text)


def parse_floats(body: str, macros: dict | None = None):
    """figure/table 환경을 뜯어 캡션·라벨·그래픽 경로를 뽑는다."""
    figures, tables = [], []
    for env, bucket in (("figure", figures), ("table", tables)):
        pattern = re.compile(
            r"\\begin\{" + env + r"\*?\}(.*?)\\end\{" + env + r"\*?\}", re.S
        )
        for i, m in enumerate(pattern.finditer(body), 1):
            block = m.group(1)
            cap = re.search(r"\\caption\{", block)
            caption = _balanced(block, cap.end() - 1) if cap else ""
            label = re.search(r"\\label\{([^}]+)\}", block)
            item = {
                "index": i,
                "label": label.group(1) if label else None,
                "caption": _clean_tex(caption, macros),
            }
            if env == "figure":
                item["graphics"] = re.findall(
                    r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", block
                )
            else:
                item["latex"] = block.strip()
            bucket.append(item)
    return figures, tables


def _balanced(s: str, open_idx: int) -> str:
    """`{`부터 짝이 맞는 `}`까지 잘라낸다 (중첩 대응)."""
    depth = 0
    for i in range(open_idx, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return s[open_idx + 1:i]
    return s[open_idx + 1:]


def _clean_tex(s: str, macros: dict | None = None) -> str:
    if macros:
        s = expand_macros(s, macros)
    s = re.sub(r"\\label\{[^}]*\}", "", s)
    s = re.sub(r"\\(?:textbf|textit|emph|uline|texttt)\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\protect\b", "", s)
    s = re.sub(r"~", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def collect_macros(body: str) -> dict:
    r"""\newcommand{\foo}[n]{body} 를 수집한다 (캡션에 자주 쓰이므로)."""
    macros = {}
    for m in re.finditer(r"\\(?:new|renew)command\{\\(\w+)\}(?:\[(\d+)\])?\{", body):
        name, argc = m.group(1), int(m.group(2) or 0)
        macros[name] = (argc, _balanced(body, m.end() - 1))
    return macros


def expand_macros(s: str, macros: dict, rounds: int = 3) -> str:
    """캡션 안의 사용자 정의 매크로를 펼친다 (\\kimi{3} → Kimi K3)."""
    for _ in range(rounds):
        changed = False
        for name, (argc, tmpl) in macros.items():
            pattern = re.compile(r"\\" + name + r"\b" + (r"\{([^}]*)\}" * argc))
            if not pattern.search(s):
                continue
            def sub(m, tmpl=tmpl, argc=argc):
                out = tmpl
                for i in range(argc):
                    out = out.replace(f"#{i + 1}", m.group(i + 1))
                return out
            s, n = pattern.subn(sub, s)
            changed = changed or bool(n)
        if not changed:
            break
    return s


def render_figures(src: Path, figures: list, out: Path) -> None:
    """저자 원본 그래픽 파일을 PNG로 렌더링한다 (벡터 PDF → 고해상도 래스터)."""
    import fitz

    out.mkdir(parents=True, exist_ok=True)
    for fig in figures:
        saved = []
        for g in fig.get("graphics", []):
            path = _resolve_graphic(src, g)
            if path is None:
                continue
            dest = out / f"fig{fig['index']}_{path.stem}.png"
            try:
                if path.suffix.lower() == ".pdf":
                    doc = fitz.open(path)
                    doc[0].get_pixmap(matrix=fitz.Matrix(3, 3)).save(dest)
                    doc.close()
                else:
                    shutil.copy(path, dest.with_suffix(path.suffix))
                    dest = dest.with_suffix(path.suffix)
                saved.append(str(dest))
            except Exception as e:
                print(f"[figure] {g} 렌더 실패: {e}", file=sys.stderr)
        fig["rendered"] = saved


def capture_missing_from_pdf(arxiv_id: str, figures: list, work: Path) -> None:
    """외부 그래픽 파일이 없는 그림(TikZ/pgfplots로 그린 것)은
    발행된 PDF에서 해당 Figure 영역을 캡처한다."""
    missing = [f for f in figures if not f.get("rendered")]
    if not missing:
        return

    pdf = work / "paper.pdf"
    if not pdf.is_file():
        try:
            r = requests.get(
                f"https://arxiv.org/pdf/{arxiv_id}", headers=UA, timeout=TIMEOUT
            )
            r.raise_for_status()
            pdf.write_bytes(r.content)
        except Exception as e:
            print(f"[figure] PDF 폴백 실패: {e}", file=sys.stderr)
            return

    script = Path(__file__).parent / "extract_figures.py"
    nums = [str(f["index"]) for f in missing]
    out = work / "figures"
    try:
        subprocess.run(
            [sys.executable, str(script), str(pdf), str(out), *nums],
            check=True, capture_output=True, timeout=300,
        )
    except Exception as e:
        print(f"[figure] 캡처 실패: {e}", file=sys.stderr)
        return

    for f in missing:
        cand = out / f"figure{f['index']}.png"
        if cand.is_file():
            f["rendered"] = [str(cand)]
            f["source"] = "pdf-capture"


def _resolve_graphic(src: Path, ref: str) -> Path | None:
    ref = ref.strip()
    for ext in ("", ".pdf", ".png", ".jpg", ".jpeg", ".eps"):
        cand = src / (ref + ext)
        if cand.is_file():
            return cand
    stem = Path(ref).name
    for cand in src.rglob(f"{stem}.*"):
        if cand.suffix.lower() in (".pdf", ".png", ".jpg", ".jpeg", ".eps"):
            return cand
    return None


# --------------------------------------------------------------------------
# Tier 2 / 3
# --------------------------------------------------------------------------

def try_html(arxiv_id: str, work: Path) -> bool:
    for url in (
        f"https://arxiv.org/html/{arxiv_id}v1",
        f"https://arxiv.org/html/{arxiv_id}",
    ):
        try:
            r = requests.get(url, headers=UA, timeout=TIMEOUT)
            if r.status_code == 200 and "<math" in r.text:
                (work / "body.html").write_text(r.text, encoding="utf-8")
                return True
        except Exception:
            continue
    return False


def try_pdf(arxiv_id: str, work: Path) -> bool:
    """PDF 텍스트 + 페이지 이미지. 수식이 깨지므로 이미지가 중요하다."""
    try:
        r = requests.get(
            f"https://arxiv.org/pdf/{arxiv_id}", headers=UA, timeout=TIMEOUT
        )
        r.raise_for_status()
    except Exception as e:
        print(f"[tier3] PDF 실패: {e}", file=sys.stderr)
        return False

    pdf = work / "paper.pdf"
    pdf.write_bytes(r.content)
    try:
        import fitz

        doc = fitz.open(pdf)
        (work / "body.txt").write_text(
            "\n".join(p.get_text() for p in doc), encoding="utf-8"
        )
        pages = work / "pages"
        pages.mkdir(exist_ok=True)
        for i, page in enumerate(doc, 1):
            page.get_pixmap(matrix=fitz.Matrix(2, 2)).save(pages / f"p{i:03d}.png")
        doc.close()
    except Exception as e:
        print(f"[tier3] 렌더 실패: {e}", file=sys.stderr)
        return False
    return True


# --------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("arxiv_id")
    ap.add_argument("--out", default="/tmp/paper", help="작업 디렉토리")
    args = ap.parse_args()

    work = Path(args.out)
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    manifest = {"arxiv_id": args.arxiv_id, "tier": None, "figures": [], "tables": []}

    if try_latex_source(args.arxiv_id, work):
        src = work / "source"
        main_tex = find_main_tex(src)
        body = inline_inputs(main_tex, src) if main_tex else ""
        (work / "body.tex").write_text(body, encoding="utf-8")
        macros = collect_macros(body)
        figures, tables = parse_floats(body, macros)
        render_figures(src, figures, work / "figures")
        capture_missing_from_pdf(args.arxiv_id, figures, work)
        manifest.update(tier="latex-source", figures=figures, tables=tables,
                        body="body.tex", main_tex=str(main_tex))
    elif try_html(args.arxiv_id, work):
        manifest.update(tier="arxiv-html", body="body.html")
    elif try_pdf(args.arxiv_id, work):
        manifest.update(tier="pdf-fallback", body="body.txt", pages="pages/")
    else:
        raise SystemExit("원문을 가져오지 못했습니다.")

    (work / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"tier      : {manifest['tier']}")
    print(f"작업 경로 : {work}")
    print(f"figures   : {len(manifest['figures'])}개")
    print(f"tables    : {len(manifest['tables'])}개")
    for f in manifest["figures"][:12]:
        n = len(f.get("rendered", []))
        print(f"  fig{f['index']:>2} [{n}장] {f['caption'][:70]}")
    for t in manifest["tables"][:12]:
        print(f"  tab{t['index']:>2} {t['caption'][:70]}")


if __name__ == "__main__":
    main()
