"""Agent-callable tools — JSON schemas + HTTP client for remote Pi."""

from __future__ import annotations

from typing import Any

import httpx

# OpenAI/Grok-compatible function tool schemas for agent orchestration.
AGENT_TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "telescope_status",
            "description": "Get current Celestron telescope status: position, tracking, parked state.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "telescope_slew",
            "description": (
                "Slew the backyard telescope to a target. "
                "Use catalog names (M31, M42, M45) or explicit coordinates."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Object name (e.g. M31) or RA in hours",
                    },
                    "dec": {
                        "type": "string",
                        "description": "Declination in degrees (required if target is RA)",
                    },
                },
                "required": ["target"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "telescope_track",
            "description": "Enable or disable sidereal tracking on the telescope.",
            "parameters": {
                "type": "object",
                "properties": {
                    "enabled": {
                        "type": "boolean",
                        "description": "True to enable tracking, false to disable",
                    },
                },
                "required": ["enabled"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "telescope_park",
            "description": "Park the telescope in its home position (end of session).",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "telescope_unpark",
            "description": "Unpark the telescope to begin observing.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "telescope_abort",
            "description": "Abort the current slew immediately.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
]


class StarwatchAgentClient:
    """HTTP client agents use to control the Pi-hosted Starwatch server."""

    def __init__(
        self,
        base_url: str = "http://starwatch-pi.local:8787",
        api_key: str | None = None,
        timeout: float = 30.0,
        client: httpx.Client | object | None = None,
    ) -> None:
        if client is not None:
            self._client = client
            self._owns_client = False
        else:
            headers = {}
            if api_key:
                headers["X-API-Key"] = api_key
            self._client = httpx.Client(base_url=base_url, headers=headers, timeout=timeout)
            self._owns_client = True

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> StarwatchAgentClient:
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def dispatch(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Route an agent tool call to the appropriate API endpoint."""
        handlers = {
            "telescope_status": lambda _: self.status(),
            "telescope_slew": self._slew,
            "telescope_track": self._track,
            "telescope_park": lambda _: self._post("/park"),
            "telescope_unpark": lambda _: self._post("/unpark"),
            "telescope_abort": lambda _: self._post("/abort"),
        }
        handler = handlers.get(tool_name)
        if handler is None:
            raise ValueError(f"Unknown tool: {tool_name}")
        return handler(arguments)

    def status(self) -> dict[str, Any]:
        r = self._client.get("/status")
        r.raise_for_status()
        return r.json()

    def _slew(self, args: dict[str, Any]) -> dict[str, Any]:
        payload: dict[str, Any] = {"target": args["target"]}
        if "dec" in args:
            payload["dec"] = args["dec"]
        r = self._client.post("/slew", json=payload)
        r.raise_for_status()
        return r.json()

    def _track(self, args: dict[str, Any]) -> dict[str, Any]:
        mode = "sidereal" if args.get("enabled", True) else "off"
        r = self._client.post("/tracking", json={"mode": mode})
        r.raise_for_status()
        return r.json()

    def _post(self, path: str) -> dict[str, Any]:
        r = self._client.post(path)
        r.raise_for_status()
        return r.json()