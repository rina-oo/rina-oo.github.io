---
title: '리뷰 허브: image-generation'
type: topic
topic: image-generation
tags:
- image-generation
added: '2026-09-29'
---
# 리뷰 허브: image-generation

일일 논문 리뷰 중 `image-generation` 태그가 붙은 논문들.
- 2026-09-29 [[2609.31620|레이어를 하나로 고정하지 말고 무작위로 섞어라]] — Representation autoencoder는 인코더의 어느 레이어를 합쳐 latent로 쓸지 고정된 규칙으로 정합니다. 문제는 얕은 레이어와 깊은 레이어 중 어느 쪽을 고르느냐에 따라 복원 품질과 생성 품질이 서로 반대로 움직인다는 것입니다. FuseReg는 이 선택 자체를 고정하지 않고 학습 때마다 무작위 레이어 부분집합을 섞어 넣는 방식으로 이 트레이드오프를 정면 돌파합니다.
- 2026-10-13 [[2610.12572|DiffusionNFT는 왜 불안정했나]] — diffusion/flow-matching 모델의 online RL 후처리에서, 효율적이지만 불안정했던 DiffusionNFT의 불안정 원인을 "forward-reverse consistency force"로 규명하고, 이를 설계로 제거한 DiffusionART를 리뷰합니다.
- 2026-11-03 [[2610.36545|비디오 생성모델에게 '몇 프레임 뒤를 상상할지' 직접 고르게 하기]] — 피사체 유지·캐니맵 변환·지시어 편집처럼 서로 다른 조건부 이미지 생성 과제를, 비디오 생성모델이 배운 "프레임 간 변화"의 눈으로 재해석한 FrameForge를 리뷰합니다. 조건과 타깃 사이 가상의 시간 간격을 입력마다 다르게 고르는 MoTE와, 그 사이를 매개하는 잠재 추론 상태 CoTR을 하나의 공유 LoRA로 묶어 DreamBench·COCO2017·GEdit-Bench에서 동시에 성능을 끌어올립니다.
