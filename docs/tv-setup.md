# TV Setup — Samsung QN65S90FAFXZA

## Identified addresses

| IP | Role | Status (2026-07-04) |
|----|------|---------------------|
| **192.168.100.70** | **Data / media** (active) | Responds to ping; hostname `samsung.localdomain` |
| **192.168.100.6** | **Control** (likely) | Unreachable — dormant or secondary interface |

### 192.168.100.70 — active interface

| Field | Value |
|-------|-------|
| Hostname | `samsung.localdomain` |
| MAC | `38:8c:ef:47:f4:3b` (Samsung Electronics) |
| Open port | **8080** (Samsung `WebServer` — media/DLNA stack) |
| Port 8001 | Closed (remote control API not enabled yet) |

Samsung TVs commonly expose:

- **8080** — DLNA / AllShare / media serving (browsing photos & video from network shares)
- **8001** — REST remote control API (sleeps until *IP Remote* is enabled in TV settings)

Use **.70** for media share mounting and slideshow. Use **.6** for control once it wakes — many Samsung sets register a second address for SmartThings / IP-remote that only appears when the control stack is active.

### 192.168.100.6 — secondary / control

- Does not respond to ping or TCP on common ports (8001, 8080, 9197, 55000) while TV is in current state
- Still listed in router — likely:
  - Secondary WiFi/control interface that sleeps independently, or
  - Stale lease from a prior connection (TV may have moved to .70), or
  - Ethernet interface (inactive unless cabled)

**Action:** Check UniFi client list for both IPs on the same MAC. If same MAC → dual-interface TV. If different MAC → two entries, one stale.

---

## Goal

Browse astro images captured by Starwatch from the living room TV without manual file copying.

## Planned approach

1. **SMB share** on Pi (`/home/pi/captures`) or home NAS/DGX
2. **Samsung TV** at **192.168.100.70** — Source → PC / Media Server, or Gallery app
3. Optional **Jellyfin** on Pi for polished slideshow / metadata

Control automation (volume, input, power) can target **.6** once IP Remote is enabled and that address responds.

---

## Enable before media test

On the TV (Settings → General → External Device Manager):

- [ ] **IP Remote** — ON (opens port 8001 on active interface; may wake .6)
- [ ] **Device Connect Manager** — allow phone/PC connections
- [ ] Note which IP answers on port 8001 after enabling (re-scan)

---

## Starwatch integration checklist

- [ ] Rescan both IPs after IP Remote enabled
- [ ] Confirm which IP serves SMB/DLNA browse (expect .70)
- [ ] Stand up SMB on Pi: `//starwatch-pi/captures`
- [ ] Add share on TV: Source → Media Server / PC
- [ ] Drop test JPEG; verify Gallery / slideshow
- [ ] (Optional) Jellyfin with TV app

---

## Network reference

| Field | Value |
|-------|-------|
| TV model | Samsung QN65S90FAFXZA (S90F OLED) |
| Data IP | `192.168.100.70` (`samsung.local`) |
| Control IP | `192.168.100.6` (pending — rescan) |
| Home subnet | `192.168.100.0/24` |
| Gateway | `192.168.100.1` (UniFi) |
| Share host | Pi or DGX — *TBD when Pi arrives* |
| Share path | `//starwatch-pi/captures` — *TBD* |

---

## Rescan command (for agents)

When TV settings change, re-probe:

```bash
for ip in 192.168.100.6 192.168.100.70; do
  echo "=== $ip ==="
  ping -c 1 -W 2 $ip
  nc -z -G 2 $ip 8001 && echo "8001 open (control)"
  nc -z -G 2 $ip 8080 && echo "8080 open (media)"
done
```