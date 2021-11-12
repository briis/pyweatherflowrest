"""WeatherFlow Data Wrapper."""
from __future__ import annotations

import asyncio
import aiohttp
from aiohttp import client_exceptions
import json as pjson
import logging
from typing import Optional

from pyweatherflowrest.const import (
    WEATHERFLOW_DEVICE_BASE_URL,
    WEATHERFLOW_FORECAST_BASE_URL,
    WEATHERFLOW_OBSERVATION_BASE_URL,
    WEATHERFLOW_STATIONS_BASE_URL,
)
from pyweatherflowrest.data import ObservationDescription, StationDescription
from pyweatherflowrest.exceptions import  Invalid,  BadRequest, WrongStationID, NotAuthorized

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

        self._station_data: StationDescription = None
        self._observation_data: ObservationDescription = None
        self._device_id = None

    @property
    def station_data(self) -> StationDescription:
        """Returns Station Data."""
        return self._station_data

    @property
    def device_url(self) -> str:
        """Rest Url for device data."""
        return f"{WEATHERFLOW_DEVICE_BASE_URL}{self._device_id}?token={self.api_token}"

    @property
    def observation_url(self) -> str:
        """Rest Url for observation data."""
        return f"{WEATHERFLOW_OBSERVATION_BASE_URL}{self.station_id}?token={self.api_token}"

    @property
    def forecast_url(self) -> str:
        """Rest Url for forecast Data."""
        return f"{WEATHERFLOW_FORECAST_BASE_URL}{self.station_id}&token={self.api_token}"

    @property
    def station_url(self) -> str:
        """Base Rest Url for station Data"""
        return f"{WEATHERFLOW_STATIONS_BASE_URL}{self.station_id}?token={self.api_token}"

    async def initialize(self) -> None:
        """Initialize data tables."""

        data = await self._api_request(self.station_url)

        if data is not None:
            if data["status"]["status_code"] == 404:
                raise WrongStationID(f"Station ID {self.station_id} does not exist") from None
            if data["status"]["status_code"] == 401:
                raise NotAuthorized(f"Token {self.api_token} is invalid") from None
            if data["stations"] == []:
                raise Invalid(f"The data returned from Station ID {self.station_id} is invalid") from None

            station = data["stations"][0]
            entity_data = StationDescription(
                key=self.station_id,
                name=station["name"],
                public_name=station["public_name"],
                latitude=station["latitude"],
                longitude=station["longitude"],
                timezone=station["timezone"],
                elevation=station["station_meta"]["elevation"],
            )
            for device in station["devices"]:
                if device["device_type"] == "HB":
                    entity_data.hub_device_id = device["device_id"]
                    entity_data.hub_hardware_revision = device["hardware_revision"]
                    entity_data.hub_firmware_revision = device["firmware_revision"]
                    entity_data.hub_serial_number = device["serial_number"]
                if device["device_type"] == "ST":
                    entity_data.tempest_device_id = device["device_id"]
                    entity_data.tempest_hardware_revision = device["hardware_revision"]
                    entity_data.tempest_firmware_revision = device["firmware_revision"]
                    entity_data.tempest_serial_number = device["serial_number"]
                    entity_data.is_tempest = True
                if device["device_type"] == "AR":
                    entity_data.air_device_id = device["device_id"]
                    entity_data.air_hardware_revision = device["hardware_revision"]
                    entity_data.air_firmware_revision = device["firmware_revision"]
                    entity_data.air_serial_number = device["serial_number"]
                if device["device_type"] == "SK":
                    entity_data.sky_device_id = device["device_id"]
                    entity_data.sky_hardware_revision = device["hardware_revision"]
                    entity_data.sky_firmware_revision = device["firmware_revision"]
                    entity_data.sky_serial_number = device["serial_number"]

            self._station_data = entity_data


    async def _read_device_data(self) -> None:
        """Update observation data."""

        if self._station_data.is_tempest:
            self._device_id = self._station_data.tempest_device_id
            voltage_index = 16
            data = await self._api_request(self.device_url)
            if data is not None:
                device = data["obs"][0]
                self._observation_data.voltage_tempest = device[voltage_index]
        else:
            self._device_id = self._station_data.air_device_id
            voltage_index = 6
            data = await self._api_request(self.device_url)
            if data is not None:
                device = data["obs"][0]
                self._observation_data.voltage_air = device[voltage_index]

            self._device_id = self._station_data.sky_device_id
            voltage_index = 8
            data = await self._api_request(self.device_url)
            if data is not None:
                device = data["obs"][0]
                self._observation_data.voltage_sky = device[voltage_index]


    async def update_observations(self) -> None:
        """Update observation data."""
        if self._station_data is None:
            return

        data = await self._api_request(self.observation_url)
        if data is not None:
            obervations = data['obs'][0]
            units = data['station_units']
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
                units_temp=units["units_temp"],
                units_wind=units["units_wind"],
                units_precip=units["units_precip"],
                units_pressure=units["units_pressure"],
                units_distance=units["units_distance"],
                units_direction=units["units_direction"],
                units_other=units["units_other"],
            )
            self._observation_data = entity_data
            await self._read_device_data()

            return entity_data

        return None

    async def _api_request(
        self,
        url: str
        ) -> None:
        """Get data from WeatherFlow API."""

        try:
            async with self.req.get(url) as resp:
                data = await resp.json()
                return data

        except client_exceptions.ClientError as err:
            raise BadRequest(f"Error requesting data from WeatherFlow: {err}") from None
