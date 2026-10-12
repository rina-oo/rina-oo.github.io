---
title: '리뷰 허브: routing'
type: topic
topic: routing
tags:
- routing
added: '2026-08-15'
---
# 리뷰 허브: routing

일일 논문 리뷰 중 `routing` 태그가 붙은 논문들.
- 2026-08-15 [[2608.06867|라우터 논문마다 딴 세상]] — 단일턴·멀티턴·개인화 라우터를 context encoder·model encoder·scoring function·decision rule·learning signal 5개 컴포넌트로 통일하고, xRouteBench(4,767개 쿼리)와 16개 이상의 라우터 구현체를 오픈소스로 공개한 LLMRouter를 리뷰한다.
- 2026-10-12 [[2610.12242|토큰마다 모델을 갈아 끼우는 추론, 기존 서빙 엔진은 왜 못 버텼나]] — 토큰마다 다른 LLM을 호출하는 token-level routing이 효율적이라는 건 이미 알려져 있었지만, 그걸 빠르게 서빙하는 엔진은 없었다는 문제를 request-centric 인터페이스와 delayed-batching 스케줄러로 푼 TokenRouter를 리뷰합니다.
