"""Dataclasses for pyweatherflowrest"""
from dataclasses import dataclass

@dataclass
class ObservationDescription:
    """A class that describes Obervation entities."""

    """This is the Key identifier for this entity"""
    key: str

    timestamp: int | None = None
    air_temperature: float | None = None
    