from ..models import Notification
from ..senders.email import EmailSender
from .base import NotificationChannel


class EmailChannel(NotificationChannel):

    def __init__(
        self,
        worker_count: int,
        queue_size: int,
        max_attempts: int,
    ):
        super().__init__(
            sender=EmailSender(),
            worker_count=worker_count,
            queue_size=queue_size,
            max_attempts=max_attempts,
        )

    def send(self, notification: Notification) -> None:
        self._sender.send(notification)