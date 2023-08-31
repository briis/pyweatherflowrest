# Change Log

This document will contain a list of all major changes.

## [1.0.11] - 2023-08-31

- Made changes, so that Fetch Errors are ignored by default. Currently this is only done for the Hourly Forecast, but will be implemented across all records.
- With the above changes, it is now also possible to toggle this from the Integration. Requires 1.0.16 od the Integration.

## [1.0.10] - 2023-08-30

    - Implemented PR #3 done by @UpDryTwist which address removal of sea_level_pressure and uv from hourly forecasts


## [1.0.9] - 2023-02-11

- Changing density units to conform with standard Home Assistant units

## [1.0.8] - 2022-01-27

### Fixed

- In rare occasions the forecast icon is not present in data supplied from WeatherFlow. Will now be set to *Cloudy* as default.

## [1.0.7] - 2022-01-02

### Changed

- Changed error description when we could not get data from WeatherFlow, to something that better reflects the error.


## [1.0.6] - 2022-01-02

### Changed

- Reverted Lightning time to DateTime object.

## [1.0.5] - 2022-01-02

### Changed

- `utc_time` is now returned as a string instead of a DateTime object, as this is what Home Assistant expects.


## [1.0.3] - 2021-12-30

### Fixed

- Previous fix worked for Imperial users, but then broke it for Metric users. Is now working for both unit systems.

## [1.0.2] - 2021-12-29

### Fixed

- Feels Like forecast temperature had wrong value when displayed with Imperial Units.

## [1.0.1] - 2021-12-28

### Added

- Altitude unit added to dictionary.


## [1.0.0] - 2021-12-26

After a lot of testing I believe we are now at a point where this module will be called 1.0.0 as it is stable and delivers as expected.

### Added

- New data point *freezing_line*. It holds the altitude above sea level where snow is possible in meters or feet, depending on unit system.
- New data point *cloud_base*. It holds the cloud height altitude above sea level in meters or feet, depending on unit system.

## [0.1.23] - 2021-12-22

### Changed

- Added better error handling, when no data is returned from WeatherFlow

## [0.1.22] - 2021-12-21

### Fixed

- Fixed error when Device List did not contain a `devie_type` which would stop the system from loading any data.


## [0.1.21] - 2021-12-18

### Added

- Add possibility to specify how many hours of the the Hourly Forecast data should be returned.


## [0.1.20] - 2021-12-16

### Added

- New sensor data points `precip_accum_local_day_final`, `precip_accum_local_yesterday_final`, `precip_minutes_local_yesterday_final`. These values will only appear for stations located in the US, as they are depended on *Rain Check* and that only works in the US.


## [0.1.19] - 2021-12-15

### Added

- New sensor data point `station_name`. Will be used as a sensor in Home Assistant with the Station Data attached as Attributes.

### Changed

- Limited the number of items in the Hourly Forecast array to 48, as the default of 240 items, was creating warnings in Home Assistant.
- Restructured the StationDescription dataclass so that all attached physical devices are added as a list to the class.

## [0.1.18] - 2021-12-14

### Changes

- Better error handling if empty dataset returned from oberservations.


## [0.1.17] - 2021-12-09

### Changes

- UV Index values are now rounded to 1 decimal.

### Added

- Added battery mode and battery mode description. This only applies to Tempest devices.

## [0.1.16] - 2021-12-09

### Changes

- Air Density values are now round to 5 decimals.


## [0.1.15] - 2021-12-07

### Changes

- Pressure values are now round to 3 decimals, when using Imperial unit system.

### Fixed

- Added missing density conversion
- If no wind_avg values present, the beaufort conversion function would fail. Now it will return empty values.

