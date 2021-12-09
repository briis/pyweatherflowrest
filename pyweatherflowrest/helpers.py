"""Helper Class for Weatherflow Rest module."""
from __future__ import annotations

import datetime as dt
import logging
import math

from pyweatherflowrest.const import BATTERY_MODE_DESCRIPTION, UNIT_TYPE_METRIC
from pyweatherflowrest.data import BeaufortDescription

UTC = dt.timezone.utc

_LOGGER = logging.getLogger(__name__)

class Conversions:
    """Convert values from metric."""

    def __init__(self, units: str, homeassistant: bool) -> None:
        """Conversion Functions."""
        self.units = units
        self.homeassistant = homeassistant

    def temperature(self, value) -> float:
        """Return celcius to Fahrenheit."""
        if value is None or self.units == UNIT_TYPE_METRIC or self.homeassistant:
            return value
        return round(value * 1.8 + 32, 1)

    def pressure(self, value) -> float:
        """Return inHg from mb/hPa."""
        if value is None or self.units == UNIT_TYPE_METRIC:
            return value
        return round(value * 0.029530, 3)

    def rain(self, value) -> float:
        """Convert rain units."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value, 2)
        return round(value * 0.03937007874, 2)

    def rain_rate(self, value) -> float:
        """Calculate Rain Rate."""
        if value is None:
            return None

        _rain_rate = value * 60

        return self.rain(_rain_rate)

    def density(self, value) -> float:
        """Convert air density."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value, 5)

        return round(value * 0.06243, 5)

    def distance(self, value) -> float:
        """Conerts km to mi."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value, 1)

        return round(value * 0.6213688756, 1)

    def windspeed(self, value, wind_unit_kmh: bool = False) -> float:
        """Return miles per hour from m/s."""
        if value is None:
            return value

        if self.units == UNIT_TYPE_METRIC:
            if wind_unit_kmh:
                return round(value * 3.6, 1)
            return round(value, 1)

        return round(value * 2.236936292, 1)

    def windspeed_knots(self, value: float) -> float:
        """Return knots from m/s."""
        if value is None:
            return value

        return round(value * 1.943844, 1)

    def windspeed_kmh(self, value: float) -> float:
        """Return km/h from m/s."""
        if value is None:
            return value

        return round(value * 3.6, 1)

    def utc_from_timestamp(self, timestamp: int) -> dt.datetime:
        """Return a UTC time from a timestamp."""
        if timestamp is None:
            return None
        return dt.datetime.utcfromtimestamp(timestamp).replace(tzinfo=UTC)

    def uv_index(self, uvi: float) -> float:
        """Return rounded UV Index."""
        if uvi is None:
            return None
        return round(uvi, 1)
        


class Calculations:
    """Calculate entity values."""

    def is_raining(self, rain):
        """Return true if it is raining."""
        if rain is None:
            return None

        rain_rate = rain * 60
        return rain_rate > 0

    def is_freezing(self, temperature):
        """Return true if temperature below 0."""
        if temperature is None:
            return None
        return temperature < 0

    def is_lightning(self, count):
        """Return true if Lightning Count larger than 0."""
        if count is None:
            return False
        return count > 0

    def day_forecast_extras(self, day_data, hour_data) -> float:
        """Return accumulated precip for the day."""
        _precip = 0
        _wind_avg = []
        _wind_bearing = []

        for item in hour_data:
            if item["local_day"] == day_data["day_num"]:
                _precip += item["precip"]
                _wind_avg.append(item["wind_avg"])
                _wind_bearing.append(item["wind_direction"])

        _sum_wind_avg = sum(_wind_avg) / len(_wind_avg)
        _sum_wind_bearing = sum(_wind_bearing) / len(_wind_bearing)

        return {
            "precip": round(_precip, 1),
            "wind_avg": round(_sum_wind_avg, 1),
            "wind_direction": int(_sum_wind_bearing)
        }

    def visibility(self, elevation, air_temperature, relative_humidity, dewpoint) -> float:
        """Return the calculated visibility."""
        if elevation is None or air_temperature is None or relative_humidity is None or dewpoint is None:
            return None

        elevation_min = float(2)
        if elevation > 2:
            elevation_min = float(elevation)

        max_visibility = float(3.56972 * math.sqrt(elevation_min))
        percent_reduction_a = float((1.13 * abs(air_temperature - dewpoint) - 1.15) / 10)
        if percent_reduction_a > 1:
            percent_reduction = float(1)
        elif percent_reduction_a < 0.025:
            percent_reduction = float(0.025)
        else:
            percent_reduction = percent_reduction_a
        visibility_km = float(max_visibility * percent_reduction)

        return visibility_km

    def absolute_humidity(self, air_temperature, relative_humidity) -> float:
        """Return calculated absolute humidity."""
        if air_temperature is None or relative_humidity is None:
            return None

        temperature_kelvin = air_temperature + 273.16
        humidity = relative_humidity / 100
        abs_humidity = (1320.65 / temperature_kelvin) * humidity * (10 ** ((7.4475 * (temperature_kelvin - 273.14)) / (temperature_kelvin - 39.44)))

        return round(abs_humidity, 2)

    def battery_percent(self, is_tempest: bool, voltage: float) -> int:
        """Return battery percentage from voltage."""
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
        """Return a Description based on uv value."""
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
        """Return a Wind Directions String from Wind Bearing."""
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

    def beaufort_value(self, wind_speed: float) -> BeaufortDescription:
        """Return Beaufort Value and Description."""
        if wind_speed is None:
            return BeaufortDescription(value=0, description="None")

        mapping_text = {
            "32.7": [12, "hurricane"],
            "28.5": [11, "violent_storm"],
            "24.5": [10, "storm"],
            "20.8": [9, "strong_gale"],
            "17.2": [8, "fresh_gale"],
            "13.9": [7, "moderate_gale"],
            "10.8": [6, "strong_breeze"],
            "8.0": [5, "fresh_breeze"],
            "5.5": [4, "moderate_breeze"],
            "3.4": [3, "gentle_breeze"],
            "1.6": [2, "light_breeze"],
            "0.3": [1, "light_air"],
            "-1": [0, "calm"],
        }
        for k, v in mapping_text.items():
            if wind_speed > float(k):
                return BeaufortDescription(value=v[0], description=v[1])
        return None

    def precip_intensity(self, precip: float) -> str:
        """Return text string with WeatherFlow Precip Intensity."""
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

    def battery_mode(self, voltage, solar_radiation):
        """Return battery operating mode.

        Input:
            Voltage in Volts DC (depends on the weather station type, see below)
            is_tempest in Boolean
            solar_radiation in W/M^2 (used to determine if battery is in a charging state)
        Tempest:
            # data["battery_level"] = cnv.battery_mode(obs[16], True, obs[11])
            # https://help.weatherflow.com/hc/en-us/articles/360048877194-Solar-Power-Rechargeable-Battery
        AIR & SKY:
            The battery mode does not apply to AIR & SKY Units
        """
        if voltage is None or solar_radiation is None:
            return None

        if voltage >= 2.455:
            # Mode 0 (independent of charging or discharging at this voltage)
            batt_mode = int(0)
        elif voltage <= 2.355:
            # Mode 3 (independent of charging or discharging at this voltage)
            batt_mode = int(3)
        elif solar_radiation > 100:
            # Assume charging and voltage is raising
            if voltage >= 2.41:
                # Mode 1
                batt_mode = int(1)
            elif voltage > 2.375:
                # Mode 2
                batt_mode = int(2)
            else:
                # Mode 3
                batt_mode = int(3)
        else:
            # Assume discharging and voltage is lowering
            if voltage > 2.415:
                # Mode 0
                batt_mode = int(0)
            elif voltage > 2.39:
                # Mode 1
                batt_mode = int(1)
            elif voltage > 2.355:
                # Mode 2
                batt_mode = int(2)
            else:
                # Mode 3
                batt_mode = int(3)

        mode_description = BATTERY_MODE_DESCRIPTION[batt_mode]
        return batt_mode, mode_description
