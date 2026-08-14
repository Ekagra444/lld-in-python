from ..models import Notification
from ..senders.sms import SMSSender
from .base import NotificationChannel


class SMSChannel(NotificationChannel):

    def __init__(
        self,
        worker_count: int,
        queue_size: int,
        max_attempts: int,
    ):
        super().__init__(
            sender=SMSSender(),
            worker_count=worker_count,
            queue_size=queue_size,
            max_attempts=max_attempts,
        )

    def send(self, notification: Notification) -> None:
        self._sender.send(notification)