from ..models import Notification
from .base import NotificationSender


class EmailSender(NotificationSender):

    def send(self, notification: Notification) -> None:
        print(
            f"Sending EMAIL to {notification.receiver}: "
            f"{notification.message}"
        )