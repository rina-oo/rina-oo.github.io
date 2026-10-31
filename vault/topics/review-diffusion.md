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
- 2026-09-29 [[2609.31620|레이어를 하나로 고정하지 말고 무작위로 섞어라]] — Representation autoencoder는 인코더의 어느 레이어를 합쳐 latent로 쓸지 고정된 규칙으로 정합니다. 문제는 얕은 레이어와 깊은 레이어 중 어느 쪽을 고르느냐에 따라 복원 품질과 생성 품질이 서로 반대로 움직인다는 것입니다. FuseReg는 이 선택 자체를 고정하지 않고 학습 때마다 무작위 레이어 부분집합을 섞어 넣는 방식으로 이 트레이드오프를 정면 돌파합니다.
- 2026-09-16 [[2609.11638|자기가 만든 영상을 다시 노이즈 씌워 재생하며 학습시킨다]] — 실시간 스트리밍 아바타와 영상 편집을 하나의 인프라 위에서 밀어붙인 Vidu S2 기술보고서를 읽고, 핵심 학습 기법인 Self-Replay Forcing과 프레임 정렬 어텐션, 그리고 인간 평가 표본 크기의 허점까지 짚어봅니다.
- 2026-10-07 [[2610.05608|소리까지 함께 만드는 비디오 생성 모델]] — 입술 싱크까지 되는 5초짜리 text-to-audio-video 생성 모델 Kandinsky 6.0 Video를 리뷰합니다. 영상과 오디오를 따로 사전학습한 뒤 블록마다 양방향 cross-attention으로 묶고, OmniNFT 기반 RL과 2단계 디스틸레이션으로 다듬어 16GB 소비자 GPU에서도 돌아가게 만든 과정을 봅니다.
- 2026-10-13 [[2610.12572|DiffusionNFT는 왜 불안정했나]] — diffusion/flow-matching 모델의 online RL 후처리에서, 효율적이지만 불안정했던 DiffusionNFT의 불안정 원인을 "forward-reverse consistency force"로 규명하고, 이를 설계로 제거한 DiffusionART를 리뷰합니다.
- 2026-10-25 [[2610.24738|편집하면서 동시에 레이어로 쪼갠다]] — 중국 화남이공대·칭화대·JD.com 연구진이 공개한 LayerEditor는 이미지 편집과 RGBA 레이어 분해를 하나의 diffusion transformer로 묶어, 편집 결과를 재사용 가능한 레이어 스택으로 동시에 생성합니다.
- 2026-10-26 [[2610.30926|MLLM 잠재표현이 생성 모델에 무시당하는 문제]] — HKUST와 Tencent Video 연구진이 제안한 FAPL은 MLLM이 만든 잠재표현을 비디오 생성 모델이 무시하고 우회하는 문제를 3단계 학습으로 해결해, 제한된 입력으로부터의 시간적 추론과 캐릭터·장면·행동·카메라별 선택적 제어를 모두 개선합니다.
- 2026-10-31 [[2610.39633|분포를 통째로 맞출 수 없다면, 평균과 분산이라도]] — DMD 기반 few-step 이미지 생성 distillation에 생성기 EMA 특징의 평균·표준편차를 맞추는 명시적 모멘트 손실을 더한 Intrinsic Distribution Matching(IDM)을 리뷰합니다. reverse-KL field를 가우시안 성분과 잔차로 분해해 모멘트 매칭의 근거를 제시하고, Z-Image-Turbo·Qwen-Image에서 2 NFE 기준 LongText-Bench 최고 점수를 달성합니다.
