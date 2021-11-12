"""Dataclasses for pyweatherflowrest"""
from dataclasses import dataclass

@dataclass
class ObservationDescription:
    """A class that describes Obervation entities."""

    """This is the Key identifier for this entity"""
    key: str

    timestamp: int | None = None
    air_temperature: float | None = None
    barometric_pressure: float | None = None
    station_pressure: float | None = None
    sea_level_pressure: float | None = None
    relative_humidity: int | None = None
    precip: float | None = None
    precip_accum_last_1hr: float | None = None
    precip_accum_local_day: float | None = None
    precip_accum_local_yesterday: float | None = None
    precip_minutes_local_day: int | None = None
    precip_minutes_local_yesterday: int | None = None
    wind_avg: float | None = None
    wind_direction: int | None = None
    wind_gust: float | None = None
    wind_lull: float | None = None
    solar_radiation: float | None = None
    uv: float | None = None
    brightness: int | None = None
    lightning_strike_last_epoch: int | None = None
    lightning_strike_last_distance: int | None = None
    lightning_strike_count: int | None = None
    lightning_strike_count_last_1hr: int | None = None
    lightning_strike_count_last_3hr: int | None = None
    feels_like: float | None = None
    heat_index: float | None = None
    wind_chill: float | None = None
    dew_point: float | None = None
    wet_bulb_temperature: float | None = None
    delta_t: float | None = None
    air_density: float | None = None
    pressure_trend: str | None = None
    