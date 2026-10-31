---
title: '리뷰 허브: distillation'
type: topic
topic: distillation
tags:
- distillation
added: '2026-08-17'
---
# 리뷰 허브: distillation

일일 논문 리뷰 중 `distillation` 태그가 붙은 논문들.
- 2026-08-17 [[2608.13546|2시간을 끊김 없이]] — 디노이저 컨텍스트를 키우지 않고도 2시간 연속 생성을 지탱하는 Evoke를 리뷰한다. 장면 기하를 외부 world state bank로 빼내고, teacher를 chunk-wise sparse attention으로 재설계해 30초 장기 supervision을 3-step student에 distill한다.
- 2026-09-06 [[2609.04199|매번 부르지 말고 한 번 구워라]] — 매 호출마다 큰 LLM을 부르는 대신, 자연어로 적은 함수 명세를 한 번 훈련시켜 0.6B짜리 로컬 어댑터로 구워버리는 "compile by training"을 실제 서비스로 배포한 논문을 읽는다.
- 2026-09-10 [[2609.08183|라우팅 로그가 곧 훈련 데이터다]] — 실서비스 라우팅 하니스가 남기는 로그 자체가 재귀적 자기개선(RSI)에 필요한 경험과 피드백이라는 관찰에서 출발해, 라우팅 점수로 SFT 커리큘럼과 on-policy distillation을 짜고 평가 결과로 다음 학습 데이터를 다시 배분하는 NeoHorse-1 리포트를 읽는다.
- 2026-10-02 [[2609.36484|모델이 아니라 방향을 베낀다]] — RL로 학습된 teacher를 on-policy distillation으로 베낄 때, teacher를 '도착점'이 아니라 '방향'으로 보자는 제안입니다. hidden state 공간에서 base→teacher residual을 teacher보다 더 멀리 extrapolate해서 학생에게 가르치면, 네 가지 base/teacher 조합 모두에서 student가 teacher를 능가합니다.
- 2026-09-24 [[2609.25804|정답률 59.7%]] — 에이전트가 긴 작업 중간에 내리는 판단, 즉 "안목(taste)"을 사람 손을 빌리지 않고 트라젝토리의 사후 결과에서 자동으로 뽑아내 측정하는 Taste-Bench를 읽는다. 최고 모델도 59.7%에 그치고, 추론 예산을 늘려도 안 되지만, 이 안목은 distillation으로 학습이 가능하다.
- 2026-10-04 [[2609.35259|On-Policy가 항상 옳다는 믿음]] — RLVR이 SFT보다 forgetting이 적고 업데이트가 sparse하다는 주장의 숨은 전제, 'on-policy라서'가 진짜 원인인지를 distillation이라는 통제된 실험실에서 해부한 논문을 리뷰합니다. 결론은 '거의 아니다'입니다 — 범인은 대부분 KL 방향과 학습률이었습니다.
- 2026-10-08 [[2610.08448|커버리지보다 신뢰도]] — 서로 다른 토크나이저를 쓰는 teacher-student 사이의 on-policy distillation에서, 정렬 범위(coverage)를 넓히려는 시도가 오히려 성능을 깎아먹는다는 것을 실험과 gradient 분석으로 보여준 논문을 리뷰합니다. 핵심은 '얼마나 많이 맞추느냐'가 아니라 '얼마나 믿을 만하게 맞추느냐'입니다.
- 2026-10-10 [[2610.12374|에이전트를 위한 '코드로 쓰는 세계']] — 시뮬레이터의 명시적 상태와 비디오 월드모델의 사실적 화면을 분리해 결합한 AgentGarten을 리뷰합니다. 에이전트는 코드로 돌아가는 엔진에서 상태를 관리하고, 신경망 렌더러가 그 상태를 실시간 영상으로 그려줍니다.
- 2026-10-18 [[2610.21601|끝점만 보면 속는다]] — 교사 모델의 RL 학습 전후 정책 변화만 보고 증류하는 기존 방법에 중간 체크포인트를 하나 더 추가해, 그 변화가 일관된 방향이었는지 확인하고 신호를 걸러내는 Waypoint-OPD를 리뷰합니다.
- 2026-10-25 [[2610.24738|편집하면서 동시에 레이어로 쪼갠다]] — 중국 화남이공대·칭화대·JD.com 연구진이 공개한 LayerEditor는 이미지 편집과 RGBA 레이어 분해를 하나의 diffusion transformer로 묶어, 편집 결과를 재사용 가능한 레이어 스택으로 동시에 생성합니다.
- 2026-10-31 [[2610.39633|분포를 통째로 맞출 수 없다면, 평균과 분산이라도]] — DMD 기반 few-step 이미지 생성 distillation에 생성기 EMA 특징의 평균·표준편차를 맞추는 명시적 모멘트 손실을 더한 Intrinsic Distribution Matching(IDM)을 리뷰합니다. reverse-KL field를 가우시안 성분과 잔차로 분해해 모멘트 매칭의 근거를 제시하고, Z-Image-Turbo·Qwen-Image에서 2 NFE 기준 LongText-Bench 최고 점수를 달성합니다.
