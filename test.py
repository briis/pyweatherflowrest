"""Demo Program."""
import asyncio
import logging
import time

from pyweatherflowrest.api import WeatherFlowApiClient
from pyweatherflowrest.data import ObservationDescription, StationDescription, ForecastDescription, ForecastDailyDescription
from pyweatherflowrest.exceptions import WrongStationID, Invalid, NotAuthorized, BadRequest

_LOGGER = logging.getLogger(__name__)

async def main() -> None:
    """Start the demo program."""
    logging.basicConfig(level=logging.DEBUG)
    start = time.time()

    weatherflow = WeatherFlowApiClient(
        34094,
        "20c70eae-e62f-4d3b-b3a4-8586e90f3ac8",
        units="metric",
        homeassistant=True,
        forecast_hours=240,
        ignore_fetch_errors=True
    )

    try:
        await weatherflow.initialize()

    except WrongStationID as err:
        _LOGGER.debug(err)
    except Invalid as err:
        _LOGGER.debug(err)
    except NotAuthorized as err:
        _LOGGER.debug(err)
    except BadRequest as err:
        _LOGGER.debug(err)

    # data = await weatherflow.load_unit_system()
    # print(data)

    # data: StationDescription = weatherflow.station_data
    # if data is not None:
    #     for field in data.__dataclass_fields__:
    #         value = getattr(data, field)
    #         print(field,"-", value)

    # try:
    #     data: ObservationDescription = await weatherflow.update_observations()
    #     if data is not None:
    #         for field in data.__dataclass_fields__:
    #             value = getattr(data, field)
    #             print(field, "-", value)
    # except WrongStationID as err:
    #     _LOGGER.debug(err)
    # except Invalid as err:
    #     _LOGGER.debug(err)
    # except NotAuthorized as err:
    #     _LOGGER.debug(err)
    # except BadRequest as err:
    #     _LOGGER.debug(err)

    try:
        data: ForecastDescription = await weatherflow.update_forecast()
        if data is not None:
            for field in data.__dataclass_fields__:
                value = getattr(data, field)
                if field == "forecast_daily":
                    # continue
                    for item in value:
                        print(
                            item.utc_time,
                            item.icon,
                            "Temp High: ",
                            item.air_temp_high,
                            "Temp Low: ",
                            item.air_temp_low,
                            item.precip, item.wind_avg,
                            item.wind_direction
                        )
                elif field == "forecast_hourly":
                    cnt = 1
                    for item in value:
                        print(cnt, item.icon, item.utc_time, item.air_temperature, item.feels_like)
                        cnt += 1
                else:
                    print(field, "-", value)
    except WrongStationID as err:
        _LOGGER.debug(err)
    except Invalid as err:
        _LOGGER.debug(err)
    except NotAuthorized as err:
        _LOGGER.debug(err)
    except BadRequest as err:
        _LOGGER.debug(err)

    end = time.time()

    await weatherflow.req.close()

    _LOGGER.info("Execution time: %s seconds", end - start)

asyncio.run(main())
