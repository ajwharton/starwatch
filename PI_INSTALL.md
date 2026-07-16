# Starwatch Pi — production install

Date: 2026-07-08

## Stack
- **INDI core 2.2.3** built from source (`/home/pi/Projects/indi`) → `/usr`
- **indi_celestron_aux** from indi-3rdparty → `/usr/bin/indi_celestron_aux`
- **pyindi-client 2.2.0** built with SWIG from `/home/pi/Projects/pyindi-client` (editable install)
- **starwatch** at `/home/pi/starwatch` venv, mode **indi**

## Services
| Unit | Role |
|------|------|
| `indiserver.service` | `indiserver -v -p 7624 indi_celestron_aux` |
| `starwatch.service` | HTTP API :8787 |

## Network
- IP: 192.168.100.122 (reserved)
- UFW: 22 any; 8787+7624 from 192.168.100.0/24
- API key: `/home/pi/starwatch/.api_key`

## Scope
1. Align on hand control first
2. USB Pi → bottom Mini-USB on NexStar+ HC
3. Expect `/dev/ttyACM0` (pi in dialout)
4. API: unpark / slew / track / park

## Rebuild notes
```bash
# INDI core
cd ~/Projects/build/indi && make -j$(nproc) && sudo make install && sudo ldconfig
# AUX driver
cd ~/Projects/build/indi-celestronaux && make -j$(nproc) && sudo make install
# pyindi (regenerate SWIG if needed)
cd ~/Projects/pyindi-client
swig -python -c++ -threads -I/usr/include -I/usr/include/libindi -outdir PyIndi -o indiclientpython_wrap.cxx indiclientpython.i
source ~/starwatch/.venv/bin/activate && pip install -e .
```

## Stability
- cmdline: pcie_aspm=off nvme_core.default_ps_max_latency_us=0
- WiFi powersave off
- headless multi-user
- Leave case off until hardware seating is proven

## Mount connection (2026-07-09 smoke)

- HC USB = Prolific PL2303 → `/dev/ttyUSB0` (not ttyACM0)
- **`indi_celestron_aux` does NOT work** on HC PC port (timeouts to ALT/AZM motors)
- **`indi_celestron_gps` @ 9600 works** — Evolution, HC firmware 5.35
- Device name for Starwatch: **Celestron GPS**
- Connect helper: `~/starwatch/scripts/connect-mount.sh`
- Mount must be **aligned** on HC before useful slews
