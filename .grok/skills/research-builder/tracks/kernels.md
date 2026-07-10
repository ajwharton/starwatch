# Track: `kernels`

## Goal

**Model-specific GPU kernel / compiler optimization** — squeeze latency and memory for *Andrew’s* stacks (inference/training kernels, recompilation, fusion). Maximize **bang for buck** while learning.

## User skill

**Learning while doing** — newer to GPU recompilation / deep kernel land than to RL.  
Every dig must include:

1. **Map of the space** (vocabulary + decision tree)  
2. **Ordered path** (what to learn/build this week vs later)  
3. **Anti-rabbit-holes**  

## In scope

- PyTorch eager vs `torch.compile` vs custom CUDA/Triton  
- Attention backends (SDPA, FlashAttention, vendor libs) — **when each matters**  
- Fusion, memory bandwidth vs compute bound  
- Profiling: Nsight, PyTorch profiler, `torch.profiler`  
- Kernel recompilation / specialization for fixed shapes  
- Quantization interaction with kernels (only if it affects kernel choice)  

## Out of scope (defer)

- Writing a full FA3 clone from scratch in week 1  
- ASIC / non-NVIDIA unless asked  
- Cosplaying compiler PhD without a profile  

## Decision tree (always refresh if stale)

```
Is it attention?
  yes → measure: is attention the hotspot?
         yes → try SDPA / FlashAttention / vendor first (don’t hand-roll)
         no  → leave attention alone
Is it memory-bound elementwise / epilogue?
  yes → fusion / compile / epilogue fusion before raw CUDA
Is it a known matmul/GEMM shape?
  yes → cuBLAS/cuDNN/CUTLASS paths; only custom if profiler proves gap
Fixed shapes in production?
  yes → specialization / compile / autotune worth it
Still learning?
  yes → profile ONE real model path before any custom kernel
```

## Bang-for-buck tiers (default teaching order)

| Tier | Do this | Why |
|------|---------|-----|
| **0** | Profile real model (one batch, one GPU) | Without this, all advice is cosplay |
| **1** | `torch.compile` / better SDPA / correct FA install | Hours of work, often double-digit % |
| **2** | Shape specialization, CUDA graphs, memory layout | After compile saturates |
| **3** | Triton fusion for hot epilogues | When profiler names the op |
| **4** | Custom CUDA / CUTLASS templates | Only with proven gap + tests |

**FlashAttention:** use when attention is hot and shapes supported — **library**, not first custom project.  
**Raw torch:** correct default for **iteration**; not the final perf ceiling.  
**Custom kernels:** last, not first.

## Success metrics

- Profile-backed “hot op” list for a named model  
- Latency or memory win with correctness check  
- Written note: what was tried and failed  

## Query seeds

**X / web**

- torch.compile inductive speedup 2025 2026  
- FlashAttention 3 SDPA PyTorch  
- Triton fused kernel tutorial  
- CUDA graph inference LLM  
- CUTLASS 3 epilogue fusion  
- Nsight compute bandwidth bound  

**Contradict**

- torch.compile slower when  
- FlashAttention not faster  
- Triton slower than PyTorch  
- compile graph break  

## Dig emphasis

1. What is the **highest ROI learning task this week**?  
2. What should Andrew **not** build yet?  
3. One **profile → change → measure** experiment  

## Inject prompt slant

- Tutor mode without condescension  
- Force profiler-first  
- Ban “just rewrite in CUDA” without evidence  
