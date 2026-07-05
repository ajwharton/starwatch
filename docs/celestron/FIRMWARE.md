# Firmware update — Celestron Firmware Manager (CFM 3)

From Celestron doc dated **2026-03-09**. Do this **once**, from your **Mac**, before Pi/INDI setup.

## What gets updated

1. **NexStar+ hand control**
2. **Evolution motor controller** (mount firmware)

## What you need

| Item | You have? |
|------|-----------|
| NexStar+ hand control plugged into mount | ✓ |
| USB **Mini-B** cable (hand paddle bottom → Mac) | ✓ (same cable as Pi later) |
| Mac on USB directly — **no hub** | — |
| Internet for CFM download | — |

Cable types (Celestron):

- Mac with USB-C → **USB-C to USB-Mini**
- Mac with USB-A → **USB-A to USB-Mini**

## Mac steps

### 1. Prolific serial driver (if CFM can't see hand control)

1. Download from Celestron's CFM page (linked inside the PDF).
2. Install **PL2303 Serial** extension; approve in **System Settings → Privacy & Security**.
3. Reboot if prompted.

### 2. Download CFM 3

- https://software.celestron.com/Evolution/cfm3/
- Download **macOS** archive (M-series Macs supported).
- Extract; run **`CFM3.app`** (may need right-click → Open first time).

### 3. Connect hardware

1. **Power on** mount (hand control can show errors — OK).
2. Plug hand control into **AUX port at top of mount** (per 2026 CFM instructions).
3. USB Mini-B on **bottom of hand paddle** → Mac USB port directly.
4. Wait **10 seconds** for hand control boot.

### 4. Update

1. Open **CFM3.app** → orange window → **Seek Devices** (10–15 s).
2. Should find **NexStar+** then **Evolution motor controller**.
3. Click **Update** → installs two files (~1–2 min).
4. **Do not** unplug or power off during update.
5. Success: “All your devices are up to date.”

### 5. After update

- Disconnect USB; power-cycle mount.
- Hand control should show **Evolution** normally.
- If **BOOT LOADER** or **No Response**: see troubleshooting PDF in `manuals/`.

## Windows (alternate)

Same CFM URL → `CFM3.exe`; hand control to AUX; USB-A→Mini to PC.

## Not used for Starwatch

- `NexRemoteInstall_1_7_24.exe` — legacy PC control
- `Setup_CPWI_2.5.6.exe` — Celestron Windows stack

Starwatch uses **INDI `indi_celestron_aux`** on the Pi, not CPWI/NexRemote.