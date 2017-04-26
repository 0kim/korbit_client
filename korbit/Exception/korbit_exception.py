
## status code: 400 or 401
class AuthException(Exception):
    pass

## status code: 500
class ServiceUnavailableException(Exception):
    pass