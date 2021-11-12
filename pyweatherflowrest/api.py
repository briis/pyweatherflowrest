"""WeatherFlow Data Wrapper."""
from __future__ import annotations

import asyncio
import aiohttp
from aiohttp import client_exceptions
import json as pjson
import logging
from typing import Optional, List, Union, Dict, Any

from pyweatherflowrest.const import (
    WEATHERFLOW_FORECAST_BASE_URL,
    WEATHERFLOW_OBSERVATION_BASE_URL,
)
from pyweatherflowrest.data import ObservationDescription, StationDescription
from pyweatherflowrest.exceptions import BadRequest, NotAuthorized, ApiError

_LOGGER = logging.getLogger(__name__)

class WeatherFlowApiClient:

    req: aiohttp.ClientSession

    def __init__ (
        self,
        station_id: int,
        api_token: str,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        self.station_id = station_id
        self.api_token = api_token

        if session is None:
            session = aiohttp.ClientSession()

        self.req = session

    @property
    def observation_url(self) -> str:
        """Base Rest Url for observation data"""
        return f"{WEATHERFLOW_OBSERVATION_BASE_URL}{self.station_id}?token={self.api_token}"

    @property
    def forecast_url(self) -> str:
        """Base Rest Url for forecast Data"""
        return f"{WEATHERFLOW_FORECAST_BASE_URL}{self.station_id}&token={self.api_token}"

    async def read_station_data(self) -> None:
        """Update observation data"""

        data = await self.api_request(self.observation_url)
        if data is not None:

            units = data['station_units']
            entity_data = StationDescription(
                key=self.station_id,
                station_name=data["station_name"],
                public_name=data["public_name"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                timezone=data["timezone"],
                elevation=data["elevation"],
                units_temp=units["units_temp"],
                units_wind=units["units_wind"],
                units_precip=units["units_precip"],
                units_pressure=units["units_pressure"],
                units_distance=units["units_distance"],
                units_direction=units["units_direction"],
                units_other=units["units_other"],
            )

            return entity_data

        return None


    async def update_observations(self) -> None:
        """Update observation data"""

        data = await self.api_request(self.observation_url)
        if data is not None:
            obervations = data['obs'][0]
            entity_data = ObservationDescription(
                key=self.station_id,
                timestamp=obervations["timestamp"],
                air_temperature=obervations["air_temperature"],
                barometric_pressure=obervations["barometric_pressure"],
                station_pressure=obervations["station_pressure"],
                sea_level_pressure=obervations["sea_level_pressure"],
                relative_humidity=obervations["relative_humidity"],
                precip=obervations["precip"],
                precip_accum_last_1hr=obervations["precip_accum_last_1hr"],
                precip_accum_local_day=obervations["precip_accum_local_day"],
                precip_accum_local_yesterday=obervations["precip_accum_local_yesterday"],
                precip_minutes_local_day=obervations["precip_minutes_local_day"],
                precip_minutes_local_yesterday=obervations["precip_minutes_local_yesterday"],
                wind_avg=obervations["wind_avg"],
                wind_direction=obervations["wind_direction"],
                wind_gust=obervations["wind_gust"],
                wind_lull=obervations["wind_lull"],
                solar_radiation=obervations["solar_radiation"],
                uv=obervations["uv"],
                brightness=obervations["brightness"],
                lightning_strike_last_epoch=obervations["lightning_strike_last_epoch"],
                lightning_strike_last_distance=obervations["lightning_strike_last_distance"],
                lightning_strike_count=obervations["lightning_strike_count"],
                lightning_strike_count_last_1hr=obervations["lightning_strike_count_last_1hr"],
                lightning_strike_count_last_3hr=obervations["lightning_strike_count_last_3hr"],
                feels_like=obervations["feels_like"],
                heat_index=obervations["heat_index"],
                wind_chill=obervations["wind_chill"],
                dew_point=obervations["dew_point"],
                wet_bulb_temperature=obervations["wet_bulb_temperature"],
                delta_t=obervations["delta_t"],
                air_density=obervations["air_density"],
                pressure_trend=obervations["pressure_trend"],
            )

            return entity_data

        return None

    async def api_request(
        self,
        url: str
        ) -> None:
        """Get data from WeatherFlow API"""

        try:
            async with self.req.get(url) as resp:
                data = await resp.json()
                return data

        except client_exceptions.ClientError as err:
            raise ApiError(f"Error requesting data from WeatherFlow: {err}") from None
