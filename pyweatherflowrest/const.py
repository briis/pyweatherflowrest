"""System Wide Constants for pyweatherflowrestapi."""
from __future__ import annotations

BATTERY_MODE_DESCRIPTION = [
    "All sensors enabled and operating at full performance. Wind sampling interval every 3 seconds",
    "Wind sampling interval set to 6 seconds",
    "Wind sampling interval set to one minute",
    "Wind sampling interval set to 5 minutes. All other sensors sampling interval set to 5 minutes. Haptic Rain sensor disabled from active listening",
]

DEVICE_TYPE_TEMPEST = "tempest"
DEVICE_TYPE_AIR = "air"
DEVICE_TYPE_SKY = "sky"
DEVICE_TYPE_HUB = "hub"

UNIT_TYPE_METRIC = "metric"
UNIT_TYPE_IMPERIAL = "imperial"
VALID_UNIT_TYPES = [UNIT_TYPE_IMPERIAL, UNIT_TYPE_METRIC]

WEATHERFLOW_BASE_URL = "https://swd.weatherflow.com/swd/rest"
WEATHERFLOW_DEVICE_BASE_URL = f"{WEATHERFLOW_BASE_URL}/observations/device/"
WEATHERFLOW_FORECAST_BASE_URL = f"{WEATHERFLOW_BASE_URL}/better_forecast?station_id="
WEATHERFLOW_OBSERVATION_BASE_URL = f"{WEATHERFLOW_BASE_URL}/observations/station/"
WEATHERFLOW_STATIONS_BASE_URL = f"{WEATHERFLOW_BASE_URL}/stations/"
