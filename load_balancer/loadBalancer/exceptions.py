class NoHealthyServersException(Exception):
    """Raised when no healthy servers are available."""
    pass


class DuplicateServerException(Exception):
    """Raised when a server with the same ID is already registered."""
    pass


class ServerNotFoundException(Exception):
    """Raised when attempting to remove a non-existent server."""
    pass