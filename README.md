# Python Wrapper for WeatherFlow REST API

![Latest PyPI version](https://img.shields.io/pypi/v/pyweatherflowrest) ![Supported Python](https://img.shields.io/pypi/pyversions/pyweatherflowrest)

This module communicates with a WeatherFlow Weather Station using a [their REST API](https://weatherflow.github.io/Tempest/api/swagger/#/).

The module is primarily written for the purpose of being used in Home Assistant for the Custom Integration called [`weatherflow`](https://github.com/briis/hass-weatherflow) but might be used for other purposes also.

When this is done, it will replace the previous module [`pysmartweatherio`](https://github.com/briis/pysmartweatherio)

## Install

`pyweatherflowrest` is avaible on PyPi:

```bash
pip install pyweatherflowrest
```

## Usage

This library is primarily designed to be used in an async context.

The main interface for the library is the `pyweatherflowrest.WeatherFlowApiClient`. This interface takes 6 options:

* `station_id`: (required) Supply the station id for the station you want data for.
* `api_token`: (required) Enter your personal api token for the above station id. You can get your *Personal Use Token* [by going here](https://tempestwx.com/settings/tokens) and login with your credentials. Then click CREATE TOKEN in the upper right corner.
* `units`: (optional) Valid options here are *metric* or *imperial*. WeatherFlow stations always deliver data in metric units, so conversion will only take place if if metric is not selected. Default value is **metric**
* `forecast_hours`: (optional) Specify how many hours of the *Hourly Forecast* that needs to be retrieved. Values between 1 and 240 are valid. Default value is **48** hours.
* `homeassistant`: (optional) Valid options are *True* or *False*. If set to True, there will be some unit types that will not be converted, as Home Assistant will take care of that. Default value is **False**
* `session`: (optional) An existing *aiohttp.ClientSession*. Default value is **None**, and then a new ClientSession will be created.

```python
import asyncio
import logging
import time

from pyweatherflowrest.api import WeatherFlowApiClient
from pyweatherflowrest.data import ObservationDescription, StationDescription, ForecastDescription, ForecastDailyDescription
from pyweatherflowrest.exceptions import WrongStationID, Invalid, NotAuthorized, BadRequest

_LOGGER = logging.getLogger(__name__)

async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    start = time.time()

    weatherflow = WeatherFlowApiClient("YOUR STATION ID", "YOUR TOKEN")
    try:
        await weatherflow.initialize() # Must be the first call

    except WrongStationID as err:
        _LOGGER.debug(err)
    except Invalid as err:
        _LOGGER.debug(err)
    except NotAuthorized as err:
        _LOGGER.debug(err)
    except BadRequest as err:
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


    data: ForecastDescription = await weatherflow.update_forecast()
    if data is not None:
        for field in data.__dataclass_fields__:
            value = getattr(data, field)
            if field == "forecast_daily":
                for item in value:
                    print(item.conditions, item.air_temp_high)
            elif field == "forecast_hourly":
                for item in value:
                    print(item.conditions, item.air_temperature)
            else:
                print(field,"-", value)

    end = time.time()

    await weatherflow.req.close()

    _LOGGER.info("Execution time: %s seconds", end - start)

asyncio.run(main())

```
