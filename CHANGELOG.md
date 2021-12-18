# Change Log

This document will contain a list of all major changes.

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

