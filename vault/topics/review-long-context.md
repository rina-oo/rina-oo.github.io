---
title: '리뷰 허브: long-context'
type: topic
topic: long-context
tags:
- long-context
added: '2026-07-29'
---
# 리뷰 허브: long-context

일일 논문 리뷰 중 `long-context` 태그가 붙은 논문들.
- 2026-07-29 [[2607.24653|2.8조 파라미터 오픈 모델의 등장]] — Moonshot AI가 공개한 2.8T 파라미터 MoE 모델 Kimi K3의 아키텍처(KDA·AttnRes·Stable LatentMoE), 학습 레시피, 평가 결과를 심층 분석한다.
- 2026-08-17 [[2608.13546|2시간을 끊김 없이]] — 디노이저 컨텍스트를 키우지 않고도 2시간 연속 생성을 지탱하는 Evoke를 리뷰한다. 장면 기하를 외부 world state bank로 빼내고, teacher를 chunk-wise sparse attention으로 재설계해 30초 장기 supervision을 3-step student에 distill한다.
- 2026-09-19 [[2609.19969|토큰당 KV 캐시 890바이트]] — 552B 파라미터 멀티모달 MoE 모델이면서 토큰당 글로벌 KV 캐시를 890바이트(DeepSeek-V4-Flash 대비 1/4)까지 줄인 DeepSeek-V4.1-Flash의 아키텍처와 성능을 읽는다.
- 2026-11-28 [[2611.34051|작은 누수가 큰 배를 가라앉힌다]] — 선형 어텐션 모델 Gated DeltaNet-2가 긴 컨텍스트 학습 중 가끔 loss가 NaN으로 터지는 원인을, erase 게이트와 key 사이의 비대칭 결합에서 찾아내고 symmetric erasure로 고친 논문을 읽어봅니다.
