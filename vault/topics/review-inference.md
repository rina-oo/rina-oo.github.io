---
title: '리뷰 허브: inference'
type: topic
topic: inference
tags:
- inference
added: '2026-10-09'
---
# 리뷰 허브: inference

일일 논문 리뷰 중 `inference` 태그가 붙은 논문들.
- 2026-10-09 [[2609.38169|틀림에도 때와 장소가 있다]] — Linear attention의 recurrent state를 양자화할 때 에러가 '언제'(기억 수명)와 '어디서'(key row·value column) 생기느냐에 따라 영향이 다르다는 것을 분석하고, 이를 반영한 STEPQuant로 6비트에서 FP32급 정확도를 유지하며 서빙 메모리를 최대 68.7% 줄인 논문을 리뷰합니다.
- 2026-10-12 [[2610.12242|토큰마다 모델을 갈아 끼우는 추론, 기존 서빙 엔진은 왜 못 버텼나]] — 토큰마다 다른 LLM을 호출하는 token-level routing이 효율적이라는 건 이미 알려져 있었지만, 그걸 빠르게 서빙하는 엔진은 없었다는 문제를 request-centric 인터페이스와 delayed-batching 스케줄러로 푼 TokenRouter를 리뷰합니다.
