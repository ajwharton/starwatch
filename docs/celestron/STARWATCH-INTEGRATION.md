# Starwatch + Evolution — how it fits together

Starwatch does **not** replace Celestron alignment or firmware. It adds **agent/API control** after you've done a normal setup.

## Control paths (pick one primary)

| Path | When to use |
|------|-------------|
| **NexStar+ hand control** | First light, alignment, troubleshooting |
| **SkyPortal / SkyQLink WiFi** | Phone GoTo from scope WiFi (optional) |
| **Starwatch HTTP API (Pi)** | Indoor agents, automation, TV pipeline |
| **CPWI / NexRemote** | Not used in this project |

**Rule:** One master at a time. Don't SkyPortal-slew while Starwatch/INDI is commanding.

## Starwatch connection (when Pi is ready)

```
Mac/DGX agents  ──WiFi──►  Pi 5 (Starwatch :8787)
                              │
                         USB-A → Mini-B
                              │
                         NexStar+ hand paddle (bottom port)
                              │
                         AUX ──► Evolution mount
```

### Not these ports

| Port | Purpose |
|------|---------|
| AUX1–AUX4 | Hand control cable, StarSense, accessories |
| Mount USB 5V out | Charge phone/tablet only |
| 12V power in | Scope AC/battery |

### INDI on Pi (Grok configures)

- Driver: **`indi_celestron_aux`**
- Serial: `/dev/ttyACM0` typical after USB connect
- Baud: **115200**
- Ekos profile: see [`config/indi-profile.md`](../../config/indi-profile.md)

### Alignment requirement

**Align with hand control (or SkyPortal) before agent slews.** INDI does not replace SkyAlign.

Recommended session flow:

1. Power scope + Pi.
2. Align: SkyAlign 3 stars on hand control.
3. Pi `starwatch-server` connects via INDI.
4. From Mac: `POST /unpark` → `POST /slew` `{"target":"M31"}`.
5. End: `POST /park` → shut down Pi.

### WiFi coexistence

- Pi on **home WiFi** (`starwatch-pi.local`).
- Scope WiFi (`SkyQLink-xx`) optional; leave **UP** for Direct Connect or disable in hand control menu if it interferes.
- Pi does **not** need to join SkyQLink.

### Firmware prerequisite

Complete [**FIRMWARE.md**](FIRMWARE.md) first. Old mount/hand-control firmware causes INDI serial quirks.

## Agent tools

Same HTTP API documented in [`docs/agents.md`](../agents.md):

- `telescope_status`, `telescope_slew`, `telescope_track`, `telescope_park`, …

## Imaging + Starwatch

Camera on **rear cell** (6D Mark II) runs parallel to INDI — USB is hand control only. Save images to Pi `captures/` for TV share later.