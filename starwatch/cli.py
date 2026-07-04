"""Command-line interface for quick telescope operations."""

from __future__ import annotations

import argparse
import json
import sys

from starwatch.config import load_config
from starwatch.factory import create_client
from starwatch.telescope.controller import TelescopeController, TrackingMode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Starwatch telescope CLI")
    parser.add_argument("--config", default="config/starwatch.yaml", help="Config file path")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Show telescope status")
    sub.add_parser("connect", help="Connect to INDI server")
    sub.add_parser("disconnect", help="Disconnect from INDI server")

    slew_p = sub.add_parser("slew", help="Slew to target")
    slew_p.add_argument("target", help="Catalog name or RA")
    slew_p.add_argument("--dec", help="Declination (if target is RA)")

    track_p = sub.add_parser("track", help="Set tracking mode")
    track_p.add_argument("mode", choices=["on", "off"], help="Tracking on/off")

    sub.add_parser("park", help="Park telescope")
    sub.add_parser("unpark", help="Unpark telescope")
    sub.add_parser("abort", help="Abort slew")

    args = parser.parse_args(argv)
    config = load_config(args.config)
    client = create_client(config)
    ctrl = TelescopeController(client)

    try:
        if args.command == "connect":
            ok = ctrl.connect()
            print("Connected" if ok else "Connection failed")
            return 0 if ok else 1

        if args.command == "disconnect":
            ctrl.disconnect()
            print("Disconnected")
            return 0

        # All other commands require connection
        if not ctrl.connect():
            print("Failed to connect to INDI server", file=sys.stderr)
            return 1

        if args.command == "status":
            state = ctrl.get_state()
            print(json.dumps(_status_dict(state), indent=2))
        elif args.command == "slew":
            coord = ctrl.slew_to_target(args.target, args.dec)
            print(f"Slewing to RA={coord.ra_hours:.4f} DEC={coord.dec_degrees:.4f}")
        elif args.command == "track":
            mode = TrackingMode.SIDEREAL if args.mode == "on" else TrackingMode.OFF
            ctrl.set_tracking(mode)
            print(f"Tracking {args.mode}")
        elif args.command == "park":
            ctrl.park()
            print("Parking")
        elif args.command == "unpark":
            ctrl.unpark()
            print("Unparked")
        elif args.command == "abort":
            ctrl.abort()
            print("Aborted")

        return 0
    finally:
        ctrl.disconnect()


def _status_dict(state) -> dict:
    s = state.status
    return {
        "connected": s.connection.value,
        "slew": s.slew.value,
        "ra_hours": s.ra_hours,
        "dec_degrees": s.dec_degrees,
        "tracking": s.tracking,
        "parked": s.parked,
        "device": s.device_name,
        "message": s.message,
    }


if __name__ == "__main__":
    raise SystemExit(main())