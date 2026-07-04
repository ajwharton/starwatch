# Cables & Power — Shopping Guide

Parts to have on hand before first light. Scope: [NexStar Evolution 9.25 (12092)](evolution-925.md) — **does not include a PC USB cable**.

**Photo confirmed (2026-07-04):** hand controller edge port with USB symbol is **Mini-USB (Mini-B)**. Mount **AUX1/AUX2** are *not* PC ports — do not use for Pi.

---

## USB cable: Pi → hand controller

### What you need

| Spec | Recommendation |
|------|----------------|
| **Connector (scope side)** | **USB Mini-B** (5-pin, trapezoid shape) — bottom of hand controller |
| **Connector (Pi side)** | **USB-A** — plug into Pi 5's USB 2.0 or 3.0 port |
| **Length** | **1–3 ft (0.3–1 m)** — shorter is better outdoors |
| **Rating** | USB 2.0 **data** cable (not charge-only) |
| **Shielding** | Prefer braided / ferrite for reliability near motors |

### Correct cable name

> **USB-A to Mini-USB** (also sold as USB-A to Mini-B)

### What NOT to buy

- ❌ Micro-USB (wrong shape — smaller, flat bottom)
- ❌ USB-C to Mini-USB *unless* you add a quality USB-C → USB-A adapter on the Pi end
- ❌ Long 6ft+ cable — snow snag hazard, voltage drop
- ❌ "Charging only" cables (no data wires)

### Where to buy

| Option | Notes |
|--------|-------|
| [Cable Matters USB-A to Mini-B, 3ft](https://www.amazon.com/s?k=usb+a+to+mini+usb+3ft) | Solid budget pick |
| Celestron / High Point Scientific "NexStar USB cable" | OEM-style, known good with hand controllers |
| Monoprice USB-A to Mini-B | Good shielding, short lengths |

### Pi 5 port to use

Use any **USB-A** port on the Pi 5 (blue USB 3.0 or black USB 2.0 — either works). The dedicated **USB-C port on the Pi is power-in only**, not for the scope cable.

### After plugging in (Grok verifies on setup)

```bash
ls -l /dev/ttyACM* /dev/ttyUSB*
# Expect something like /dev/ttyACM0
```

---

## Power supply: Raspberry Pi 5

### What you need

| Spec | Requirement |
|------|-------------|
| **Standard** | USB-C **Power Delivery (PD)** |
| **Wattage** | **27W minimum** (Pi 5 + NVMe + WiFi) |
| **Voltage / current** | 5.1V @ 5A (PD negotiated) |
| **Plug** | US Type A (wall) |

### First choice — official PSU

**[Raspberry Pi 27W USB-C Power Supply](https://www.raspberrypi.com/products/27w-power-supply/)**

- 5.1V / 5.0A, 1.2m cable attached
- White or black, ~$12–15
- Also sold at Adafruit, CanaKit, The Pi Hut, Amazon (verify "official" or authorized)

### Check your kit first

Your **RasTech Pi 5 kit** and **GeeekPi case** may **already include** a 27W PD supply — unbox before buying a duplicate.

### Acceptable third-party (if kit has no PSU)

Look for packaging that explicitly says:

- "Raspberry Pi 5 compatible"
- **27W USB-C PD**
- 5V **5A** output (not 3A)

Examples that generally work:

- CanaKit 27W USB-C for Pi 5
- Vilros 27W PD for Pi 5

### Avoid

- ❌ iPhone / generic 20W USB-C chargers (underpowered under load)
- ❌ Laptop USB-C ports as sole power (current-limited)
- ❌ Unmarked "45W" multi-port GaN bricks unless they guarantee 5A on the Pi port

### Field power (later — optional)

Share the scope's **12V** astro battery:

- **12V → 5V USB-C PD buck** rated **5A continuous** (e.g. vehicle PD trigger boards with 5A profile)
- Only after indoor testing with wall PSU is stable

---

## Shopping checklist

| Item | Qty | Have? |
|------|-----|-------|
| USB-A to Mini-USB cable, 1–3 ft, data-rated | 1 | ☐ |
| Spare same cable (backup) | 1 | ☐ optional |
| 27W USB-C PD PSU (if not in kit) | 1 | ☐ |
| USB NVMe enclosure (flash SSD from Mac) | 1 | ☐ one-time |
| Short outdoor Ethernet (WiFi backup) | 1 | ☐ optional |

---

## Photo confirmation ✓

From owner photos of Evolution 9.25 (12092):

| Photo | What it shows | Pi connection? |
|-------|---------------|----------------|
| Hand controller edge | **Mini-USB** + USB symbol — PC port | **Yes — cable goes here** |
| Mount side AUX1/AUX2 | Celestron accessory ports (hand control cable) | **No** |
| Full rig | Hand controller docked on mount arm | Route short cable to Mini-USB on paddle |

Cable routing: Pi near mount base; 1–2 ft USB-A → Mini-USB to the port shown on the hand paddle (may need to tilt/unclip paddle slightly for plug clearance).