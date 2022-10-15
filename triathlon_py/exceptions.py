class TriathlonAPIBaseException(Exception):
    """Base exception for all Triathlon API exceptions."""

    pass

class TriathlonAPIException(TriathlonAPIBaseException):
    """Exception for Triathlon API errors."""

    pass

class TriathlonAPIHTTPException(TriathlonAPIBaseException):
    """Exception for Triathlon API HTTP errors."""

    pass

class TriathlonAPIRateLimitException(TriathlonAPIBaseException):
    """Exception for Triathlon API rate limit errors."""

    pass

class TriathlonAPIAuthenticationException(TriathlonAPIBaseException):
    """Exception for Triathlon API authentication errors."""

    pass

class TriathlonAPIAuthorizationException(TriathlonAPIBaseException):
    """Exception for Triathlon API authorization errors."""

    pass

class TriathlonAPIRequestException(TriathlonAPIBaseException):
    """Exception for Triathlon API request errors."""

    pass