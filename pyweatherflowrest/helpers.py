"""Helper Class for Weatherflow Rest module."""
from __future__ import annotations

import datetime
import pytz

from pyweatherflowrest.const import UNIT_TYPE_METRIC

UTC = pytz.utc

class Conversions:
    """Converts values from metric."""
    def __init__(self, units: str, homeassistant: bool) -> None:
        self.units = units
        self.homeassistant = homeassistant

    async def temperature(self, value) -> float:
        """Returns celcius to Fahrenheit."""
        if value is None or self.units == UNIT_TYPE_METRIC or self.homeassistant:
            return value
        return round(value * 1.8 + 32, 1)

    async def pressure(self, value) -> float:
        """Returns inHg from mb/hPa."""
        if value is None or self.units == UNIT_TYPE_METRIC:
            return value
        return round(value * 0.029530, 1)

    async def rain(self, value) -> float:
        """Converts rain units."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value, 2)
        return round(value * 0.03937007874, 2)

    async def rain_rate(self, value) -> float:
        """Calculates Rain Rate."""
        if value is None:
            return None

        _rain_rate = value * 60

        return await self.rain(_rain_rate)

    async def density(self, value) -> float:
        """Converts air density."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value, 1)

        return round(value * 0.06243, 1)

    async def distance(self, value) -> float:
        """Conerts km to mi."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value,1)

        return round(value * 0.6213688756, 1)
        
    async def windspeed(self, value, wind_unit_kmh: bool = False) -> float:
        """Returns miles per hour from m/s."""
        if value is None:
            return value
        
        if self.units == UNIT_TYPE_METRIC:
            if wind_unit_kmh:
                return round(value * 3.6, 1)
            return round(value, 1)

        return round(value * 2.236936292, 1)

    async def utc_from_timestamp(self, timestamp: int) -> datetime.datetime:
        """Return a UTC time from a timestamp."""
        return UTC.localize(datetime.datetime.utcfromtimestamp(timestamp))

class Calculations:
    """Calculate entity values."""

    async def is_raining(self, rain):
        """Returns true if it is raining."""
        if rain is None:
            return None
            
        rain_rate = rain * 60
        return rain_rate > 0

    async def is_freezing(self, temperature):
        """Returns true if temperature below 0."""
        if temperature is None:
            return None
            
        return temperature < 0

    async def day_forecast_extras(self, day_data, hour_data) -> float:
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