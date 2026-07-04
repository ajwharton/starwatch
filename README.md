# Starwatch

Agentic control of a **Celestron NexStar Evolution 9.25** telescope over your home network.

Starwatch runs on a Raspberry Pi 5 (StellarMate OS recommended) connected via USB to the hand controller. Indoor agents on your Mac or DGX call a small HTTP API to slew, track, park, and query status — no ASCOM required.

## Architecture

```
┌─────────────────┐     WiFi      ┌──────────────────────┐
│  Mac / DGX      │ ────────────► │  Raspberry Pi 5      │
│  Grok agents    │   HTTP :8787  │  starwatch-server    │
│  (reasoning)    │               │         │            │
└─────────────────┘               │         ▼            │
                                  │  INDI :7624          │
                                  │  indi_celestron_aux  │
                                  │         │            │
                                  │    USB (short)       │
                                  └─────────┬────────────┘
                                            ▼
                                  NexStar Evolution 9.25
```

## Hardware (ordered)

| Component | Purpose |
|-----------|---------|
| Raspberry Pi 5 16GB kit | Telescope control node |
| Crucial P310 1TB NVMe 2230 | Boot + image storage |
| GeeekPi metal case + cooler | Outdoor-adjacent deployment |

Connect Pi to the **bottom USB port** of the NexStar hand controller. Power Pi from scope battery or shared 12V supply.

## Quick Start (development — no hardware)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Mock mode (default) — no Pi or INDI needed
starwatch status
starwatch unpark
starwatch slew M31
starwatch track on

# HTTP server for agent integration
starwatch-server
curl http://localhost:8787/health
```

## Pi Deployment (when hardware arrives)

1. Flash **StellarMate OS** to NVMe, boot Pi 5.
2. Enable **Celestron AUX** driver in Ekos (see `config/indi-profile.md`).
3. Install Starwatch:

```bash
git clone https://github.com/ajwharton/starwatch.git
cd starwatch
pip install -e ".[indi]"
cp .env.example .env  # set STARWATCH_MODE=indi and API key
```

4. Run as a systemd service (see `docs/setup-pi.md`).
5. From indoors: `curl http://starwatch-pi.local:8787/status -H "X-API-Key: your-key"`

## Agent Integration

Tool schemas in `starwatch/agent/tools.py` are ready for Grok/Hermes function calling:

```python
from starwatch.agent.tools import AGENT_TOOLS, StarwatchAgentClient

with StarwatchAgentClient("http://starwatch-pi.local:8787", api_key="secret") as client:
    client.dispatch("telescope_unpark", {})
    client.dispatch("telescope_slew", {"target": "M31"})
    client.dispatch("telescope_track", {"enabled": True})
```

Voice flow: *"Slew the backyard scope to M31"* → agent reasons → `telescope_slew` → Pi obeys.

## Project Layout

```
starwatch/
├── starwatch/
│   ├── client/       # INDI backends (mock + PyIndi)
│   ├── telescope/    # Coordinates, controller
│   ├── server/       # FastAPI agent API
│   └── agent/        # Tool schemas + HTTP client
├── config/           # YAML config + INDI profile notes
├── docs/             # Setup guides
└── tests/            # pytest suite (mock mode)
```

## License

Apache-2.0