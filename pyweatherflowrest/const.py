"""System Wide Constants for pyweatherflowrestapi"""
from __future__ import annotations

from pyweatherflowrest.data import ConversionDescription

DEVICE_TYPE_TEMPEST = "tempest"
DEVICE_TYPE_AIR = "air"
DEVICE_TYPE_SKY="sky"
DEVICE_TYPE_HUB = "hub"

FIELDS_PRESSURRE = ["station_pressure", "sea_level_pressure"]
FIELDS_WIND = ["wind_avg", "wind_gust", "wind_lull"]

UNIT_TYPE_METRIC = "metric"
UNIT_TYPE_IMPERIAL = "imperial"
VALID_UNIT_TYPES = [UNIT_TYPE_IMPERIAL, UNIT_TYPE_METRIC]

WEATHERFLOW_BASE_URL = "https://swd.weatherflow.com/swd/rest"
WEATHERFLOW_DEVICE_BASE_URL = f"{WEATHERFLOW_BASE_URL}/observations/device/"
WEATHERFLOW_FORECAST_BASE_URL = f"{WEATHERFLOW_BASE_URL}/better_forecast?station_id="
WEATHERFLOW_OBSERVATION_BASE_URL = f"{WEATHERFLOW_BASE_URL}/observations/station/"
WEATHERFLOW_STATIONS_BASE_URL = f"{WEATHERFLOW_BASE_URL}/stations/"

CONVERSION_DATA = ConversionDescription = (
    ConversionDescription(
        field_type=FIELDS_WIND,
        function="wind_speed_imperial",
    ),
    ConversionDescription(
        field_type=FIELDS_PRESSURRE,
        function="pressure_imperial",
    ),
)
