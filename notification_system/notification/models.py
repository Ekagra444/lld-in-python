from dataclasses import dataclass, field
from uuid import UUID, uuid4

from .enums import ChannelType, NotificationStatus
from .observer.observer import NotificationObserver


@dataclass
class Notification:
    sender: UUID
    receiver: UUID
    message: str
    channel_type: ChannelType

    id: UUID = field(default_factory=uuid4)
    status: NotificationStatus = NotificationStatus.PENDING
    attempts: int = 0

    _observers: list[NotificationObserver] = field(
        default_factory=list,
        repr=False,
    )

    def add_observer(self, observer: NotificationObserver) -> None:
        self._observers.append(observer)

    def set_status(self, status: NotificationStatus) -> None:
        self.status = status

        for observer in self._observers:
            observer.update(self)