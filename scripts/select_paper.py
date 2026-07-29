#!/usr/bin/env python3
"""HuggingFace Daily Papers에서 오늘 리뷰할 논문을 선정한다.

선정 규칙:
  1. KST 기준 어제 날짜의 daily papers를 조회한다.
  2. 해당 날짜에 논문이 없으면(주말/공휴일) 최대 MAX_LOOKBACK일까지 거슬러 올라간다.
  3. upvote 내림차순으로 정렬해, 아직 리뷰하지 않은(= _posts/ 파일명에 arXiv ID가
     없는) 첫 논문을 고른다.
  4. 선정 결과를 JSON으로 stdout에 출력한다.

사용법:
    python scripts/select_paper.py [--date YYYY-MM-DD]

향후 확장: discuss.pytorch.kr 등 다른 소스를 추가하려면 fetch_hf_daily()와 같은
시그니처의 fetch 함수를 만들어 SOURCES에 등록한다.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

API_URL = "https://huggingface.co/api/daily_papers"
MAX_LOOKBACK = 5  # 주말 + 공휴일까지 커버
KST = timezone(timedelta(hours=9))
POSTS_DIR = Path(__file__).resolve().parent.parent / "_posts"
ARXIV_ID_RE = re.compile(r"(\d{4}\.\d{4,5})")


def reviewed_ids() -> set[str]:
    """_posts/ 파일명에서 이미 리뷰한 arXiv ID를 수집한다."""
    ids = set()
    if POSTS_DIR.is_dir():
        for f in POSTS_DIR.glob("*.md"):
            m = ARXIV_ID_RE.search(f.name)
            if m:
                ids.add(m.group(1))
    return ids


def fetch_hf_daily(date_str: str) -> list[dict]:
    """지정 날짜의 daily papers를 upvote 내림차순 후보 리스트로 반환한다."""
    resp = requests.get(API_URL, params={"date": date_str}, timeout=30)
    resp.raise_for_status()
    items = resp.json()
    candidates = []
    for item in items:
        paper = item.get("paper", item)
        arxiv_id = paper.get("id")
        if not arxiv_id:
            continue
        candidates.append(
            {
                "arxiv_id": arxiv_id,
                "title": paper.get("title", "").strip(),
                "upvotes": paper.get("upvotes", 0),
                "summary": paper.get("summary", "").strip(),
                "github_repo": paper.get("githubRepo"),
                "source": "hf-daily-papers",
                "source_date": date_str,
            }
        )
    candidates.sort(key=lambda c: c["upvotes"], reverse=True)
    return candidates


def select(base_date: datetime | None = None) -> dict:
    done = reviewed_ids()
    base = base_date or (datetime.now(KST) - timedelta(days=1))
    for back in range(MAX_LOOKBACK + 1):
        date_str = (base - timedelta(days=back)).strftime("%Y-%m-%d")
        candidates = fetch_hf_daily(date_str)
        if not candidates:
            continue
        for c in candidates:
            if c["arxiv_id"] in done:
                continue
            c["arxiv_url"] = f"https://arxiv.org/abs/{c['arxiv_id']}"
            c["ar5iv_url"] = f"https://ar5iv.labs.arxiv.org/html/{c['arxiv_id']}"
            c["hf_url"] = f"https://huggingface.co/papers/{c['arxiv_id']}"
            return c
    raise SystemExit(
        f"최근 {MAX_LOOKBACK + 1}일 안에 리뷰할 새 논문을 찾지 못했습니다."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--date",
        help="기준 날짜(YYYY-MM-DD, 이 날짜의 daily papers부터 탐색). 기본: KST 어제",
    )
    args = parser.parse_args()
    base = None
    if args.date:
        base = datetime.strptime(args.date, "%Y-%m-%d").replace(tzinfo=KST)
    result = select(base)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
