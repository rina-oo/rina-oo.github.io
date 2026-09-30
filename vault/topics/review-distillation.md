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
- 2026-09-30 [[2609.29233|관련 없는 단어 선택 하나로 사후학습을 훔쳐본다]] — 코드나 수학과 전혀 상관없는 "잠옷과 티셔츠 중 뭐가 더 어울려?" 같은 질문의 답 한 단어만으로, 비공개 파인튜닝 모델의 능력 일부를 다른 모델로 옮길 수 있다는 것을 보인 논문입니다.
