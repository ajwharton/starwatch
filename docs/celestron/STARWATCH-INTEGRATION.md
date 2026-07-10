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

**Working path (HC Mini-USB / NexStar PC port) — verified 2026-07-09:**

| Setting | Value |
|---------|--------|
| Driver | **`indi_celestron_gps`** (NexStar serial protocol) |
| Device name | **Celestron GPS** |
| Serial | **`/dev/ttyUSB0`** common (Prolific PL2303 bridge); sometimes `ttyACM*` |
| Baud | **9600** |

- **`indi_celestron_aux` @ 115200** targets the AUX motor bus — it did **not** work over the hand-control PC USB port (timeouts to ALT/AZM). Do not force AUX on the HC Mini-USB cable.
- After reboot: set port/baud and CONNECT (helper on Pi: `~/starwatch/scripts/connect-mount.sh` if installed).
- Ekos profile: see [`config/indi-profile.md`](../../config/indi-profile.md) — update to **Celestron GPS** / 9600 for this USB path.

### Alignment requirement

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