# Rina's Paper Log 📰

> **AI가 매일 아침 논문을 읽고, 리뷰를 쓰고, 지식 그래프를 쌓는 블로그**
> https://rina-oo.github.io

매일 09:00 KST, 예약된 Claude Code 에이전트가 Hugging Face Daily Papers 1위 논문을 골라 원문(LaTeX 소스)을 읽고 한국어 심층 리뷰를 발행합니다. 사람(저)은 아침에 읽기만 합니다.

## 매일 일어나는 일

```
09:00 KST — 클라우드 예약 에이전트 기동
  1. HF Daily Papers에서 오늘의 논문 선정 (중복 발행 방지 체크)
  2. arXiv /e-print/ LaTeX 원본 확보 (PDF 파싱은 폴백)
  3. 원문 정독 → 한국어 심층 리뷰 작성 (수식·그림·표 해석 포함)
  4. 지식 레이어 갱신:
     ├ vault/papers/   논문 노트 (Obsidian 호환)
     ├ 인용 엣지        Semantic Scholar로 vault 내부 논문 간 연결
     ├ vault/topics/   태그별 허브
     └ vault/syntheses/ 주간 종합 (일요일)
  5. git push → GitHub Pages 자동 배포
  6. Notion DB에 카탈로그 행 추가 (도움 여부 판정 포함)
```

발행된 지식 레이어는 로컬 [Research OS](https://github.com/rina-oo)의 Obsidian vault로 동기화되어 임베딩 검색·지식 그래프·QA에 쓰입니다. 구조는 **"생성은 클라우드, 로컬은 material view"** — 맥북이 꺼져 있어도 지식은 git에 계속 쌓입니다.

## 저장소 구조

| 경로 | 역할 |
|---|---|
| `_posts/` | 발행된 리뷰 (`YYYY-MM-DD-<arxiv_id>.md`) |
| `REVIEW_GUIDE.md` | 리뷰 작성 규격 — 에이전트가 매일 맨 먼저 읽는 단일 기준 |
| `scripts/select_paper.py` | 오늘의 논문 선정 |
| `scripts/fetch_paper.py` | arXiv LaTeX 소스/PDF 확보 |
| `scripts/build_knowledge.py` | 논문 노트·인용 엣지·토픽 허브 생성 |
| `vault/` | 지식 레이어 (Jekyll 발행 제외, Research OS로 동기화) |
| `assets/img/posts/` | 리뷰에 쓰인 논문 Figure |

## 스택

- **글쓰기**: Claude Code 예약 루틴 (클라우드, 매일 자동)
- **호스팅**: GitHub Pages + Jekyll ([Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) 테마)
- **댓글**: [giscus](https://giscus.app) (GitHub Discussions) · **통계**: [GoatCounter](https://www.goatcounter.com)
- **지식 연동**: Semantic Scholar API, Obsidian vault, 임베딩 검색 (multilingual-e5)
- **로컬 개발**: Docker (`docker compose up -d` 후 http://localhost:4000)

## 리뷰 원칙 (REVIEW_GUIDE.md 요약)

**옮기지 말고 해석한다.** 번역이 아니라 읽고 소화해서 설명하는 글. 수식은 핵심 3~5개만 4단 구성(도입→수식→기호→의미)으로, 그림은 직접 열어본 뒤 축과 의미를 설명, 표는 행 생략 없이 전체 재현 후 패턴 해석. 논문 주장('~라고 합니다')과 검증된 사실('~입니다')의 말투 구분. 없는 수치 만들기 금지.

---

*사람의 개입: 이 README와 가이드 문서, 그리고 아침의 독서뿐.*
