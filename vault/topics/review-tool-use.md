---
title: '리뷰 허브: tool-use'
type: topic
topic: tool-use
tags:
- tool-use
added: '2026-08-26'
---
# 리뷰 허브: tool-use

일일 논문 리뷰 중 `tool-use` 태그가 붙은 논문들.
- 2026-08-26 [[2608.23283|'완료된 작업'을 지능의 단위로 삼기]] — 에이전트의 지능을 "정답을 맞혔는가"가 아니라 "실행 가능한 환경에서 검증 가능한 작업을 완료했는가"로 재정의하고, Environment Scaling과 Agentic Coordination Scaling이라는 두 축으로 이를 학습·평가하는 Apodex 1.1 기술 보고서를 읽는다.
- 2026-10-15 [[2610.18773|결정에도 전용 설계가 필요하다]] — 도구 선택·문서 식별·분류 같은 '한 번에 끝나는 결정'을 LLM이 답 토큰으로 처리하는 관행이 순서에 취약하고 캐싱이 안 되고 null 처리가 어색하다는 문제를 짚고, 요청과 후보를 분리 인코딩한 뒤 가벼운 상태 갱신만 후보 집합에 노출시키는 Jeva 아키텍처를 리뷰합니다.
- 2026-10-28 [[2610.33568|성공한 trajectory가 좋은 교재는 아니다]] — Westlake University와 Ant International 연구진이, tool-use 에이전트 SFT 데이터로 흔히 쓰는 "성공한 trajectory"가 사실은 나쁜 교재일 수 있다는 문제를 지적하고, 구조적 커버리지와 결정 단위 grounding을 함께 만족하는 데이터 구성 파이프라인 Trajectory2Gym을 제안한 논문입니다. Qwen3 1.7B부터 30B까지 다섯 스케일 전부에서 SFT만으로 RL 학습 체크포인트를 능가합니다.
