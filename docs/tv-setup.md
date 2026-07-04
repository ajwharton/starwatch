# TV Setup — Samsung QN65S95FAFXZA

## Device identity (from TV API)

Source: `GET http://192.168.100.6:8001/api/v2/` (authoritative)

| Field | Value |
|-------|-------|
| Model | **QN65S95FAFXZA** |
| Name | 65" OLED |
| Internal model | `25_RSM_QD` |
| Type | Samsung SmartTV |
| OS | Tizen |
| Resolution | 3840×2160 |
| DUID | `uuid:b90ea709-f847-4969-877f-8fa2a85b4b8f` |
| WiFi MAC | `38:8C:EF:FA:14:2A` |

## Identified addresses (TV on — 2026-07-04)

| IP | Role | MAC | When awake |
|----|------|-----|------------|
| **192.168.100.6** | **Control** | `38:8c:ef:fa:14:2a` (WiFi) | 8001, 8002, 8080, 9197 |
| **192.168.100.70** | **Data / media** | `38:8c:ef:47:f4:3b` | 8080 only |

Two separate Samsung interfaces — not a stale lease. When the TV is **off**, `.6` goes dark and only `.70` may linger with partial services.

### 192.168.100.6 — control (primary when on)

| Field | Value |
|-------|-------|
| Hostname | `Samsung.localdomain` |
| API | `http://192.168.100.6:8001/api/v2/` |
| OS | Tizen, PowerState `on` |
| Network | WiFi (`networkType: wireless`) |

Samsung REST API responds here — remote control, app launch, power state. Use **.6** for agent automation.

### 192.168.100.70 — data / media (secondary)

| Field | Value |
|-------|-------|
| Hostname | *(none — no reverse DNS)* |
| Open port | **8080** (`WebServer` — DLNA/media) |
| Port 8001 | Closed |

Use **.70** for DLNA media browse and network share slideshow. No REST control API on this interface.

---

## Goal

Browse astro images captured by Starwatch from the living room TV without manual file copying.

## Planned approach

1. **SMB share** on Pi (`/home/pi/captures`) or home NAS/DGX
2. **Samsung TV** — Source → PC / Media Server (try **.70** first for DLNA; **.6** if share requires Smart Hub path)
3. Optional **Jellyfin** on Pi — install Samsung Jellyfin app, point at Pi server
4. **Agent control** (power, input, slideshow trigger) via REST on **.6:8001**

---

## Starwatch integration checklist

- [x] Rescan with TV on — roles confirmed
- [x] Model identified from TV API — QN65S95FAFXZA
- [ ] Stand up SMB on Pi: `//starwatch-pi/captures`
- [ ] Add share on TV: Source → Media Server / PC
- [ ] Drop test JPEG; verify Gallery / slideshow
- [ ] (Optional) Jellyfin server + Samsung TV app
- [ ] (Optional) Wire agent to TV REST at `.6:8001` for "show tonight's captures"

---

## Network reference

| Field | Value |
|-------|-------|
| TV model | Samsung QN65S95FAFXZA (65" OLED, S95F) |
| Control IP | `192.168.100.6` (`Samsung.local`) |
| Data IP | `192.168.100.70` |
| Home subnet | `192.168.100.0/24` |
| Gateway | `192.168.100.1` (UniFi) |
| Share host | Pi or DGX — *TBD when Pi arrives* |
| Share path | `//starwatch-pi/captures` — *TBD* |

---

## Rescan command (for agents)

```bash
for ip in 192.168.100.6 192.168.100.70; do
  echo "=== $ip ==="
  ping -c 1 -W 2 $ip
  nc -z -G 2 $ip 8001 && echo "8001 open (control)"
  nc -z -G 2 $ip 8080 && echo "8080 open (media)"
done
curl -s http://192.168.100.6:8001/api/v2/ | python3 -m json.tool | head -20
```

Expect `.6` dark when TV is off; `.70` may still answer on 8080.