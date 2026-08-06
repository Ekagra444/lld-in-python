from __future__ import annotations

from threading import Lock
from collections.abc import Sequence

from .routing_strategy import RoutingStrategy
from .server import Server


class WeightedRoundRobinStrategy(RoutingStrategy):
    def __init__(self) -> None:
        self._current_weights: dict[Server, int] = {}
        self._lock = Lock()

    def select_server(
        self,
        servers: Sequence[Server],
    ) -> Server:
        if not servers:
            raise ValueError("No servers available.")

        with self._lock:
            # Remove stale entries for servers that no longer exist.
            live_servers = set(servers)
            for server in list(self._current_weights):
                if server not in live_servers:
                    del self._current_weights[server]

            total_weight = 0
            selected_server: Server | None = None
            selected_weight = float("-inf")

            for server in servers:
                current_weight = (
                    self._current_weights.get(server, 0)
                    + server._weight
                )
                self._current_weights[server] = current_weight

                total_weight += server._weight

                if current_weight > selected_weight:
                    selected_server = server
                    selected_weight = current_weight

            assert selected_server is not None

            self._current_weights[selected_server] -= total_weight

            return selected_server

    