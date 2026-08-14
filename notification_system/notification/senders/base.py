from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Notification


class DeliveryError(Exception):
    pass


class NotificationSender(ABC):

    @abstractmethod
    def send(self, notification: Notification) -> None:
        pass