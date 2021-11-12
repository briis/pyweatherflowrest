"""System Wide Constants for pyweatherflowrestapi"""

WEATHERFLOW_BASE_URL = "https://swd.weatherflow.com/swd/rest"
WEATHERFLOW_DEVICE_BASE_URL = f"{WEATHERFLOW_BASE_URL}/observations/device/"
WEATHERFLOW_FORECAST_BASE_URL = f"{WEATHERFLOW_BASE_URL}/better_forecast?station_id="
WEATHERFLOW_OBSERVATION_BASE_URL = f"{WEATHERFLOW_BASE_URL}/observations/station/"
WEATHERFLOW_STATIONS_BASE_URL = f"{WEATHERFLOW_BASE_URL}/stations/"
