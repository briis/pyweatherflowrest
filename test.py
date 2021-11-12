import asyncio
import logging
import time

from pyweatherflowrest.api import WeatherFlowApiClient
from pyweatherflowrest.data import ObservationDescription

_LOGGER = logging.getLogger(__name__)

async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    start = time.time()

    weatherflow = WeatherFlowApiClient(51146, "4e168eb2-b84f-4014-bc1b-b4317976f283")

    data: ObservationDescription = await weatherflow.update_observations()
    for field in data.__dataclass_fields__:
        value = getattr(data, field)
        print(field, value)
    # print(data.air_temperature)

    end = time.time()

    await weatherflow.req.close()

    _LOGGER.info("Execution time: %s seconds", end - start)

asyncio.run(main())
