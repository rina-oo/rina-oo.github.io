#!/usr/bin/env python3
"""주간 종합(vault/syntheses/)을 블로그 포스트(_posts/)로 내보낸다.

vault 노트가 단일 원본이고 이 스크립트는 기계적 변환만 한다:

  - 위키링크 ``[[<arxiv_id>|이름]]`` → ``[이름](/posts/<arxiv_id>/)``
  - 발행일 = 해당 ISO 주차의 일요일 21:00 KST
    (그날의 논문 리뷰가 보통 09시대라, 종합이 목록에서 위에 오도록 저녁으로 둔다)
  - 태그 = 참조된 논문 글들의 태그 중 빈도 상위 5개 + weekly-synthesis
  - 제목/설명 = vault 노트 front matter의 headline / summary

사용법:
    python3 scripts/publish_synthesis.py 2026-W41   # 한 주
    python3 scripts/publish_synthesis.py --all      # 전부 (이미 있으면 건너뜀)
    python3 scripts/publish_synthesis.py --all --force
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYNTH_DIR = ROOT / "vault" / "syntheses"
POSTS_DIR = ROOT / "_posts"

WIKILINK = re.compile(r"\[\[([0-9]{4}\.[0-9]+)\|([^\]]+)\]\]")
SOCIAL_IMG = "/assets/img/social-preview.png"
MAX_TAGS = 5


def parse_front_matter(text: str) -> tuple[dict, str]:
    """``---`` 로 감싼 front matter를 얕게 파싱한다 (key: value 한 줄짜리만)."""
    if not text.startswith("---"):
        raise ValueError("front matter가 없다")
    _, fm, body = text.split("---", 2)
    data: dict[str, str] = {}
    for line in fm.splitlines():
        m = re.match(r"\s*([A-Za-z_]+):\s*(.*)$", line)
        if not m:
            continue
        val = m.group(2).strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        data[m.group(1)] = val
    return data, body


def post_tags(arxiv_id: str) -> list[str]:
    """해당 논문 블로그 글의 태그 목록."""
    for p in POSTS_DIR.glob(f"*-{arxiv_id}.md"):
        fm, _ = parse_front_matter(p.read_text(encoding="utf-8"))
        raw = fm.get("tags", "")
        return [t.strip() for t in raw.strip("[]").split(",") if t.strip()]
    return []


def sunday_of(week: str) -> datetime.date:
    year, num = week.split("-W")
    return datetime.date.fromisocalendar(int(year), int(num), 7)


def yaml_quote(s: str) -> str:
    """YAML 큰따옴표 스칼라. 제목에 따옴표가 섞여도 안전하다.

    front matter가 깨지면 Jekyll이 제목과 permalink를 통째로 잃는다
    (REVIEW_GUIDE §5 참고). 그래서 항상 감싼다.
    """
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def convert(week: str, force: bool = False) -> Path | None:
    src = SYNTH_DIR / f"{week}.md"
    if not src.exists():
        sys.exit(f"없는 주차: {src}")

    fm, body = parse_front_matter(src.read_text(encoding="utf-8"))
    headline, summary = fm.get("headline"), fm.get("summary")
    if not headline or not summary:
        sys.exit(
            f"{week}: vault 노트에 headline / summary 가 없다. "
            "REVIEW_GUIDE §7-2 형식으로 추가할 것."
        )

    ids = list(dict.fromkeys(WIKILINK.findall(body)))  # [(id, label), ...] 순서 유지
    if not ids:
        sys.exit(f"{week}: 위키링크가 하나도 없다 — 종합 노트 형식을 확인할 것")

    missing = [i for i, _ in ids if not list(POSTS_DIR.glob(f"*-{i}.md"))]
    if missing:
        sys.exit(f"{week}: 발행되지 않은 논문을 참조한다 → {', '.join(missing)}")

    date = sunday_of(week)
    out = POSTS_DIR / f"{date}-weekly-{week}.md"
    if out.exists() and not force:
        print(f"건너뜀 (이미 있음): {out.name}")
        return None

    counter: Counter[str] = Counter()
    for arxiv_id, _ in ids:
        counter.update(t for t in post_tags(arxiv_id) if t != "weekly-synthesis")
    tags = ["weekly-synthesis"] + [t for t, _ in counter.most_common(MAX_TAGS)]

    linked = WIKILINK.sub(lambda m: f"[{m.group(2)}](/posts/{m.group(1)}/)", body).strip()
    covered = " · ".join(f"[{label}](/posts/{i}/)" for i, label in ids)
    start = date - datetime.timedelta(days=6)

    out.write_text(
        "---\n"
        f"title: {yaml_quote(f'주간 종합 {week} — {headline}')}\n"
        f"date: {date} 21:00:00 +0900\n"
        "categories: [논문리뷰, Weekly-Synthesis]\n"
        f"tags: [{', '.join(tags)}]\n"
        "math: true\n"
        "image:\n"
        f"  path: {SOCIAL_IMG}\n"
        f"  alt: {yaml_quote(f'주간 종합 {week}')}\n"
        f"description: {yaml_quote(summary)}\n"
        "---\n\n"
        f"> **{start.strftime('%m/%d')}~{date.strftime('%m/%d')} 리뷰한 논문 {len(ids)}편**: {covered}\n"
        "{: .prompt-info }\n\n"
        f"{linked}\n",
        encoding="utf-8",
    )
    print(f"발행: {out.name}  (논문 {len(ids)}편, 태그 {len(tags)}개)")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("week", nargs="?", help="예: 2026-W41")
    ap.add_argument("--all", action="store_true", help="vault의 모든 주차")
    ap.add_argument("--force", action="store_true", help="이미 있는 글도 덮어쓴다")
    args = ap.parse_args()

    if args.all:
        weeks = sorted(p.stem for p in SYNTH_DIR.glob("*-W*.md"))
    elif args.week:
        weeks = [args.week]
    else:
        ap.error("주차를 지정하거나 --all 을 쓸 것")

    made = sum(convert(w, args.force) is not None for w in weeks)
    print(f"\n{made}/{len(weeks)}편 발행")


if __name__ == "__main__":
    main()
