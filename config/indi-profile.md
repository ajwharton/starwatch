# INDI/Ekos Profile — NexStar Evolution 9.25

Use this profile once StellarMate OS (or Ubuntu + INDI) is running on the Pi.

## Connection

1. USB cable from Pi to **bottom port** of the NexStar hand controller (not the top phone dock).
2. Power the Pi from the scope's internal battery or a shared 12V astro power station.
3. Start `indiserver` with the Celestron AUX driver:

```bash
indiserver -v indi_celestron_aux
```

On StellarMate, enable the **Celestron AUX** driver in Ekos → Profile Editor instead.

## Ekos Profile Settings

| Setting | Value |
|---------|-------|
| Mount | Celestron AUX |
| Connection | Serial |
| Port | `/dev/ttyACM0` (verify with `ls /dev/ttyACM*`) |
| Baud | 115200 |
| Alignment | StarSense (if equipped) or Manual |
| Parking | Enabled — set park position after first successful session |

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
starwatch status

# From Mac (after Pi hostname resolves)
curl http://starwatch-pi.local:8787/health
```