"""System Wide Constants for pyweatherflowrestapi"""

DEVICE_TYPE_TEMPEST = "tempest"
DEVICE_TYPE_AIR = "air"
DEVICE_TYPE_SKY="sky"
DEVICE_TYPE_HUB = "hub"

WEATHERFLOW_BASE_URL = "https://swd.weatherflow.com/swd/rest"
WEATHERFLOW_DEVICE_BASE_URL = f"{WEATHERFLOW_BASE_URL}/observations/device/"
WEATHERFLOW_FORECAST_BASE_URL = f"{WEATHERFLOW_BASE_URL}/better_forecast?station_id="
WEATHERFLOW_OBSERVATION_BASE_URL = f"{WEATHERFLOW_BASE_URL}/observations/station/"
WEATHERFLOW_STATIONS_BASE_URL = f"{WEATHERFLOW_BASE_URL}/stations/"
