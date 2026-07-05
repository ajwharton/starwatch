# Pi Handoff — Andrew flashes, Grok configures

When the Pi 5 kit arrives, Andrew handles hardware + OS; Grok handles everything after the Pi is on the network.

**Before Pi:** Complete scope assembly, [CFM firmware](../celestron/FIRMWARE.md), and at least one SkyAlign session per [`celestron/SETUP-GUIDE.md`](../celestron/SETUP-GUIDE.md).

## Andrew does

- [ ] Assemble Pi 5 + NVMe + case (see `arrival-checklist.md` §1–2)
- [ ] Flash **StellarMate OS** to NVMe
- [ ] Pre-configure in Raspberry Pi Imager:
  - Hostname (suggest: `starwatch-pi`)
  - WiFi credentials
  - **SSH enabled** (password or key)
  - User `pi` (or note alternate username)
- [ ] First boot, confirm Pi joins `192.168.100.0/24`
- [ ] Note the Pi's IP or confirm `starwatch-pi.local` resolves
- [ ] Reply **"ready for setup"** with:
  - Pi IP or hostname
  - SSH username
  - How Grok gets access (SSH key on Mac, password in secure channel, Cursor remote, etc.)
  - Whether scope USB is connected yet (OK if not — Starwatch can install before scope)

## Grok does (once SSH/network access is granted)

- [ ] `apt update && apt upgrade`
- [ ] Confirm NVMe boot, disk space, hostname
- [ ] Verify / install INDI Celestron AUX driver (`indi_celestron_aux`)
- [ ] Clone `github.com/ajwharton/starwatch`, `pip install -e ".[indi]"`
- [ ] Generate API key, write `.env`, set `STARWATCH_MODE=indi`
- [ ] Configure `indiserver` + Ekos profile for NexStar Evolution 9.25
- [ ] Install + enable `starwatch.service` (systemd)
- [ ] Firewall: LAN access to 8787 (Starwatch) and 7624 (INDI)
- [ ] Smoke test: `curl /health`, `/status`, mock slew if scope not connected
- [ ] When scope is USB-connected: verify `/dev/ttyACM*`, first real unpark/slew/park
- [ ] Document final IP, API key location, and serial port in repo config
- [ ] (Later) SMB share `captures/` for Samsung TV at `192.168.100.70`

## What to have ready for handoff

| Item | Why |
|------|-----|
| Pi on same LAN as Mac (`192.168.100.x`) | SSH + API tests from indoors |
| SSH access | Grok runs all configuration remotely |
| StellarMate OS (not plain Raspberry Pi OS) | INDI/Ekos pre-baked |
| USB-A → Mini-USB cable (1–3 ft) | Scope tests — see `cables-and-power.md` |
| 27W USB-C PD PSU (if not in kit) | Pi power |

## Access patterns that work

1. **SSH from Mac** — Grok runs `ssh pi@starwatch-pi.local` in harness (best)
2. **Cursor / remote terminal** — Andrew opens SSH session, Grok drives commands
3. **Direct on Pi** — Andrew at keyboard; Grok provides copy-paste blocks (fallback)

## Success criteria

From the Mac indoors:

```bash
ssh pi@starwatch-pi.local hostname
curl http://starwatch-pi.local:8787/health
curl -H "X-API-Key: …" http://starwatch-pi.local:8787/status
```

With scope connected and aligned:

```bash
curl -X POST -H "X-API-Key: …" http://starwatch-pi.local:8787/unpark
curl -X POST -H "X-API-Key: …" -H "Content-Type: application/json" \
  -d '{"target":"M31"}' http://starwatch-pi.local:8787/slew
```

Andrew says **"ready for setup"** — Grok takes it from there.