"""Exception handling for WeatherFlow Rest."""
class WeatherFlowError(Exception):
    """Base class for all other WeatherFlow errors."""


class ClientError(WeatherFlowError):
    """Base Class for all other Unifi Protect client errors."""


class BadRequest(ClientError):
    """Invalid request from API Client."""


class Invalid(ClientError):
    """Invalid return from Authorization Request."""


class NotAuthorized(ClientError):
    """Wrong API Token."""


class WrongStationID(ClientError):
    """Station ID does not exist."""
