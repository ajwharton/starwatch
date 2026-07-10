# Track: `rl-small`

## Goal

Improve **reinforcement learning on small models** (trainability, sample efficiency, stability, eval) — something Andrew can run and iterate, not frontier-scale only.

## User skill

**Strong** — knows RL well. Prefer depth, citations, failure modes, and “what changes for small models specifically.” Less hand-holding; more sharp prioritization.

## In scope

- Online RL, offline RL, preference methods (DPO/ORPO/KTO), process rewards  
- Small base models (≤~7–8B class unless stated)  
- Reward hacking, KL control, over-optimization  
- Synthetic data + RL interaction  
- Eval: capability vs sycophancy vs tool-use  
- Curiosity / exploration bonuses **as algorithms**, grounded in experiments  

## Out of scope (unless asked)

- Full pretraining from scratch at huge scale  
- Pure infra without RL signal  

## Success metrics (examples)

- Higher task reward at fixed compute  
- Lower collapse / less mode-seeking  
- Better tool-use or anti-sycophancy at fixed KL  
- Reproducible ablations on a named setup  

## Query seeds (rotate)

**X / web**

- small model RLHF DPO 2025 2026  
- process reward model small LLM  
- GRPO RLOO PPO small model  
- reward hacking language model  
- offline RL language model  

**Contradict**

- DPO fails when  
- RLHF over-optimization small model  
- process reward model gaming  

**Authors / venues to watch** (non-exhaustive)

- Recent arXiv RLHF / alignment / post-training  
- Open-source stacks: TRL, OpenRLHF, veRL, etc. (verify current)

## Dig emphasis

1. What transfers from big-model RL to small?  
2. What is **not** worth copying from frontier blogs?  
3. One experiment runnable on consumer/prosumer GPU this month  

## Inject prompt slant

- Assume expert reader  
- Demand equations / algorithms named correctly  
- Demand failure modes and eval design  
