---
title: '리뷰 허브: reinforcement-learning'
type: topic
topic: reinforcement-learning
tags:
- reinforcement-learning
added: '2026-08-04'
---
# 리뷰 허브: reinforcement-learning

일일 논문 리뷰 중 `reinforcement-learning` 태그가 붙은 논문들.
- 2026-08-04 [[2607.23802|정답 없는 문제를 '스파이 게임'으로 채점한다]] — 요약이나 창작처럼 정답이 없는 open-ended 과제에 RLVR을 적용하기 위해, "누가 정보가 부족한 스파이인가"를 맞히는 사회적 추리 게임으로 바꿔치는 RLSVR/SpyRL을 리뷰한다. LLM 판정자 없이도 순위 기반 보상만으로 요약·창작·수학 전 영역에서 일관된 향상을 만든 방법론과, 그 이면의 한계를 함께 짚는다.
- 2026-08-05 [[2608.02023|레퍼런스 음성 없이 목소리를 '설계'한다]] — 레퍼런스 음성이 없어도 자연어 캡션만으로 화자를 설계하고, 음성·환경음·효과음을 한 waveform 안에서 동시에 생성하는 ByteDance의 통합 TTS 모델 SwanTale을 리뷰한다. SwanVAE, Engram conditioning, Unified MoE, GRPO 후처리까지 데이터부터 모델·후처리까지 전 파이프라인을 뜯어본다.
- 2026-08-09 [[2608.05987|국지적 신호는 아직 credit이 아니다]] — 에이전틱 RL에서 turn 단위 credit을 "국지적 self-distillation gap"이 아니라 "그 gap이 누적 belief를 얼마나 revision했는가"로 재정의한 AgentOPSD를 리뷰한다. Bayes factor에서 출발해 재귀적 belief update, sign-aligned credit, bounded advantage reshaping까지 이어지는 설계를 뜯어본다.
- 2026-08-11 [[2608.03573|SFT는 싸우고 RL은 공존한다]] — SFT는 멀티태스크 학습에서 서로 충돌하는데 왜 RL은 공존할까요? 파라미터 업데이트의 크기와 방향을 직접 뜯어보고, GRPO의 advantage zero-sum 성질로 그 이유를 증명한 뒤, 태스크별로 따로 학습해서 그냥 더하기만 하는 Parallel-RL까지 이어지는 논문을 리뷰합니다.
