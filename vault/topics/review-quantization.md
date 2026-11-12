---
title: '리뷰 허브: quantization'
type: topic
topic: quantization
tags:
- quantization
added: '2026-10-09'
---
# 리뷰 허브: quantization

일일 논문 리뷰 중 `quantization` 태그가 붙은 논문들.
- 2026-10-09 [[2609.38169|틀림에도 때와 장소가 있다]] — Linear attention의 recurrent state를 양자화할 때 에러가 '언제'(기억 수명)와 '어디서'(key row·value column) 생기느냐에 따라 영향이 다르다는 것을 분석하고, 이를 반영한 STEPQuant로 6비트에서 FP32급 정확도를 유지하며 서빙 메모리를 최대 68.7% 줄인 논문을 리뷰합니다.
- 2026-11-12 [[2611.14210|에이전트가 아니라 최적화로 모델을 고친다]] — LLM 에이전트가 158턴·9천만 토큰을 써서 고친 추론 루프 버그를, forward pass 4번과 GPU 어닐링만으로 더 정확하게, 비트는 훨씬 적게 고치는 Tree-Ising 논문 리뷰입니다.
