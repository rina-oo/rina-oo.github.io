#!/usr/bin/env python3
"""리뷰 한 편을 지식 레이어(vault/)에 편입시킨다.

만드는 것 세 가지:
  1. vault/papers/<arxiv_id>.md   — Research OS 호환 논문 노트 (골격 생성,
     TL;DR·핵심 기여·한계는 리뷰 front matter/본문에서 초안 추출.
     예약 에이전트는 생성 후 내용을 다듬어 채운다)
  2. 인용 엣지                     — Semantic Scholar로 인용/피인용을 조회해
     vault 안에 이미 있는 논문과의 교집합만 cites/cited_by frontmatter와
     '## 연결' 섹션에 양방향 기록
  3. vault/topics/review-<tag>.md — 태그별 허브 노트에 한 줄 항목 추가

사용법:
    python3 scripts/build_knowledge.py <arxiv_id>
    python3 scripts/build_knowledge.py --retry-pending   # 실패했던 인용 조회 재시도

Semantic Scholar가 실패해도(레이트리밋 잦음) 노트·허브는 만들어지고,
인용 조회만 data/citations/pending.json에 적혀 다음 실행 때 재시도된다.
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "_posts"
PAPERS_DIR = ROOT / "vault" / "papers"
TOPICS_DIR = ROOT / "vault" / "topics"
CITATIONS_DIR = ROOT / "data" / "citations"
PENDING_FILE = CITATIONS_DIR / "pending.json"

S2_API = "https://api.semanticscholar.org/graph/v1/paper/arXiv:{id}"
S2_FIELDS = "title,year,authors,externalIds"
S2_EDGE_FIELDS = "references.externalIds,citations.externalIds"
KST = timezone(timedelta(hours=9))

FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# 리뷰 태그 → Research OS fields 어휘 매핑 (그 외 태그는 tags로만 유지)
FIELD_MAP = {
    "llm": "NLP", "nlp": "NLP", "moe": "Efficiency", "efficiency": "Efficiency",
    "vision": "CV", "multimodal": "Multimodal", "diffusion": "Generative",
    "rl": "RL", "agent": "Agents", "robotics": "Robotics",
    "long-context": "Efficiency",
}


def parse_front_matter(text: str) -> dict:
    import yaml

    m = FM_RE.match(text)
    return yaml.safe_load(m.group(1)) if m else {}


def find_review(arxiv_id: str) -> Path | None:
    hits = sorted(POSTS_DIR.glob(f"*-{arxiv_id}.md"))
    return hits[-1] if hits else None


def s2_get(url: str, retries: int = 3) -> dict | None:
    for i in range(retries):
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429:  # 레이트리밋 — 잠깐 쉬고 재시도
                time.sleep(5 * (i + 1))
                continue
            return None
        except requests.RequestException:
            time.sleep(3)
    return None


def fetch_citation_data(arxiv_id: str) -> dict | None:
    """메타데이터 + 인용/피인용 arXiv ID 목록. 캐시 우선."""
    CITATIONS_DIR.mkdir(parents=True, exist_ok=True)
    cache = CITATIONS_DIR / f"{arxiv_id}.json"
    if cache.is_file():
        return json.loads(cache.read_text(encoding="utf-8"))

    meta = s2_get(S2_API.format(id=arxiv_id) + f"?fields={S2_FIELDS}")
    edges = s2_get(S2_API.format(id=arxiv_id) + f"?fields={S2_EDGE_FIELDS}")
    if meta is None:
        return None

    def arxiv_ids(items):
        out = []
        for it in items or []:
            ext = (it or {}).get("externalIds") or {}
            if ext.get("ArXiv"):
                out.append(ext["ArXiv"])
        return sorted(set(out))

    all_authors = [a["name"] for a in meta.get("authors") or []]
    # 대규모 팀 논문은 저자가 수백 명 — 노트에는 8명 + '외 N명'만
    if len(all_authors) > 8:
        all_authors = all_authors[:8] + [f"외 {len(all_authors) - 8}명"]
    data = {
        "arxiv_id": arxiv_id,
        "title": meta.get("title"),
        "year": meta.get("year"),
        "authors": all_authors,
        "references": arxiv_ids((edges or {}).get("references")),
        "citations": arxiv_ids((edges or {}).get("citations")),
        "fetched": datetime.now(KST).isoformat(),
    }
    cache.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                     encoding="utf-8")
    return data


def vault_ids() -> set[str]:
    return {p.stem for p in PAPERS_DIR.glob("*.md")}


# --------------------------------------------------------------------------
# frontmatter 배열 필드 갱신 (cites / cited_by)
# --------------------------------------------------------------------------

def update_fm_list(path: Path, key: str, add: list[str]) -> None:
    import yaml

    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        return
    fm = yaml.safe_load(m.group(1)) or {}
    merged = sorted(set(fm.get(key) or []) | set(add))
    if merged == (fm.get(key) or []):
        return
    fm[key] = merged
    new_fm = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).strip()
    path.write_text(f"---\n{new_fm}\n---\n{text[m.end():]}", encoding="utf-8")


def append_connection(path: Path, line: str) -> None:
    """'## 연결' 섹션에 중복 없이 한 줄 추가."""
    text = path.read_text(encoding="utf-8")
    if line in text:
        return
    if "\n## 연결\n" in text:
        head, _, tail = text.partition("\n## 연결\n")
        # 섹션 끝(다음 ## 또는 EOF) 직전에 삽입
        nm = re.search(r"\n## ", tail)
        if nm:
            tail = tail[:nm.start()] + line + "\n" + tail[nm.start():]
        else:
            tail = tail.rstrip("\n") + "\n" + line + "\n"
        text = head + "\n## 연결\n" + tail
    else:
        text = text.rstrip("\n") + f"\n\n## 연결\n{line}\n"
    path.write_text(text, encoding="utf-8")


# --------------------------------------------------------------------------
# 1) 논문 노트 골격
# --------------------------------------------------------------------------

def build_note(arxiv_id: str, review: Path, s2: dict | None) -> Path:
    import yaml

    review_text = review.read_text(encoding="utf-8")
    fm = parse_front_matter(review_text)
    tags = [str(t).lower() for t in fm.get("tags") or []]
    fields = sorted({FIELD_MAP[t] for t in tags if t in FIELD_MAP})
    title_ko = str(fm.get("title") or "").split("—")[0].strip()
    title = (s2 or {}).get("title") or str(fm.get("title") or arxiv_id)
    date_str = str(fm.get("date") or "")[:10] or datetime.now(KST).strftime("%Y-%m-%d")

    note_path = PAPERS_DIR / f"{arxiv_id}.md"
    if note_path.is_file():
        return note_path  # 골격은 한 번만 — 내용은 에이전트/사람이 관리

    front = {
        "title": title,
        "title_ko": title_ko or title,
        "type": "paper",
        "source_url": f"https://arxiv.org/abs/{arxiv_id}",
        "arxiv_id": arxiv_id,
        "authors": (s2 or {}).get("authors") or [],
        "year": (s2 or {}).get("year") or int(date_str[:4]),
        "fields": fields,
        "tags": tags,
        "added": date_str,
        "read_status": "read",
        "review_url": f"https://rina-oo.github.io/posts/{arxiv_id}/",
        "cites": [],
        "cited_by": [],
    }
    tldr = str(fm.get("description") or "").strip()
    body = f"""# {title}

> 원제: {title}
> 리뷰: [블로그 전문](https://rina-oo.github.io/posts/{arxiv_id}/)

## TL;DR
{tldr or '(작성 필요)'}

## 핵심 기여
(리뷰의 핵심 기여를 3~5개 불릿으로)

## 한계
(리뷰의 한계 섹션 요약)

## 연결
"""
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    fm_str = yaml.safe_dump(front, allow_unicode=True, sort_keys=False).strip()
    note_path.write_text(f"---\n{fm_str}\n---\n{body}", encoding="utf-8")
    return note_path


# --------------------------------------------------------------------------
# 2) 인용 엣지
# --------------------------------------------------------------------------

def link_citations(arxiv_id: str, s2: dict) -> int:
    """vault 안 논문과의 인용 교집합을 양방향 기록. → 엣지 수."""
    existing = vault_ids() - {arxiv_id}
    me = PAPERS_DIR / f"{arxiv_id}.md"
    edges = 0
    for other in sorted(set(s2.get("references") or []) & existing):
        update_fm_list(me, "cites", [other])
        update_fm_list(PAPERS_DIR / f"{other}.md", "cited_by", [arxiv_id])
        append_connection(me, f"- 인용함 → [[{other}]]")
        append_connection(PAPERS_DIR / f"{other}.md", f"- 인용됨 ← [[{arxiv_id}]]")
        edges += 1
    for other in sorted(set(s2.get("citations") or []) & existing):
        update_fm_list(me, "cited_by", [other])
        update_fm_list(PAPERS_DIR / f"{other}.md", "cites", [arxiv_id])
        append_connection(me, f"- 인용됨 ← [[{other}]]")
        append_connection(PAPERS_DIR / f"{other}.md", f"- 인용함 → [[{arxiv_id}]]")
        edges += 1
    return edges


def mark_pending(arxiv_id: str) -> None:
    CITATIONS_DIR.mkdir(parents=True, exist_ok=True)
    pending = json.loads(PENDING_FILE.read_text()) if PENDING_FILE.is_file() else []
    if arxiv_id not in pending:
        pending.append(arxiv_id)
    PENDING_FILE.write_text(json.dumps(pending), encoding="utf-8")


def enrich_note_meta(arxiv_id: str, s2: dict) -> None:
    """S2 데이터가 늦게 도착한 경우 노트 frontmatter의 빈 메타데이터를 채운다."""
    import yaml

    path = PAPERS_DIR / f"{arxiv_id}.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        return
    fm = yaml.safe_load(m.group(1)) or {}
    changed = False
    if not fm.get("authors") and s2.get("authors"):
        fm["authors"] = s2["authors"]
        changed = True
    if s2.get("year") and fm.get("year") != s2["year"]:
        fm["year"] = s2["year"]
        changed = True
    if changed:
        new_fm = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).strip()
        path.write_text(f"---\n{new_fm}\n---\n{text[m.end():]}", encoding="utf-8")


def retry_pending() -> None:
    if not PENDING_FILE.is_file():
        print("재시도할 인용 조회 없음")
        return
    pending = json.loads(PENDING_FILE.read_text())
    still = []
    for pid in pending:
        s2 = fetch_citation_data(pid)
        if s2 is None:
            still.append(pid)
            continue
        enrich_note_meta(pid, s2)
        n = link_citations(pid, s2)
        print(f"{pid}: 인용 엣지 {n}개")
    PENDING_FILE.write_text(json.dumps(still), encoding="utf-8")


# --------------------------------------------------------------------------
# 3) 토픽 허브
# --------------------------------------------------------------------------

def update_topic_hubs(arxiv_id: str, review: Path) -> list[str]:
    fm = parse_front_matter(review.read_text(encoding="utf-8"))
    tags = [str(t).lower() for t in fm.get("tags") or []]
    one_liner = str(fm.get("description") or "").strip()
    title_ko = str(fm.get("title") or arxiv_id).split("—")[0].strip()
    date_str = str(fm.get("date") or "")[:10]
    TOPICS_DIR.mkdir(parents=True, exist_ok=True)

    touched = []
    entry = f"- {date_str} [[{arxiv_id}|{title_ko}]] — {one_liner}"
    for tag in tags:
        hub = TOPICS_DIR / f"review-{tag}.md"
        if not hub.is_file():
            hub.write_text(
                f"""---
title: '리뷰 허브: {tag}'
type: topic
topic: {tag}
tags:
- {tag}
added: '{date_str}'
---
# 리뷰 허브: {tag}

일일 논문 리뷰 중 `{tag}` 태그가 붙은 논문들.

""",
                encoding="utf-8",
            )
        text = hub.read_text(encoding="utf-8")
        if f"[[{arxiv_id}|" not in text and f"[[{arxiv_id}]]" not in text:
            hub.write_text(text.rstrip("\n") + "\n" + entry + "\n",
                           encoding="utf-8")
            touched.append(hub.name)
    return touched


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("arxiv_id", nargs="?")
    ap.add_argument("--retry-pending", action="store_true")
    args = ap.parse_args()

    if args.retry_pending:
        retry_pending()
        return
    if not args.arxiv_id:
        ap.error("arxiv_id가 필요합니다")

    review = find_review(args.arxiv_id)
    if review is None:
        sys.exit(f"_posts/에서 {args.arxiv_id} 리뷰를 찾지 못했습니다")

    s2 = fetch_citation_data(args.arxiv_id)
    note = build_note(args.arxiv_id, review, s2)
    print(f"노트: {note.relative_to(ROOT)}")

    if s2 is None:
        mark_pending(args.arxiv_id)
        print("Semantic Scholar 실패 — pending에 기록, 다음 실행 때 재시도")
    else:
        n = link_citations(args.arxiv_id, s2)
        print(f"인용 엣지: {n}개 (vault 내부 교집합 기준)")

    hubs = update_topic_hubs(args.arxiv_id, review)
    print(f"토픽 허브: {', '.join(hubs) if hubs else '변경 없음'}")


if __name__ == "__main__":
    main()
