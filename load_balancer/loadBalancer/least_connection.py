from threading import Lock
from typing import Sequence

from .server import Server
from .routing_strategy import RoutingStrategy


class LeastConnectionStrategy(RoutingStrategy):

    def __init__(self) -> None:
        self._active_connections: dict[Server, int] = {}
        self._lock = Lock()

    def select_server(
        self,
        servers: Sequence[Server],
    ) -> Server:

        if not servers:
            raise ValueError("No servers available")

        with self._lock:
            server =  min(
                servers,
                key=lambda server: self._active_connections.get(
                    server,
                    0,
                ),
            )
        self._increment(server)
        return server
    
    def _increment(self, server):
        self._active_connections[server] = (
            self._active_connections.get(server, 0) + 1
        )

    def on_request_finished(
        self,
        server: Server,
    ) -> None:

        with self._lock:
            current_connections = self._active_connections.get(
                server,
                0,
            )

            if current_connections == 0:
                return

            self._active_connections[server] = (
                current_connections - 1
            )