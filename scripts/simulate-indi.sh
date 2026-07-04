#!/usr/bin/env bash
# Start INDI simulator for local testing (requires INDI installed).
set -euo pipefail

if ! command -v indiserver &>/dev/null; then
  echo "indiserver not found. Install INDI or use mock mode (STARWATCH_MODE=mock)."
  exit 1
fi

echo "Starting INDI simulator on port 7624..."
indiserver -v indi_simulator_telescope