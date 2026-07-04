# NexStar Evolution 9.25 — Starwatch compatibility

**Model:** Celestron NexStar Evolution 9.25 (item **12092**)  
**Product:** [celestron.com/products/nexstar-evolution-925-telescope](https://www.celestron.com/products/nexstar-evolution-925-telescope)

This scope is a **strong match** for the Starwatch + Pi + INDI plan.

---

## What the telescope already includes

| Included | Starwatch relevance |
|----------|---------------------|
| **NexStar+ hand control** | USB 2.0 **PC port on bottom** → Pi connects here |
| **Built-in WiFi** | SkyPortal app (optional); Starwatch uses USB/INDI instead |
| **LiFePO4 battery** (~10 hr) | Powers scope; Pi uses its own 27W supply to start |
| **AC adapter (4-plug)** | Charges mount battery indoors |
| **40mm + 13mm eyepieces** | Visual observing — not needed for agent slew |
| **StarPointer finder, diagonal** | Standard visual kit |
| **4 Aux ports** | Hand control can use any Aux port on mount |

Hand control spec (per Celestron): *"USB 2.0 port for PC connection"* — use a **USB-A to Mini-USB** cable to the **bottom** of the hand paddle (not the top phone-charging area on the mount arm).

---

## What you still need (not in scope box)

### Ordered — Pi rig

- [x] Raspberry Pi 5 16GB kit
- [x] Crucial P310 1TB NVMe 2230
- [x] GeeekPi metal case + cooler

### Buy if not in Pi kit

| Item | Status | Notes |
|------|--------|-------|
| **USB-A → Mini-USB cable**, 1–3 ft, data | ☐ **Required** | Not included with scope |
| **27W USB-C PD PSU** | ☐ Check kit first | RasTech / GeeekPi may include |
| **USB NVMe enclosure** | ☐ One-time | Flash StellarMate from Mac |

See [`cables-and-power.md`](cables-and-power.md).

### Grok configures (no purchase)

- StellarMate OS flash (you) → Starwatch, INDI, Ekos profile (Grok)
- Celestron AUX driver — free, on StellarMate

---

## NOT required for Starwatch

| Item | Why skip (for now) |
|------|---------------------|
| Celestron SkyPortal WiFi module (#93973) | Evolution **has WiFi built in** |
| StarSense AutoAlign (#94005) | Optional; manual / SkyAlign works |
| Pro HD Equatorial Wedge | Only for long-exposure EQ imaging |
| USB-to-serial adapters | NexStar+ has USB built in — no RS-232 adapter |

---

## NH / backyard optional (later)

| Item | Why |
|------|-----|
| Dew heater ring 9.25" (#94052) | Condensation on corrector plate |
| Smart dew heater controller | Automated dew management |
| 12V → 5V USB-C PD buck | Share scope battery with Pi in field |
| Ventilated outdoor Pi enclosure | Winter deployment |

---

## Connection diagram

```
Pi 5 (GeeekPi case)                    NexStar Evolution 9.25
┌─────────────────┐                    ┌──────────────────────┐
│ 27W USB-C power │── wall outlet      │ AC adapter → battery │
│ USB-A port      │── Mini-USB cable ──│ NexStar+ hand ctrl   │
│ WiFi → home LAN │                    │ (bottom PC port)     │
│ starwatch :8787 │                    │ Built-in WiFi (skip) │
└─────────────────┘                    └──────────────────────┘
         │                                        │
         └──────────── WiFi (192.168.100.x) ──────┘
                    Mac / agents indoors
```

---

## Ports — photo confirmed

| Port | Location | Use for Starwatch? |
|------|----------|-------------------|
| **Mini-USB** (USB symbol) | Edge of NexStar+ hand paddle | **Yes** — Pi USB-A → Mini-USB |
| **AUX1 / AUX2** | Mount side panel | No — hand controller & accessories only |
| Phone charge USB | Mount arm (if present) | No — charging only |

Hand controller can stay docked; use a **short, right-angle Mini-USB** plug if straight connector is tight against the mount.