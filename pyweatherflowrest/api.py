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
from pyweatherflowrest.data import ObservationDescription
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

    async def update_observations(self) -> None:
        """Update observation data"""

        data = await self.api_request(self.observation_url)
        if data is not None:
            obervations = data['obs'][0]
            entity_data = ObservationDescription(
                key=self.station_id,
                timestamp=obervations["timestamp"],
                air_temperature=obervations["air_temperature"]
            )

        return entity_data

    async def api_request(
        self,
        url: str
        ) -> None:
        """Get data from WeatherFlow API"""

        async with self.req.get(url) as resp:
            data = await resp.json()
            return data

