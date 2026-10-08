---
title: '리뷰 허브: tokenizer'
type: topic
topic: tokenizer
tags:
- tokenizer
added: '2026-09-29'
---
# 리뷰 허브: tokenizer

일일 논문 리뷰 중 `tokenizer` 태그가 붙은 논문들.
- 2026-09-29 [[2609.31620|레이어를 하나로 고정하지 말고 무작위로 섞어라]] — Representation autoencoder는 인코더의 어느 레이어를 합쳐 latent로 쓸지 고정된 규칙으로 정합니다. 문제는 얕은 레이어와 깊은 레이어 중 어느 쪽을 고르느냐에 따라 복원 품질과 생성 품질이 서로 반대로 움직인다는 것입니다. FuseReg는 이 선택 자체를 고정하지 않고 학습 때마다 무작위 레이어 부분집합을 섞어 넣는 방식으로 이 트레이드오프를 정면 돌파합니다.
- 2026-10-08 [[2610.08448|커버리지보다 신뢰도]] — 서로 다른 토크나이저를 쓰는 teacher-student 사이의 on-policy distillation에서, 정렬 범위(coverage)를 넓히려는 시도가 오히려 성능을 깎아먹는다는 것을 실험과 gradient 분석으로 보여준 논문을 리뷰합니다. 핵심은 '얼마나 많이 맞추느냐'가 아니라 '얼마나 믿을 만하게 맞추느냐'입니다.
