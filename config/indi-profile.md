# INDI/Ekos Profile — NexStar Evolution 9.25

Use this profile once the Pi is running with INDI.

**Prerequisites:** Scope assembled, aligned at least once, and [**CFM firmware updated**](../docs/celestron/FIRMWARE.md) from your Mac. See [Starwatch integration](../docs/celestron/STARWATCH-INTEGRATION.md).

## Connection

1. USB cable from Pi to **bottom Mini-USB PC port** of the NexStar hand controller (not the mount 5V phone port).
2. Power the Pi from its **27W USB-C PD** supply (or later, a rated 12V→5V buck from shared astro power).
3. Start `indiserver` with the **Celestron GPS** (NexStar serial) driver:

```bash
indiserver -v -p 7624 indi_celestron_gps
```

**Note (verified 2026-07-09):** Hand-control USB enumerates as Prolific PL2303 → `/dev/ttyUSB0` at **9600** baud.  
`indi_celestron_aux` does **not** work on this port (AUX protocol / motor bus is a different path).

On Ekos, enable **Celestron GPS** (not AUX) for this USB path.

## Ekos Profile Settings

| Setting | Value |
|---------|-------|
| Mount | **Celestron GPS** |
| Connection | Serial |
| Port | `/dev/ttyUSB0` (or `ls /dev/ttyUSB* /dev/ttyACM*`) |
| Baud | **9600** |
| Alignment | Manual / SkyAlign on hand control first |
| Parking | Optional — set park position after first successful session |

Starwatch env: `STARWATCH_INDI_DEVICE=Celestron GPS`, `STARWATCH_MODE=indi`.

## Expose INDI Over WiFi

Agents on your Mac/DGX connect to the Pi's INDI server:

```bash
# On Pi — INDI default port 7624
# Ensure firewall allows LAN access:
sudo ufw allow from 192.168.0.0/16 to any port 7624
sudo ufw allow from 192.168.0.0/16 to any port 8787
```

Starwatch HTTP API (port 8787) is the preferred agent interface — it wraps INDI with safety checks.

## Verify

```bash
# From Pi
ls -l /dev/ttyUSB* /dev/ttyACM*
# optional: ~/starwatch/scripts/connect-mount.sh

# From Mac
curl http://192.168.100.122:8787/health
curl -H "X-API-Key: $KEY" http://192.168.100.122:8787/status
```
