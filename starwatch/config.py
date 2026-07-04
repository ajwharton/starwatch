"""Configuration loading for Starwatch."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class IndiConfig(BaseModel):
    host: str = "localhost"
    port: int = 7624
    device_name: str = "Celestron AUX"


class TelescopeConfig(BaseModel):
    model: str = "NexStar Evolution 9.25"
    connection: Literal["usb", "wifi"] = "usb"
    slew_rate: Literal["slow", "medium", "fast"] = "medium"


class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8787
    api_key: str | None = None


class StarwatchConfig(BaseModel):
    indi: IndiConfig = Field(default_factory=IndiConfig)
    telescope: TelescopeConfig = Field(default_factory=TelescopeConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)
    mode: Literal["mock", "indi"] = "mock"


class Settings(BaseSettings):
    """Environment-variable overrides (prefix STARWATCH_)."""

    model_config = SettingsConfigDict(env_prefix="STARWATCH_", env_nested_delimiter="__")

    indi_host: str = "localhost"
    indi_port: int = 7624
    indi_device: str = "Celestron AUX"
    mode: Literal["mock", "indi"] = "mock"
    server_host: str = "0.0.0.0"
    server_port: int = 8787
    api_key: str | None = None


def load_config(path: Path | str | None = None) -> StarwatchConfig:
    """Load YAML config, falling back to defaults."""
    if path is None:
        path = Path("config/starwatch.yaml")
    else:
        path = Path(path)

    if not path.exists():
        return StarwatchConfig()

    with path.open() as f:
        data = yaml.safe_load(f) or {}

    return StarwatchConfig.model_validate(data)


def settings_to_config(settings: Settings) -> StarwatchConfig:
    """Merge environment settings into a StarwatchConfig."""
    return StarwatchConfig(
        mode=settings.mode,
        indi=IndiConfig(
            host=settings.indi_host,
            port=settings.indi_port,
            device_name=settings.indi_device,
        ),
        server=ServerConfig(
            host=settings.server_host,
            port=settings.server_port,
            api_key=settings.api_key,
        ),
    )