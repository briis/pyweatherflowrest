# Python Wrapper for WeatherFlow REST API

[![Latest PyPI version](https://img.shields.io/pypi/v/pyweatherflowrest
)](https://pypi.org/project/pyweatherflowrest
/) [![Supported Python](https://img.shields.io/pypi/pyversions/pyweatherflowrest
)](https://pypi.org/project/pyweatherflowrest
/)

This module communicates with a WeatherFlow Weather Station using a [their REST API](https://weatherflow.github.io/Tempest/api/swagger/#/).

The module is primarily written for the purpose of being used in Home Assistant for the Custom Integration called `smartweather` but might be used for other purposes also.

When this is done, it will replace the previous module [`pysmartweatherio`](https://github.com/briis/pysmartweatherio)

## Install

`pyweatherflowrest` is avaible on PyPi:

```bash
pip install pyweatherflowrest
```

## Usage

This library is primarily designed to be used in an async context.

The main interface for the library is the `pyweatherflowrest.WeatherFlowApiClient`:

```python
from pyweatherflowrest import WeatherFlowApiClient
from pyweatherflowrest.data import ObservationDescription, StationDescription, ForecastDescription, ForecastDailyDescription
from pyweatherflowrest.exceptions import WrongStationID, Invalid, NotAuthorized, BadRequest

weatherflow = WeatherFlowApiClient(station_id, token)

   try:
        await weatherflow.initialize() # this will initalize the connection to weatherflow and load needed data for further queries.

    except WrongStationID as err:
        _LOGGER.debug(err)
    except Invalid as err:
        _LOGGER.debug(err)
    except NotAuthorized as err:
        _LOGGER.debug(err)
    except BadRequest as err:
        _LOGGER.debug(err)

# get station information
data: StationDescription = weatherflow.station_data
if data is not None:
    for field in data.__dataclass_fields__:
        value = getattr(data, field)
        print(field,"-", value)

# get forecast data
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


# get current condition data
data: ObservationDescription = await weatherflow.update_observations()
if data is not None:
    for field in data.__dataclass_fields__:
        value = getattr(data, field)
        print(field,"-", value)

```
