# Arrival Checklist — Pi 5 + Evolution 9.25

Work through this in order when the Amazon order lands. Check boxes as you go.

## Before You Unbox

- [ ] Clear a bench with good light — static-sensitive board
- [ ] Have on hand: Phillips screwdriver (case), USB-C PD 27W supply (kit or case)
- [ ] Confirm hand controller **bottom USB port** (not phone dock on top)
- [ ] Pick a hostname now: e.g. `starwatch-pi` or `stellarmate` (used in agent URLs)
- [ ] Reserve a static DHCP lease on your router for the Pi (MAC address after first boot)

---

## 1. Assemble the Pi Rig

- [ ] Seat Crucial P310 2230 on NVMe HAT (one screw, gentle pressure until click)
- [ ] Mount Pi 5 board onto HAT / case standoffs
- [ ] Attach active cooler per GeeekPi instructions
- [ ] Close metal case; verify NVMe not obstructing airflow
- [ ] **Do not power on** until assembly is complete

---

## 2. Power Supply — Read This

You need **two** power paths. Plan both before first light.

### Pi 5 (always on during observing)

| Option | Notes |
|--------|-------|
| **A. Dedicated USB-C PD 27W** (recommended to start) | Use the RasTech / GeeekPi 27W supply. Pi 5 + NVMe + WiFi peaks ~15–20W. 27W PD is correct. |
| **B. Share scope 12V** (cleaner field setup) | Step down 12V → 5V/5A USB-C PD (e.g. buck converter rated for Pi 5). **Not** a cheap phone charger — Pi 5 needs PD negotiation. |

- [ ] Label which cable is Pi power vs scope power
- [ ] Test Pi boots stable for 30 min indoors before taking outside
- [ ] Outdoor: one shared 12V astro battery is fine **if** the 5V leg is rated 5A continuous

### NexStar Evolution 9.25

- [ ] Charge internal battery fully (first boot indoors)
- [ ] Note runtime with Pi drawing from same battery if using shared 12V (budget ~2–3W extra for Pi)
- [ ] Keep a **backup** 12V source (Talentcell / West Mountain Radio style) for long winter sessions

### Power checklist (field night)

- [ ] Pi powered and booted **before** connecting USB to hand controller
- [ ] USB cable from Pi to controller is **short** (6–12") and strain-relieved
- [ ] Scope battery > 50% before unparking
- [ ] Graceful shutdown: `telescope_park` → wait for park → `sudo shutdown -h now` on Pi

---

## 3. Flash & First Boot (StellarMate OS)

- [ ] Download [StellarMate OS](https://stellarmate.com/) image (Pi 5 / NVMe variant)
- [ ] Flash to NVMe via USB adapter on Mac ([Raspberry Pi Imager](https://www.raspberrypi.com/software/) or `dd`)
- [ ] Pre-configure WiFi + SSH in imager advanced options
- [ ] Insert NVMe, power Pi, wait for boot (~2 min first time)
- [ ] SSH in: `ssh pi@<hostname>.local` (or IP from router)
- [ ] Run `sudo raspi-config` → confirm NVMe boot, expand filesystem if needed
- [ ] `sudo apt update && sudo apt upgrade -y`

---

## 4. Connect the Telescope

- [ ] Mount scope, power scope on, complete normal power-up / alignment on hand controller first
- [ ] USB: Pi → **bottom** of NexStar hand controller
- [ ] Verify serial device: `ls -l /dev/ttyACM*` or `/dev/ttyUSB*`
- [ ] In Ekos Profile Editor → Mount → **Celestron AUX** → correct port, 115200 baud
- [ ] Test slew in Ekos GUI before trusting agents

See `config/indi-profile.md` for Ekos settings.

---

## 5. Install Starwatch

```bash
git clone https://github.com/ajwharton/starwatch.git
cd starwatch
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[indi]"
cp .env.example .env
```

- [ ] Edit `.env`: `STARWATCH_MODE=indi`, set `STARWATCH_API_KEY` (long random string)
- [ ] Enable systemd service — see `docs/setup-pi.md`
- [ ] `sudo ufw allow from 192.168.0.0/16 to any port 8787` (adjust subnet)
- [ ] From Mac indoors:

```bash
curl http://starwatch-pi.local:8787/health
curl -H "X-API-Key: YOUR_KEY" http://starwatch-pi.local:8787/status
```

---

## 6. First Agent Slew (Indoors / Backyard)

- [ ] `POST /unpark` (or voice: "unpark the backyard scope")
- [ ] `POST /slew` with `{"target": "M31"}` or a bright star you can see
- [ ] Confirm scope moves, `GET /status` shows updated RA/DEC
- [ ] `POST /tracking` with `{"mode": "sidereal"}`
- [ ] End session: `POST /park`

---

## 7. Network & WiFi

- [ ] Pi on 5 GHz WiFi if router supports it (less interference than 2.4)
- [ ] Static DHCP lease reserved
- [ ] mDNS works: `ping starwatch-pi.local` from Mac
- [ ] Optional: short Ethernet run to house if backyard signal is weak

---

## 8. Outdoor / Winter Prep (NH)

- [ ] Ventilated weatherproof enclosure around metal case (not airtight)
- [ ] Desiccant pack inside enclosure, replaced seasonally
- [ ] No long USB — inches only, protected from snow drip
- [ ] Park and cover scope before precip
- [ ] Test cold-start once in garage (~32°F) before trusting a January night

---

## 9. TV / Media (when ready)

Goal: processed images on the Samsung TV without manual copying.

Samsung **QN65S95FAFXZA** (65" OLED, per TV API) on **192.168.100.6** (control) and **192.168.100.70** (media/DLNA).

- [ ] Enable SMB or Jellyfin on Pi (1TB NVMe has room)
- [ ] Point TV at `//starwatch-pi/captures` via Source → Media Server (use **.70** for browse)
- [ ] Agent TV control via REST at **.6:8001** (power, apps, slideshow trigger)
- [ ] Agent save path: `captures/` → nightly sync to share
- [ ] Ask Grok to finish TV share wiring once Pi share is live

See `docs/tv-setup.md`.

---

## 10. Cables & Adapters to Buy If Missing

| Item | Why |
|------|-----|
| Short USB-A → Micro-USB or USB-B | Hand controller port (verify yours before buying) |
| USB-C PD 27W supply + cable | Pi dedicated power |
| 12V → 5V/5A USB-C PD buck | Optional shared astro battery power |
| USB NVMe enclosure | Flash SSD from Mac before first Pi boot |
| Short outdoor-rated Ethernet | WiFi fallback |

---

## Quick Reference

| Service | Port | URL |
|---------|------|-----|
| Starwatch API | 8787 | `http://starwatch-pi.local:8787` |
| INDI | 7624 | TCP (Ekos / PyIndi) |
| SSH | 22 | `ssh pi@starwatch-pi.local` |

## When You're Ready

Reply **"ready for setup"** in chat — we'll walk first boot live, verify the Ekos profile, and run the first indoor agent slew together.