from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Notification

class NotificationObserver(ABC):

    @abstractmethod
    def update(self, notification: Notification) -> None:
        pass