from __future__ import annotations

from typing import TYPE_CHECKING

from .server import Server

if TYPE_CHECKING:
    from load_balancer import LoadBalancer


class RequestContext:
    def __init__(
        self,
        load_balancer: LoadBalancer,
        server: Server,
    ) -> None:
        self._load_balancer = load_balancer
        self._server = server

    def __enter__(self) -> Server:
        return self._server

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._load_balancer._complete_request(self._server)