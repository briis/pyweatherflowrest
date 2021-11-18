"""Helper Class for Weatherflow Rest module."""
from __future__ import annotations

import datetime as dt
import logging
import math

from pyweatherflowrest.const import UNIT_TYPE_METRIC
from pyweatherflowrest.data import BeaufortDescription

UTC = dt.timezone.utc

_LOGGER = logging.getLogger(__name__)

class Conversions:
    """Converts values from metric."""
    def __init__(self, units: str, homeassistant: bool) -> None:
        self.units = units
        self.homeassistant = homeassistant

    def temperature(self, value) -> float:
        """Returns celcius to Fahrenheit."""
        if value is None or self.units == UNIT_TYPE_METRIC or self.homeassistant:
            return value
        return round(value * 1.8 + 32, 1)

    def pressure(self, value) -> float:
        """Returns inHg from mb/hPa."""
        if value is None or self.units == UNIT_TYPE_METRIC:
            return value
        return round(value * 0.029530, 1)

    def rain(self, value) -> float:
        """Converts rain units."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value, 2)
        return round(value * 0.03937007874, 2)

    def rain_rate(self, value) -> float:
        """Calculates Rain Rate."""
        if value is None:
            return None

        _rain_rate = value * 60

        return self.rain(_rain_rate)

    def density(self, value) -> float:
        """Converts air density."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value, 1)

        return round(value * 0.06243, 1)

    def distance(self, value) -> float:
        """Conerts km to mi."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value,1)

        return round(value * 0.6213688756, 1)
        
    def windspeed(self, value, wind_unit_kmh: bool = False) -> float:
        """Returns miles per hour from m/s."""
        if value is None:
            return value
        
        if self.units == UNIT_TYPE_METRIC:
            if wind_unit_kmh:
                return round(value * 3.6, 1)
            return round(value, 1)

        return round(value * 2.236936292, 1)

    def utc_from_timestamp(self, timestamp: int) -> dt.datetime:
        """Return a UTC time from a timestamp."""
        return dt.datetime.utcfromtimestamp(timestamp).replace(tzinfo=UTC)

class Calculations:
    """Calculate entity values."""

    def is_raining(self, rain):
        """Returns true if it is raining."""
        if rain is None:
            return None
            
        rain_rate = rain * 60
        return rain_rate > 0

    def is_freezing(self, temperature):
        """Returns true if temperature below 0."""
        if temperature is None:
            return None
            
        return temperature < 0

    def day_forecast_extras(self, day_data, hour_data) -> float:
        """Returns accumulated precip for the day."""
        _precip = 0
        _wind_avg =[]
        _wind_bearing=[]

        for item in hour_data:
            if item["local_day"] == day_data["day_num"]:
                _precip += item["precip"]
                _wind_avg.append(item["wind_avg"])
                _wind_bearing.append(item["wind_direction"])
        
        _sum_wind_avg = sum(_wind_avg) / len(_wind_avg)
        _sum_wind_bearing = sum(_wind_bearing) / len(_wind_bearing)

        return {"precip": round(_precip, 1), "wind_avg": round(_sum_wind_avg, 1), "wind_direction": int(_sum_wind_bearing)}

    def visibility(self, elevation, air_temperature, relative_humidity, dewpoint) -> float:
        """Returns the calculated visibility."""

        if elevation is None or air_temperature is None or relative_humidity is None or dewpoint is None:
            return None

        elevation_min = float(2)
        if elevation > 2:
            elevation_min = float(elevation)

        max_visibility = float(3.56972 * math.sqrt(elevation_min))
        percent_reduction_a = float((1.13 * abs(air_temperature - dewpoint) - 1.15) /10)
        if percent_reduction_a > 1:
            percent_reduction = float(1)
        elif percent_reduction_a < 0.025:
            percent_reduction = float(0.025)
        else:
            percent_reduction = percent_reduction_a
        
        visibility_km = float(max_visibility * percent_reduction)

        return visibility_km

    def absolute_humidity(self, air_temperature, relative_humidity) -> float:
        """Returns calculated absolute humidity."""

        if air_temperature is None or relative_humidity is None:
            return None

        temperature_kelvin = air_temperature + 273.16
        humidity = relative_humidity / 100
        abs_humidity = (1320.65 / temperature_kelvin) * humidity * (10 ** ((7.4475 * (temperature_kelvin - 273.14)) / (temperature_kelvin - 39.44)))

        return round(abs_humidity, 2)

    def battery_percent(self, is_tempest: bool, voltage: float) -> int:
        """Returns battery percentage from voltage."""

        if is_tempest is None or voltage is None:
            return None

        if is_tempest:
            if voltage > 2.80:
                bat_percent = 100
            elif voltage < 1.8:
                bat_percent = 0
            else:
                bat_percent = (voltage - 1.8) * 100
        else:
            if voltage > 3.50:
                bat_percent = 100
            elif voltage < 2.4:
                bat_percent = 0
            else:
                bat_percent = ((voltage - 2.4) / 1.1) * 100

        return int(bat_percent)

    def uv_description(self, uv: float) -> str:
        """Returns a Description based on uv value."""
        if uv is None:
            return None

        if uv >= 10.5:
            return "extreme"
        if uv >= 7.5:
            return "very-high"
        if uv >= 5.5:
            return "high"
        if uv >= 2.5:
            return "moderate"
        if uv > 0:
            return "low"

        return "none"

    def wind_direction(self, wind_bearing: int) -> str:
        """Returns a Wind Directions String from Wind Bearing."""
        if wind_bearing is None:
            return None

        direction_array = [
            "n",
            "nne",
            "ne",
            "ene",
            "e",
            "ese",
            "se",
            "sse",
            "s",
            "ssw",
            "sw",
            "wsw",
            "w",
            "wnw",
            "nw",
            "nnw",
            "n",
        ]
        return direction_array[int((wind_bearing + 11.25) / 22.5)]     

    def beaufort(self, wind_speed: float) -> BeaufortDescription:
        """Retruns data structure with Beaufort values."""
        if wind_speed is None:
            return None

        if wind_speed > 32.7:
            bft = BeaufortDescription(
                value=12,
                description="hurricane"
            )
        elif wind_speed >= 28.5:
            bft = BeaufortDescription(
                value=11,
                description="violent_storm"
            )
        elif wind_speed >= 24.5:
            bft = BeaufortDescription(
                value=10,
                description="storm"
            )
        elif wind_speed >= 20.8:
            bft = BeaufortDescription(
                value=9,
                description="strong_gale"
            )
        elif wind_speed >= 17.2:
            bft = BeaufortDescription(
                value=8,
                description="fresh_gale"
            )
        elif wind_speed >= 13.9:
            bft = BeaufortDescription(
                value=7,
                description="moderate_gale"
            )
        elif wind_speed >= 10.8:
            bft = BeaufortDescription(
                value=6,
                description="strong_breeze"
            )
        elif wind_speed >= 8.0:
            bft = BeaufortDescription(
                value=5,
                description="fresh_breeze"
            )
        elif wind_speed >= 5.5:
            bft = BeaufortDescription(
                value=4,
                description="moderate_breeze"
            )
        elif wind_speed >= 3.4:
            bft = BeaufortDescription(
                value=3,
                description="gentle_breeze"
            )
        elif wind_speed >= 1.6:
            bft = BeaufortDescription(
                value=2,
                description="light_breeze"
            )
        elif wind_speed >= 0.3:
            bft = BeaufortDescription(
                value=1,
                description="light_air"
            )
        else:
            bft = BeaufortDescription(
                value=0,
                description="calm"
            )

        return bft

    def precip_intensity(self, precip: float) -> str:
        """Returns text string with WeatherFlow Precip Intensity."""

        if precip is None:
            return None

        rain_rate = precip * 60

        if rain_rate == 0:
            intensity = "none"
        elif rain_rate < 0.25:
            intensity = "very_light"
        elif rain_rate < 1:
            intensity = "light"
        elif rain_rate < 4:
            intensity = "moderate"
        elif rain_rate < 16:
            intensity = "heavy"
        elif rain_rate < 50:
            intensity = "very_heavy"
        else:
            intensity = "extreme"

        return intensity
