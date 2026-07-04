"""FastAPI application exposing telescope control to agents."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

from starwatch.config import Settings, load_config, settings_to_config
from starwatch.factory import create_client
from starwatch.telescope.controller import TelescopeController, TrackingMode

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


class SlewRequest(BaseModel):
    target: str = Field(..., description="Catalog name (e.g. M31) or object id")
    dec: str | float | None = Field(None, description="DEC if target is RA")


class CoordsRequest(BaseModel):
    ra: str | float
    dec: str | float


class TrackingRequest(BaseModel):
    mode: TrackingMode = TrackingMode.SIDEREAL


class StatusResponse(BaseModel):
    connected: bool
    slew_state: str
    ra_hours: float | None
    dec_degrees: float | None
    tracking: bool
    parked: bool
    device: str
    message: str | None


class ActionResponse(BaseModel):
    ok: bool
    message: str
    ra_hours: float | None = None
    dec_degrees: float | None = None


_controller: TelescopeController | None = None
_settings: Settings | None = None


def get_controller() -> TelescopeController:
    if _controller is None:
        raise HTTPException(503, "Server not initialized")
    return _controller


def get_settings() -> Settings:
    if _settings is None:
        raise HTTPException(503, "Server not initialized")
    return _settings


def _verify_api_key(
    api_key: Annotated[str | None, Security(_api_key_header)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> None:
    if settings.api_key and api_key != settings.api_key:
        raise HTTPException(401, "Invalid or missing API key")


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _controller, _settings
    _settings = Settings()
    config = load_config()
    env_config = settings_to_config(_settings)
    # Environment overrides file config
    config.mode = env_config.mode
    config.indi = env_config.indi
    config.server = env_config.server

    client = create_client(config)
    _controller = TelescopeController(client)
    _controller.connect()
    yield
    _controller.disconnect()
    _controller = None


app = FastAPI(
    title="Starwatch",
    description="Agentic Celestron telescope control API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "starwatch"}


@app.get("/status", response_model=StatusResponse, dependencies=[Depends(_verify_api_key)])
def status(ctrl: Annotated[TelescopeController, Depends(get_controller)]) -> StatusResponse:
    state = ctrl.get_state()
    s = state.status
    return StatusResponse(
        connected=ctrl.client.is_connected(),
        slew_state=s.slew.value,
        ra_hours=s.ra_hours,
        dec_degrees=s.dec_degrees,
        tracking=s.tracking,
        parked=s.parked,
        device=s.device_name,
        message=s.message,
    )


@app.post("/slew", response_model=ActionResponse, dependencies=[Depends(_verify_api_key)])
def slew(
    req: SlewRequest,
    ctrl: Annotated[TelescopeController, Depends(get_controller)],
) -> ActionResponse:
    try:
        coord = ctrl.slew_to_target(req.target, req.dec)
        return ActionResponse(
            ok=True,
            message=f"Slewing to {req.target}",
            ra_hours=coord.ra_hours,
            dec_degrees=coord.dec_degrees,
        )
    except (RuntimeError, ValueError) as e:
        raise HTTPException(400, str(e)) from e


@app.post("/slew/coords", response_model=ActionResponse, dependencies=[Depends(_verify_api_key)])
def slew_coords(
    req: CoordsRequest,
    ctrl: Annotated[TelescopeController, Depends(get_controller)],
) -> ActionResponse:
    try:
        coord = ctrl.slew_to_coords(req.ra, req.dec)
        return ActionResponse(
            ok=True,
            message="Slewing to coordinates",
            ra_hours=coord.ra_hours,
            dec_degrees=coord.dec_degrees,
        )
    except (RuntimeError, ValueError) as e:
        raise HTTPException(400, str(e)) from e


@app.post("/tracking", response_model=ActionResponse, dependencies=[Depends(_verify_api_key)])
def tracking(
    req: TrackingRequest,
    ctrl: Annotated[TelescopeController, Depends(get_controller)],
) -> ActionResponse:
    ctrl.set_tracking(req.mode)
    return ActionResponse(ok=True, message=f"Tracking set to {req.mode.value}")


@app.post("/park", response_model=ActionResponse, dependencies=[Depends(_verify_api_key)])
def park(ctrl: Annotated[TelescopeController, Depends(get_controller)]) -> ActionResponse:
    ctrl.park()
    return ActionResponse(ok=True, message="Parking telescope")


@app.post("/unpark", response_model=ActionResponse, dependencies=[Depends(_verify_api_key)])
def unpark(ctrl: Annotated[TelescopeController, Depends(get_controller)]) -> ActionResponse:
    ctrl.unpark()
    return ActionResponse(ok=True, message="Unparking telescope")


@app.post("/abort", response_model=ActionResponse, dependencies=[Depends(_verify_api_key)])
def abort(ctrl: Annotated[TelescopeController, Depends(get_controller)]) -> ActionResponse:
    ctrl.abort()
    return ActionResponse(ok=True, message="Slew aborted")


def run() -> None:
    """Entry point for starwatch-server console script."""
    settings = Settings()
    uvicorn.run(
        "starwatch.server.app:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=False,
    )