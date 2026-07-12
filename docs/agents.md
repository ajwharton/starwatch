> Pull-on-miss detail. Auto card: repo-root `AGENTS.md`. Thin harness: `~/.grok/docs/thin-harness.md`.

# Agent Integration

## Design

- **Reasoning** stays on Mac/DGX (Grok, Hermes)
- **Execution** on Pi via Starwatch HTTP API (low latency, safe wrapper around INDI)
- **Mock mode** for development without hardware

## Available Tools

| Tool | Description |
|------|-------------|
| `telescope_status` | Position, tracking, parked state |
| `telescope_slew` | Slew to catalog object or coordinates |
| `telescope_track` | Enable/disable sidereal tracking |
| `telescope_park` | Park at end of session |
| `telescope_unpark` | Begin observing |
| `telescope_abort` | Stop current slew |

## Example Voice Flow

1. User: *"Point the backyard scope at Andromeda and start tracking"*
2. Agent parses intent → `telescope_unpark`, `telescope_slew(M31)`, `telescope_track(true)`
3. Agent confirms with status readback

## Security

- Set `STARWATCH_API_KEY` on Pi
- Bind to LAN only (default `0.0.0.0` behind home router)
- Do not expose port 8787 to the internet

## Future: MCP Server

A dedicated MCP server wrapping the same API can be added for native Cursor/Grok tool access. The HTTP API is the stable contract either way.