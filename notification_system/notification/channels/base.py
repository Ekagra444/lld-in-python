from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from threading import Thread

from ..models import Notification
from ..senders.base import NotificationSender
from ..workers.worker import Worker


class NotificationChannel(ABC):

    def __init__(
        self,
        sender: NotificationSender,
        worker_count: int,
        queue_size: int,
        max_attempts: int,
    ):
        self._queue: Queue[Notification] = Queue(
            maxsize=queue_size
        )

        self._sender = sender
        self._max_attempts = max_attempts
        self._workers: list[Thread] = []

        self._start_workers(worker_count)

    def publish(self, notification: Notification) -> None:
        self._queue.put(notification)

    def _start_workers(self, worker_count: int) -> None:
        for _ in range(worker_count):
            worker = Worker(
                queue=self._queue,
                channel=self,
                max_attempts=self._max_attempts,
            )

            thread = Thread(
                target=worker.run,
                daemon=True,
            )

            thread.start()
            self._workers.append(thread)

    @abstractmethod
    def send(self, notification: Notification) -> None:
        pass