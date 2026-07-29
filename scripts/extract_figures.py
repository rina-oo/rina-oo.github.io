#!/usr/bin/env python3
"""논문 PDF에서 Figure를 이미지로 캡처한다.

캡션 텍스트("Figure N:")를 찾고, 같은 페이지에서 캡션 위쪽의 벡터 드로잉/이미지
영역을 합쳐 Figure 영역을 추정한 뒤 PNG로 렌더링한다.

사용법:
    python scripts/extract_figures.py <pdf> <out_dir> <figure_num> [<figure_num> ...]
"""

import sys
from pathlib import Path

import fitz  # PyMuPDF


def find_caption(doc, fig_num: int):
    needle = f"Figure {fig_num}:"
    for pno in range(len(doc)):
        rects = doc[pno].search_for(needle)
        if rects:
            return pno, rects[0]
    return None, None


def figure_bbox(page, caption_rect, prev_caption_bottom: float):
    """캡션 위쪽 드로잉·이미지 블록을 합쳐 figure 영역을 추정한다."""
    top_limit = prev_caption_bottom
    bbox = None
    candidates = [d["rect"] for d in page.get_drawings()]
    candidates += [fitz.Rect(b[:4]) for b in page.get_text("blocks") if b[6] == 1]
    # 캡션 바로 위 텍스트(축 라벨 등)도 figure의 일부일 수 있으므로 드로잉 근처 텍스트 포함
    for r in candidates:
        if r.y1 <= caption_rect.y0 + 2 and r.y0 >= top_limit and r.height < caption_rect.y0 - top_limit:
            bbox = r if bbox is None else bbox | r
    if bbox is None:
        # 드로잉이 없으면 캡션 위 150pt를 잘라낸다
        bbox = fitz.Rect(page.rect.x0 + 36, max(top_limit, caption_rect.y0 - 150),
                         page.rect.x1 - 36, caption_rect.y0)
    # figure 내부 텍스트(범례·축 라벨)를 bbox에 포함
    for b in page.get_text("blocks"):
        r = fitz.Rect(b[:4])
        if b[6] == 0 and r.y0 >= bbox.y0 - 5 and r.y1 <= caption_rect.y0 + 2 and r.y0 >= top_limit:
            bbox |= r
    bbox |= caption_rect  # 캡션 포함
    bbox.y1 = caption_rect.y1 + 20  # 캡션 여러 줄 여유
    # 캡션은 본문 전체 폭이므로 가로는 텍스트 폭으로 고정 (잘림 방지)
    bbox.x0 = min(bbox.x0, 50)
    bbox.x1 = max(bbox.x1, page.rect.x1 - 50)
    bbox &= page.rect
    return bbox


def main():
    pdf, out_dir = sys.argv[1], Path(sys.argv[2])
    fig_nums = [int(n) for n in sys.argv[3:]]
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf)
    for n in fig_nums:
        pno, cap = find_caption(doc, n)
        if pno is None:
            print(f"figure {n}: caption not found", file=sys.stderr)
            continue
        page = doc[pno]
        # 같은 페이지의 이전 figure 캡션 아래부터 탐색
        prev_bottom = 60.0
        for m in range(1, n):
            for r in page.search_for(f"Figure {m}:"):
                prev_bottom = max(prev_bottom, r.y1 + 4)
        bbox = figure_bbox(page, cap, prev_bottom)
        pix = page.get_pixmap(clip=bbox, matrix=fitz.Matrix(2.5, 2.5))
        out = out_dir / f"figure{n}.png"
        pix.save(out)
        print(f"figure {n}: page {pno + 1} -> {out} ({pix.width}x{pix.height})")


if __name__ == "__main__":
    main()
