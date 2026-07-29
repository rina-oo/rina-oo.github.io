# 논문 리뷰 작성 가이드

매일 자동 발행되는 논문 리뷰의 품질과 일관성을 위한 규격이다. 예약 에이전트와 수동 작성 모두 이 문서를 따른다.

## 작성 절차

1. `python3 scripts/select_paper.py` 실행 → 오늘 리뷰할 논문 JSON 획득
   (이미 오늘 날짜 포스트가 `_posts/`에 있으면 **아무것도 하지 않고 종료**한다 — 중복 실행 안전장치)
2. 논문 원문 읽기 — 반드시 abstract만 보고 쓰지 말 것:
   - 1순위: ar5iv HTML (`https://ar5iv.labs.arxiv.org/html/<arxiv_id>`)
   - 2순위: arXiv abs 페이지 + HF paper 페이지 토론
   - GitHub repo가 있으면 README도 참고
3. 아래 규격대로 리뷰 작성 → `_posts/YYYY-MM-DD-<arxiv_id>.md` 저장
4. 커밋 메시지: `post: <arxiv_id> <논문 제목 요약> 리뷰` → push

## 파일 규격

- 경로: `_posts/YYYY-MM-DD-<arxiv_id>.md` (날짜는 KST 오늘, 예: `2026-07-29-2607.24653.md`)
- 파일명의 arXiv ID는 중복 방지 키로 쓰이므로 **반드시 포함**한다.

## Front matter

```yaml
---
title: "한국어 요약 제목 — 원제 그대로 (Original Title)"
date: YYYY-MM-DD HH:MM:SS +0900
categories: [논문리뷰, Daily-Paper]
tags: [llm, ...]        # 소문자, 논문 주제 3~6개
math: true
description: 한 문장 요약 (리스트/SEO에 노출)
---
```

## 본문 구성 (총 2,000자 이상)

1. **논문 소개** — 어떤 논문이고 왜 주목받았나 (HF upvote 수, 소속 기관, 공개 여부 등 맥락)
2. **배경과 문제의식** — 이 논문이 풀려는 문제, 기존 접근의 한계
3. **핵심 아이디어와 방법론** — 가장 긴 섹션. 수식이 필요하면 MathJax(`$...$`, `$$...$$`) 사용. 구조도·표는 마크다운으로 재구성
4. **실험 결과** — 주요 벤치마크 수치를 표로 정리하고, 숫자가 의미하는 바를 해석
5. **한계와 의문점** — 논문이 인정한 한계 + 리뷰어 관점의 비판적 질문
6. **시사점** — 실무자/연구자에게 주는 의미, 관련 후속 연구 방향

## 스타일

- 한국어 존댓말이 아닌 **평서체**("~한다", "~이다")로 쓴다.
- 전문 용어는 첫 등장 시 영문 병기. 예: 증류(distillation)
- 근거 없는 과장 금지 — 논문에 없는 수치나 주장을 만들지 않는다. 불확실하면 "논문에 명시되지 않았다"라고 쓴다.
- 본문 첫 섹션 앞에 출처 블록을 넣는다:

```markdown
> **원문**: [arXiv](https://arxiv.org/abs/<id>) · [HuggingFace](https://huggingface.co/papers/<id>) (👍 upvote수) · [GitHub](repo주소, 있으면)
{: .prompt-info }
```
