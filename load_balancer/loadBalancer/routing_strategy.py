from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from .server import Server


class RoutingStrategy(ABC):

    @abstractmethod
    def select_server(
        self,
        servers: Sequence[Server],
    ) -> Server:
        """Select the next server."""
        raise NotImplementedError

    def on_request_started(
        self,
        server: Server,
    ) -> None:
        """Lifecycle hook."""
        pass

    def on_request_finished(
        self,
        server: Server,
    ) -> None:
        """Lifecycle hook."""
        pass