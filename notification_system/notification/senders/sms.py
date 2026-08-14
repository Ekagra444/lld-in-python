from ..models import Notification
from .base import NotificationSender


class SMSSender(NotificationSender):

    def send(self, notification: Notification) -> None:
        print(
            f"Sending SMS to {notification.receiver}: "
            f"{notification.message}"
        )