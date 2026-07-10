---
name: research-builder
description: >
  Meta skill for gated curious research digs across discrete tracks (RL on small
  models, GPU/kernel optimization, equities thesis). Use when the user asks for
  research builder, research dig, curiosity bots, research subjects, inject prompts
  for DeepSeek/Grok, bang-for-buck in kernels/RL/markets, or runs /research-builder
  /research-dig /curiosity-dig. Builds digests + injectable prompts, not sycophancy.
metadata:
  short-description: "Gated research digs → digests + inject prompts"
---

# Research Builder (meta skill)

## Purpose

Turn “I read X and told my AI it’s cool” into a **gated loop**:

```
goal → search (X/web/arxiv) → critique → contradict → experiment card
     → digest + inject prompt(s) → optional memory
```

**Grok’s job in this skill:** native X + web + structure.  
**User’s job:** pick track, approve experiments, run GPU/RL/trading risk.  
**Other LLMs (DeepSeek etc.):** receive **inject prompts** — frozen, skeptical, tool-ready.

Do **not** default to praise. Partner mode: friction first.

## Tracks (Andrew’s active set)

| ID | Track | Data root |
|----|--------|-----------|
| `rl-small` | RL on small models | `tracks/rl-small.md` |
| `kernels` | Model-specific GPU/kernel optimization | `tracks/kernels.md` |
| `equities` | Thesis-bound equities edges | `tracks/equities.md` |

Config files live next to this skill:  
`~/.grok/skills/research-builder/tracks/*.md`

On-disk artifacts (writable):

```
~/research-builder/
  digests/YYYY-MM-DD_<track>.md
  inject/YYYY-MM-DD_<track>_*.md
  memory/<track>_notes.jsonl
  experiments/<track>/...
```

## When to run

1. User names a track or says “research dig / research builder / curiosity dig”
2. User asks “what should I learn next” in RL / kernels / equities
3. `/research-builder` or `/research-dig` with optional track id
4. Scheduled multi-track dig (if configured)

If no track given: dig **all three** briefly (one card each) or ask which track if time-boxed.

## Hard rules

1. **No pure agreement.** Every seed gets risks + prior art or “unknown — search needed.”
2. **Tools before strong claims** (X semantic/keyword search, web_search, open_page).
3. **≥1 disconfirming angle** per dig (paper/thread that says the hot idea fails).
4. **Bang-for-buck ranking** required for learning tracks (especially `kernels`).
5. **Equities:** no “sure alpha.” Thesis + falsifiers + what would kill the trade. Not financial advice.
6. Write artifacts under `~/research-builder/` when dig is non-trivial (not just chat).

## Dig procedure (per track)

### Step 0 — Load track

Read `tracks/<id>.md`: goals, out-of-scope, query seeds, beginner gaps, success metrics.

### Step 1 — State

- `memory_search` / read last lines of `~/research-builder/memory/<track>_notes.jsonl` if present
- Note user skill: e.g. kernels = **learning while doing**; RL = **stronger background**

### Step 2 — Seek (Grok native)

Run **3–6** targeted searches (mix X + web):

- From track `query_seeds`
- One **contradict** query (“doesn’t work”, “regression”, “failed”, “slower than”)
- One **2025/2026** or “state of” query for freshness

Prefer primary sources (papers, official docs, repo READMEs) over pure meme accounts.

### Step 3 — Score seeds (internal)

For each hit keep only if:

- Relevant to track goal, AND
- Actionable in ≤2 weeks OR foundational for hand-holding path

Drop engagement bait with no technical content.

### Step 4 — Critique card (per kept hit)

```
### <short title>
Source: <url or @handle>
Claim: ...
Why it matters for THIS track: ...
Risks / limits: ...
Prior art: ...
Contradict / failure mode: ...
Bang-for-buck (1–5): N — <why>
Next 1-hour action: ...
```

### Step 5 — Experiment card (1–3 per dig)

Use template `templates/experiment-card.md`. Must be falsifiable.

### Step 6 — Outputs (always produce these three layers)

#### A. Digest (human)

Write `~/research-builder/digests/YYYY-MM-DD_<track>.md` using `templates/digest.md`.

Structure:

1. **Headline** — one line: what to care about this week  
2. **Bang-for-buck stack** — ordered list (do first → later)  
3. **Map of the space** — short orientation for learning tracks  
4. **Critique cards** — top 3–5 hits  
5. **Experiments** — 1–3 cards  
6. **Open questions** — what Andrew still needs to decide  
7. **Sources**

#### B. Inject prompts (other LLMs / next Grok session)

Write under `~/research-builder/inject/`:

| File | Use |
|------|-----|
| `..._deepseek_sft_or_rl.md` | Paste into DeepSeek / training notes |
| `..._grok_session.md` | Paste as next Grok user message |
| `..._implementer.md` | Code-focused implementer (kernels/RL) |

Use `templates/inject-prompt.md`. Each inject prompt MUST include:

- Role + non-sycophancy rule  
- Track goal + constraints  
- What was found (compressed)  
- Required output format (plan / code / critique)  
- Explicit “I don’t know → search/tool” behavior  

#### C. Memory line

Append one JSON line to `~/research-builder/memory/<track>_notes.jsonl`  
(schema in `templates/memory-line.json`).

Optional: `agent-memory__add_memory` one-liner for cross-session retrieval.

## Curiosity scores (lightweight, for dig quality)

Self-check before finishing (aim ≥4/5 yes):

- [ ] B1 Friction before praise  
- [ ] B2 Used X/web tools  
- [ ] B3 At least one contradict angle  
- [ ] B4 ≥1 experiment card with metric  
- [ ] B5 If revisiting old note, update belief  

## Learning-track mode (`kernels` especially)

When user is new to a sub-area:

1. **Layer 0 map** — vocabulary + decision tree (e.g. when PyTorch vs custom kernel vs FlashAttention)  
2. **Layer 1 highest ROI path** — 3–5 day learning/build sequence  
3. **Layer 2 advanced** — only after Layer 1  
4. **Anti-rabbit-holes** — list of shiny topics to defer  

Never dump “read everything about CUDA.” Always **ordered**.

## Equities-track mode

- Prefer **named thesis** with catalysts, time horizon, disconfirming data  
- Separate **narrative** vs **measurable**  
- Risk: position sizing, regime change, liquidity — always  
- Not advice; research scaffolding only  

## Session modes

| User says | Do |
|-----------|-----|
| `research dig kernels` | Full dig on kernels only |
| `research dig all` | Short dig ×3 tracks |
| `inject only kernels` | Refresh inject prompts from last digest + light new search |
| `bang for buck kernels` | Map + ROI stack only (faster) |
| `hand holding kernels` | Learning path emphasis, fewer experiment cards |

## Relationship to other skills

- **research-monitor** (Mia): hourly background scans — different product; can *feed* seeds into this skill  
- **amherst-observing-weather**: unrelated domain  
- This skill is the **meta research subject builder** for personal multi-track R&D  

## Done criteria

Dig is done when:

1. Digest written (or clearly inlined if user said chat-only)  
2. ≥1 inject prompt written  
3. ≥1 experiment card  
4. Friction-first tone throughout  
