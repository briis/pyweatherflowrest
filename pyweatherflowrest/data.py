"""Dataclasses for pyweatherflowrest."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ObservationDescription:
    """A class that describes Obervation entities."""

    """This is the Key identifier for this entity"""
    key: int

    utc_time: str | None = None
    air_temperature: float | None = None
    barometric_pressure: float | None = None
    station_pressure: float | None = None
    sea_level_pressure: float | None = None
    relative_humidity: int | None = None
    absolute_humidity: int | None = None
    precip: float | None = None
    precip_rate: float | None = None
    precip_intensity: str | None = None
    precip_accum_last_1hr: float | None = None
    precip_accum_local_day: float | None = None
    precip_accum_local_day_final: float | None = None
    precip_accum_local_yesterday: float | None = None
    precip_accum_local_yesterday_final: float | None = None
    precip_minutes_local_day: int | None = None
    precip_minutes_local_yesterday: int | None = None
    precip_minutes_local_yesterday_final: int | None = None
    wind_avg: float | None = None
    wind_direction: int | None = None
    wind_cardinal: str | None = None
    wind_gust: float | None = None
    wind_lull: float | None = None
    wind_avg_kmh: float | None = None
    wind_gust_kmh: float | None = None
    wind_lull_kmh: float | None = None
    wind_avg_knots: float | None = None
    wind_gust_knots: float | None = None
    wind_lull_knots: float | None = None
    beaufort: int | None = None
    beaufort_description: str | None = None
    solar_radiation: float | None = None
    uv: float | None = None
    uv_description: str | None = None
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
    visibility: float | None = None
    pressure_trend: str | None = None
    voltage_air: float | None = None
    battery_air: float | None = None
    voltage_sky: float | None = None
    battery_sky: float | None = None
    voltage_tempest: float | None = None
    battery_tempest: float | None = None
    battery_mode: float | None = None
    battery_mode_description: str | None = None
    is_freezing: bool | None = None
    is_raining: bool | None = None
    is_lightning: bool | None = None
    station_name: str | None = None


@dataclass
class StationDescription:
    """A class that describes Station entities."""

    """This is the Key identifier for this entity"""
    key: int

    name: str | None = None
    public_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    timezone: str | None = None
    elevation: int | None = None
    is_tempest: bool | None = False
    hub_device_id: int | None = None
    hub_device_type: str | None = None
    hub_hardware_revision: int | None = None
    hub_firmware_revision: int | None = None
    hub_serial_number: int | None = None
    device_list: list[DeviceDescription] = field(default_factory=list)

@dataclass
class DeviceDescription:
    """Class describing a Physical Device."""
    device_id: int
    name: str | None = None
    device_type: str | None = None
    hardware_revision: int | None = None
    firmware_revision: int | None = None
    serial_number: int | None = None

@dataclass
class ForecastDailyDescription:
    """A class that describes Daily Forecast entities."""

    utc_time: int | None = None
    conditions: str | None = None
    icon: str | None = None
    sunrise: int | None = None
    sunset: int | None = None
    air_temp_high: float | None = None
    air_temp_low: float | None = None
    precip: float | None = None
    precip_probability: int | None = None
    wind_avg: float | None = None
    wind_direction: int | None = None

@dataclass
class ForecastHourlyDescription:
    """A class that describes Hourly Forecast entities."""

    utc_time: int | None = None
    conditions: str | None = None
    icon: str | None = None
    air_temperature: float | None = None
    sea_level_pressure: float | None = None
    relative_humidity: int | None = None
    precip: float | None = None
    precip_probability: int | None = None
    wind_avg: float | None = None
    wind_direction: int | None = None
    wind_direction_cardinal: str | None = None
    wind_gust: float | None = None
    uv: float | None = None
    feels_like: float | None = None

@dataclass
class ForecastDescription:
    """A class that describes Forecast entities."""

    """This is the Key identifier for this entity"""
    key: int

    utc_time: int | None = None
    conditions: str | None = None
    icon: str | None = None
    air_temperature: float | None = None
    temp_high_today: float | None = None
    temp_low_today: float | None = None
    station_pressure: float | None = None
    sea_level_pressure: float | None = None
    pressure_trend: str | None = None
    relative_humidity: int | None = None
    wind_avg: float | None = None
    wind_direction: int | None = None
    wind_direction_cardinal: str | None = None
    wind_gust: float | None = None
    solar_radiation: float | None = None
    uv: float | None = None
    brightness: int | None = None
    feels_like: float | None = None
    dew_point: float | None = None
    wet_bulb_temperature: float | None = None
    delta_t: float | None = None
    air_density: float | None = None
    lightning_strike_count_last_1hr: int | None = None
    lightning_strike_count_last_3hr: int | None = None
    lightning_strike_last_distance: int | None = None
    lightning_strike_last_distance_msg: str | None = None
    lightning_strike_last_epoch: int | None = None
    precip_accum_local_day: float | None = None
    precip_accum_local_yesterday: float | None = None
    precip_minutes_local_day: int | None = None
    precip_minutes_local_yesterday: int | None = None
    forecast_daily: list[ForecastDailyDescription] = field(default_factory=list)
    forecast_hourly: list[ForecastHourlyDescription] = field(default_factory=list)

@dataclass
class BeaufortDescription:
    """A class that describes beaufort values."""

    value: int
    description: str
