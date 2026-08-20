---
title: '리뷰 허브: llm'
type: topic
topic: llm
tags:
- llm
added: '2026-07-29'
---
# 리뷰 허브: llm

일일 논문 리뷰 중 `llm` 태그가 붙은 논문들.
- 2026-07-29 [[2607.24653|2.8조 파라미터 오픈 모델의 등장]] — Moonshot AI가 공개한 2.8T 파라미터 MoE 모델 Kimi K3의 아키텍처(KDA·AttnRes·Stable LatentMoE), 학습 레시피, 평가 결과를 심층 분석한다.
- 2026-08-01 [[2607.28618|논문이 아니라 '주장'을 검색한다]] — 논문이 아니라 출처가 달린 개별 '주장(claim)'을 검색 단위로 바꾼 화학 문헌 인프라 AskChem을 리뷰한다. 240만 개 claim, evidence graph, Living Taxonomy 구조와 GPT-5.5 grounding 벤치마크, 그리고 공개된 실제 하이브리드 검색 구현까지 함께 살펴본다.
- 2026-08-04 [[2607.23802|정답 없는 문제를 '스파이 게임'으로 채점한다]] — 요약이나 창작처럼 정답이 없는 open-ended 과제에 RLVR을 적용하기 위해, "누가 정보가 부족한 스파이인가"를 맞히는 사회적 추리 게임으로 바꿔치는 RLSVR/SpyRL을 리뷰한다. LLM 판정자 없이도 순위 기반 보상만으로 요약·창작·수학 전 영역에서 일관된 향상을 만든 방법론과, 그 이면의 한계를 함께 짚는다.
- 2026-08-09 [[2608.05987|국지적 신호는 아직 credit이 아니다]] — 에이전틱 RL에서 turn 단위 credit을 "국지적 self-distillation gap"이 아니라 "그 gap이 누적 belief를 얼마나 revision했는가"로 재정의한 AgentOPSD를 리뷰한다. Bayes factor에서 출발해 재귀적 belief update, sign-aligned credit, bounded advantage reshaping까지 이어지는 설계를 뜯어본다.
- 2026-08-14 [[2608.00677|프롬프트가 아니라 '환경'을 공격한다]] — 단일 프롬프트 인젝션이 아니라 워크스페이스·메모리·플랜 상태 같은 "환경" 자체를 진화시켜 에이전트를 공격하는 OpenART 벤치마크와 EMHA 공격 정책을 리뷰한다. 10K 시나리오, 15개 배포 에이전트, 85%의 pooled ASR, 그리고 "37 스텝 뒤에 터지는" long-horizon safety drift까지.
- 2026-08-15 [[2608.06867|라우터 논문마다 딴 세상]] — 단일턴·멀티턴·개인화 라우터를 context encoder·model encoder·scoring function·decision rule·learning signal 5개 컴포넌트로 통일하고, xRouteBench(4,767개 쿼리)와 16개 이상의 라우터 구현체를 오픈소스로 공개한 LLMRouter를 리뷰한다.
- 2026-08-19 [[2608.15089|모델은 그대로, 하니스만 갈았다]] — 모델 가중치를 하나도 안 건드리고 GPT-5.5의 Terminal-Bench 2.1 점수를 83.1%에서 92.1%로 끌어올린 StateM을 리뷰한다. YAML 상태 기계로 에이전트의 실행 상태를 외부화하고, 전이마다 검증을 강제해 "모델은 할 줄 아는데 하니스가 놓친" 실패를 잡는다.
- 2026-08-20 [[2608.14036|Skill이 통하는 이유, 통하지 않는 이유]] — 에이전트 skill이 실제로 왜 통하는지 528개 쌍대 trajectory를 뜯어본 논문. Skill은 사실 주입(4.5%)이 아니라 절차 앵커링(65.7%)으로 작동하며, retrieval pool이 5에서 100으로 커지면 실사용 precision이 29.6%에서 3.3%로 무너진다.
