# Setup guide — from zero to first light

Checklist for **NexStar Evolution 9.25 (12092)**. Work top to bottom; don't skip firmware (step 4).

## Phase 0 — inventory

From manual “What’s in the box”:

- [ ] Fork mount + LiFePO4 battery (internal)
- [ ] Tripod (9.25" uses **larger** tripod — no click-fit, bolt mount)
- [ ] OTA 9.25" (you install on fork — not pre-installed like 6")
- [ ] 40 mm + 13 mm eyepieces, 1.25" star diagonal, StarPointer
- [ ] NexStar+ hand control + hand-control cable to mount
- [ ] AC adapter (12V 2A, multi-plug)
- [ ] Your gear: USB-A→Mini-USB (Pi/PC), 6D II imaging stack (when it arrives)

---

## Phase 1 — mechanical assembly (indoors)

### Tripod

1. Spread legs, level with bubble level and leg index marks.
2. Accessory tray on center column; tighten support nut firmly.

### Mount on tripod

1. Center mount on tripod post (9.25" **does not** click — align sockets, bolt tight).
2. Thread **three** mounting bolts from under tripod head.

### OTA on fork (9.25" only)

1. Loosen altitude clutch; rotate so quick-release knob faces down; re-lock.
2. Loosen quick-release knob; slide dovetail from **back**, fork on **left**, read “Evolution” nameplate.
3. Tighten quick-release knob.

### Visual accessories

1. Star diagonal → visual back (set screws).
2. 40 mm eyepiece → diagonal (start every session with low power).
3. StarPointer on dovetail rail; align at night (Phase 3).

**Clutch warning:** Don't unlock altitude/azimuth clutches while aligned — alignment is lost.

---

## Phase 2 — power & battery

**Can't find the charger?** See what it looks like: [`images/ac-adapter-2amp-celestron-18778.jpg`](images/ac-adapter-2amp-celestron-18778.jpg) (Celestron model **18778**, 12V 2A, black brick + snap-on US/EU/UK/AU plugs + barrel cable).

Manual battery rules:

- [ ] **Charge to full** on first receipt (included 12V AC adapter).
- [ ] Use only included 12V 2A supply or FCC/CE **12V ≥2A** tip-positive.
- [ ] Recharge every 3–6 months in storage.
- [ ] Don't store fully discharged or above 140°F.

**Power switch:** ON = 1, OFF = 0. Logo LED on = power good.

**Not for Pi:** Mount **USB Power Output** (5V 2A) is for phones only. Pi uses its **own 27W USB-C** supply.

---

## Phase 3 — WiFi & switches (know these, Starwatch uses home WiFi)

| Switch / LED | Position / meaning |
|--------------|-------------------|
| **WiFi switch UP** | Direct Connect — scope broadcasts `SkyQLink-xx` |
| **WiFi switch DOWN** | Access Point — join home router (see manual Appendix B) |
| **Reset** | Ballpoint only if mount freezes after power cycle |

For **Starwatch**: Pi joins your **home LAN** (`192.168.100.x`). You can use hand control + Pi without SkyPortal fighting for control. See [CEVO addendum](manuals/CEVO_Addendum.pdf) — only one controller at a time.

---

## Phase 4 — firmware update (Mac, before Pi)

**Required if never updated.** Updates **hand control + motor controller**.

→ Full steps: [**FIRMWARE.md**](FIRMWARE.md)

Short version:

1. Hand control → **AUX port on mount** (CFM doc specifies top AUX).
2. USB **Mini-B** on hand paddle bottom → Mac (USB-C or USB-A).
3. CFM 3 from https://software.celestron.com/Evolution/cfm3/
4. Mac: install **Prolific PL2303** driver if needed.
5. Run CFM3 → Seek Devices → Update both packages.

---

## Phase 5 — first alignment (hand control)

Skip SkyPortal for now — use **NexStar+** plugged into any **AUX** port.

1. Power on → “Verifying Packages…” → “Evolution”.
2. **ALIGN** → **SkyAlign** (easiest: any 3 bright stars).
3. Enter time (24h), DST, time zone, date.
4. Slew to star 1 → center in StarPointer → ENTER → center in eyepiece → **ALIGN**.
5. Repeat stars 2 and 3 (widely spaced).
6. **“Align Success”** → try GoTo Moon or a bright planet.

**Daytime test:** Solar System Align or one-star manual (Moon with care — not for visual without filter).

**Hibernate:** Menu → Hibernate saves alignment across power-off (useful between sessions).

---

## Phase 6 — visual checkout

- [ ] Slew to Moon or bright star with 40 mm.
- [ ] Switch to 13 mm — refocus.
- [ ] If stars won't focus / triangular — see [collimation guide](manuals/SCT%20&%20EdgeHD%20Collimation%20Guide(1).pdf) (common after shipping).

---

## Phase 7 — Starwatch (when Pi arrives)

→ [**STARWATCH-INTEGRATION.md**](STARWATCH-INTEGRATION.md)

You: flash StellarMate, get Pi on network.  
Grok: INDI, Starwatch, Celestron AUX profile, first agent slew.

---

## Phase 8 — imaging (when adapters arrive)

→ [**IMAGING.md**](IMAGING.md)

6D Mark II on rear cell with f/6.3 reducer — **remove star diagonal** for camera.

---

## Quick troubleshooting

| Symptom | See |
|---------|-----|
| Hand control “No Response” | Try different **AUX** port; check power; [troubleshooting PDF](manuals/Celestron%20NexStar+%20Hand%20Control%20Troubleshooting%20Guide_2022-WEB-F.pdf) |
| WiFi won't connect | CEVO addendum; forget old `SkyQLink` networks on phone |
| GoTo misses targets | Re-align; add alignment stars in SkyPortal; check clutches locked |
| DSLR hits fork arm | Set **altitude slew limit** (manual p.14) — max < 90° with big camera |