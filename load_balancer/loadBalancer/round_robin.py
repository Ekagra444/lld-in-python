from __future__ import annotations

from collections.abc import Sequence
from threading import Lock

from .routing_strategy import RoutingStrategy
from .server import Server


class RoundRobinStrategy(RoutingStrategy):
    def __init__(self) -> None:
        self._current_index = 0
        self._lock = Lock()

    def select_server(
        self,
        servers: Sequence[Server],
    ) -> Server:

        with self._lock:
            size = len(servers)
            
            server = servers[self._current_index % size]

            self._current_index = (
                self._current_index + 1
            ) 

            return server