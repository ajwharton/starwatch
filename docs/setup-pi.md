# Pi Setup Guide

Run when your Pi 5 kit arrives. Reply "ready for setup" for step-by-step first-boot help.

## 1. Assemble Hardware

1. Install Crucial P310 2230 onto NVMe HAT
2. Mount Pi 5 + HAT in GeeekPi case, attach active cooler
3. Connect 27W USB-C PD power

## 2. Flash StellarMate OS

Preferred: [StellarMate OS](https://stellarmate.com/) — KStars/Ekos + INDI pre-installed.

```bash
# On Mac — download image, flash to NVMe via USB adapter
# Enable SSH on first boot (wpa_supplicant or Ethernet)
```

Alternative: Ubuntu 24.04 LTS + manual INDI install.

## 3. First Boot

```bash
ssh pi@stellarmate.local   # or your hostname
sudo raspi-config          # enable NVMe boot if needed
```

## 4. Install Starwatch

```bash
git clone https://github.com/ajwharton/starwatch.git
cd starwatch
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[indi]"
cp .env.example .env
# Edit: STARWATCH_MODE=indi, STARWATCH_API_KEY=<random>
```

## 5. Systemd Service

```ini
# /etc/systemd/system/starwatch.service
[Unit]
Description=Starwatch telescope API
After=network.target indiserver.service
Wants=indiserver.service

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/starwatch
EnvironmentFile=/home/pi/starwatch/.env
ExecStart=/home/pi/starwatch/.venv/bin/starwatch-server
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now starwatch
```

## 6. Firewall

```bash
sudo ufw allow from 192.168.0.0/16 to any port 8787
sudo ufw allow from 192.168.0.0/16 to any port 7624
```

## 7. Verify from Mac

```bash
curl http://stellarmate.local:8787/health
curl -H "X-API-Key: your-key" http://stellarmate.local:8787/status
```