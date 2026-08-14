from __future__ import annotations

from queue import Queue
from threading import Thread

from ..enums import NotificationStatus
from ..models import Notification
from ..senders.base import DeliveryError, NotificationSender


class Worker:

    def __init__(
        self,
        queue: Queue[Notification],
        sender: NotificationSender,
        max_attempts: int,
    ):
        self._queue = queue
        self._sender = sender
        self._max_attempts = max_attempts

    def run(self) -> None:
        while True:
            notification = self._queue.get()

            try:
                notification.set_status(NotificationStatus.PROCESSING)
                notification.attempts += 1

                self._sender.send(notification)

                notification.set_status(NotificationStatus.SENT)

            except DeliveryError:
                if notification.attempts < self._max_attempts:
                    notification.set_status(NotificationStatus.PENDING)
                    self._queue.put(notification)
                else:
                    notification.set_status(NotificationStatus.FAILED)

            finally:
                self._queue.task_done()