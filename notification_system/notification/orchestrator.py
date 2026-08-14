from .channels.base import NotificationChannel
from .enums import ChannelType
from .models import Notification


class NotificationOrchestrator:

    def __init__(
        self,
        channels: dict[ChannelType, NotificationChannel],
    ):
        self._channels = channels

    def send(self, notification: Notification) -> None:
        channel = self._channels[notification.channel_type]
        channel.publish(notification)