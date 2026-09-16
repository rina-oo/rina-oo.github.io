---
title: '리뷰 허브: diffusion'
type: topic
topic: diffusion
tags:
- diffusion
added: '2026-08-05'
---
# 리뷰 허브: diffusion

일일 논문 리뷰 중 `diffusion` 태그가 붙은 논문들.
- 2026-08-05 [[2608.02023|레퍼런스 음성 없이 목소리를 '설계'한다]] — 레퍼런스 음성이 없어도 자연어 캡션만으로 화자를 설계하고, 음성·환경음·효과음을 한 waveform 안에서 동시에 생성하는 ByteDance의 통합 TTS 모델 SwanTale을 리뷰한다. SwanVAE, Engram conditioning, Unified MoE, GRPO 후처리까지 데이터부터 모델·후처리까지 전 파이프라인을 뜯어본다.
- 2026-08-17 [[2608.13546|2시간을 끊김 없이]] — 디노이저 컨텍스트를 키우지 않고도 2시간 연속 생성을 지탱하는 Evoke를 리뷰한다. 장면 기하를 외부 world state bank로 빼내고, teacher를 chunk-wise sparse attention으로 재설계해 30초 장기 supervision을 3-step student에 distill한다.
- 2026-09-09 [[2609.04010|품질 손실 없이 3배 빠르게]] — AR 모델의 가중치는 그대로 두고 LoRA로 붙인 확산 가중치가 토큰 블록을 병렬로 제안하면, AR 가중치가 그걸 검증해서 품질 저하 없이 최대 3배 빠르게 생성하는 Uno를 리뷰합니다.
- 2026-09-16 [[2609.11638|자기가 만든 영상을 다시 노이즈 씌워 재생하며 학습시킨다]] — 실시간 스트리밍 아바타와 영상 편집을 하나의 인프라 위에서 밀어붙인 Vidu S2 기술보고서를 읽고, 핵심 학습 기법인 Self-Replay Forcing과 프레임 정렬 어텐션, 그리고 인간 평가 표본 크기의 허점까지 짚어봅니다.
