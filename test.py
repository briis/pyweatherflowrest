import asyncio
import logging
import time

from pyweatherflowrest.api import WeatherFlowApiClient
from pyweatherflowrest.data import ObservationDescription, StationDescription
from pyweatherflowrest.exceptions import WrongStationID, ApiError, Invalid

_LOGGER = logging.getLogger(__name__)

async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    start = time.time()

    weatherflow = WeatherFlowApiClient(51146, "20c70eae-e62f-4d3b-b3a4-8586e90f3ac8")
    try:
        await weatherflow.initialize()

    except WrongStationID as err:
        _LOGGER.debug(err)
    except ApiError as err:
        _LOGGER.debug(err)
    except Invalid as err:
        _LOGGER.debug(err)

    data: StationDescription = weatherflow.station_data
    if data is not None:
        for field in data.__dataclass_fields__:
            value = getattr(data, field)
            print(field,"-", value)

    data: ObservationDescription = await weatherflow.update_observations()
    if data is not None:
        for field in data.__dataclass_fields__:
            value = getattr(data, field)
            print(field,"-", value)

    end = time.time()

    await weatherflow.req.close()

    _LOGGER.info("Execution time: %s seconds", end - start)

asyncio.run(main())
