# start.md — session entry for starwatch

> **How to start a session:** open Grok in this directory, then say
> `read start.md` (or just `start`). Then state your **Outcome** in one line.
>
> Do **not** open other docs unless this file’s pull-on-miss table says so.
> Thin harness: `~/.grok/docs/thin-harness.md`


**Outcome default:** safe telescope control via Starwatch HTTP API (or mock); no internet exposure of :8787.  
**Thin harness:** `~/.grok/docs/thin-harness.md`.

State: `Track: scope|pi|api|imaging | Outcome: <one line>`

## Facts

| Item | Value |
|------|--------|
| Scope | Celestron NexStar Evolution 9.25 |
| Control path | Mac/DGX agent → HTTP :8787 → Pi → INDI → USB hand controller |
| Dev default | **Mock mode** (no hardware) |
| Pi host | `starwatch-pi` / `192.168.100.122` (often offline — not AIOps CRIT) |

## Red lines

- Do **not** expose port **8787** to the public internet  
- Require API key when leaving mock (`STARWATCH_API_KEY`)  
- Abort/park safely; don’t leave slews hanging without status  
- Scope assembly/firmware before blaming software — see pull-on-miss  
- Don’t turn astronomy Pi into long-term robot brain (robotics is separate)

## Commands (dev)

```bash
source .venv/bin/activate  # if used
pip install -e ".[dev]"    # once
starwatch status
starwatch-server           # HTTP for agents
curl -s http://localhost:8787/health
```

## Pull-on-miss only

| Path | When |
|------|------|
| `docs/celestron/SETUP-GUIDE.md` | Scope still in box / first light |
| `docs/handoff.md` | Pi arrived — Andrew flash, Grok configure |
| `docs/arrival-checklist.md` | Hardware unbox order |
| `docs/agents.md` | Tool list / voice flow detail |
| `config/indi-profile.md` | INDI driver setup |

## Do not

- Preload full celestron manual set  
- Load investing/mia MCP stacks for a slew  
- Assume Pi is online without a ping/health check  

## Agent memory

Optional Qdrant `agent-memory__*` on miss only.
