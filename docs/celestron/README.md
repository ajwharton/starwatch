# Celestron NexStar Evolution 9.25 — setup docs

Official manuals live in [`manuals/`](manuals/). These guides distill them for **your 12092** rig and the **Starwatch** (Pi + INDI + agents) path.

## Start here (you haven't set up yet)

| Order | Guide | What it covers |
|-------|--------|----------------|
| 1 | [**SETUP-GUIDE.md**](SETUP-GUIDE.md) | Assembly → charge → align → first light |
| 2 | [**FIRMWARE.md**](FIRMWARE.md) | CFM update from your Mac (**do before Pi**) |
| 3 | [**STARWATCH-INTEGRATION.md**](STARWATCH-INTEGRATION.md) | USB to Pi, INDI, agents, imaging |
| 4 | [**IMAGING.md**](IMAGING.md) | 6D Mark II + f/6.3 reducer on rear cell |

## Source PDFs (in repo)

| File | Contents |
|------|----------|
| `12090_12091_12092_NexStar_EVO_Telescopes_Series_Manual_5lang_Web.pdf` | Main manual — assembly, WiFi, SkyPortal, hand control, specs |
| `Updating your NexStar Evolution mount with Celestron Firmware Manager (CFM)_5Languages 03092026.pdf` | **CFM 3** — mount + hand control firmware (Mar 2026) |
| `nexstar_plus_hc_Addendum_5lang.pdf` | NexStar+ hand control buttons & catalogs |
| `CEVO_Addendum.pdf` | WiFi conflict tips |
| `Celestron NexStar+ Hand Control Troubleshooting Guide_2022-WEB-F.pdf` | No Response / BOOT LOADER / CFM recovery |
| `SCT & EdgeHD Collimation Guide(1).pdf` | Collimation after shipping |
| `1299179004_91024inst0405.pdf` | SCT OTA / visual back / eyepieces |

Windows-only installers in Downloads (`NexRemote`, `CPWI`) are **not** used for Starwatch — we use **INDI + Starwatch API** on the Pi instead.

## Model 12092 specs (from manual)

| | |
|--|--|
| Aperture | 235 mm (9.25") |
| Focal length | 2350 mm, f/10 |
| Mount | Alt-az, brass worm gears |
| Battery | LiFePO4 9.6V 4.5Ah (~10 hr) |
| AUX ports | **4** (hand control → any AUX) |
| Power in | **12V DC tip-positive**, up to 5A (included adapter **2A**) |
| USB on mount | **5V out, 2A max** — phone charge only, **not for Pi** |
| PC port | **USB Mini-B on bottom of NexStar+ hand paddle** |