# TV Setup — Samsung QN65S90FAFXZA

*Placeholder — filled in when we configure your network TV.*

## Goal

Browse astro images captured by Starwatch from the living room TV without manual file copying.

## Planned approach

1. **SMB share** on Pi (`/home/pi/captures`) or home NAS/DGX
2. **Samsung TV** — built-in media player, Gallery, or SmartThings
3. Optional **Jellyfin** on Pi for polished slideshow / metadata

## Discovery (pending)

When Andrew asks to configure the TV, we'll:

- [ ] Scan LAN for Samsung device (SSDP / mDNS / port 8001)
- [ ] Confirm TV IP and model (QN65S90FAFXZA)
- [ ] Enable PC/SMB input on TV (Settings → General → External Device Manager)
- [ ] Mount share from TV or add via SmartThings
- [ ] Test with a sample JPEG from `starwatch captures/`

### Scan log — 2026-07-04

Subnet: `192.168.100.0/24` (UniFi gateway `192.168.100.1`)

| Result | Detail |
|--------|--------|
| Samsung UPnP | Not found (TV likely off or asleep) |
| Samsung mDNS | No `_samsung._tcp` responders |
| Unknown `192.168.100.172` | MAC `50:9a:4c` → **Dell Inc.** (not the TV) |

**Next scan:** Turn TV on, then ask Grok to re-scan. Samsung sets typically expose port **8001** (remote API) and respond to SSDP with `Samsung` / `Tizen` in headers.

## Network notes

| Field | Value |
|-------|-------|
| TV IP | *TBD — rescan when TV is on* |
| TV model | Samsung QN65S90FAFXZA (S90F OLED) |
| Home subnet | 192.168.100.0/24 |
| Share host | Pi or DGX — *TBD* |
| Share path | `//starwatch-pi/captures` — *TBD* |