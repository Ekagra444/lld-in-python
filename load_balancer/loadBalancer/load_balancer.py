from __future__ import annotations

from threading import Lock

from .routing_strategy import RoutingStrategy
from .server import Server, ServerStatus
from .exceptions import NoHealthyServersException
from .request_context import RequestContext

class LoadBalancer:
    def __init__(
        self,
        strategy: RoutingStrategy,
    ) -> None:
        self._strategy = strategy
        self._servers: list[Server] = []
        self._lock = Lock()

    def register_server(
        self,
        server: Server,
    ) -> None:
        with self._lock:
            self._servers.append(server)

    def remove_server(
        self,
        server_id: str,
    ) -> None:
        with self._lock:
            self._servers = [
                server
                for server in self._servers
                if server.server_id != server_id
            ]

    def update_strategy(
        self,
        strategy: RoutingStrategy,
    ) -> None:
        self._strategy = strategy

    def _begin_request(self) -> Server:

        with self._lock:
            available_servers = tuple(
                server
                for server in self._servers
                if server.status == ServerStatus.HEALTHY
            )

        if not available_servers:
            raise NoHealthyServersException()

        server =  self._strategy.select_server(
            available_servers
        )

        # self._strategy.on_request_started(server) we have to make reserve server atomic and therefore call increament logic from within select server itself
        
        return server

    def _complete_request(self,server:Server):
        self._strategy.on_request_finished(server)

    def request(self)->RequestContext:
        server = self._begin_request()
        return RequestContext(self,server)