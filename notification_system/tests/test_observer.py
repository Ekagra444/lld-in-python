from uuid import uuid4

from notification.enums import ChannelType, NotificationStatus
from notification.models import Notification
from notification.observer.observer import NotificationObserver


class TestObserver(NotificationObserver):

    def __init__(self):
        self.statuses = []

    def update(self, notification):
        self.statuses.append(notification.status)


def make_notification():
    return Notification(
        sender=uuid4(),
        receiver=uuid4(),
        message="Hello",
        channel_type=ChannelType.EMAIL,
    )


def test_observer_receives_status_updates():
    notification = make_notification()
    observer = TestObserver()

    notification.add_observer(observer)

    notification.set_status(NotificationStatus.PROCESSING)
    notification.set_status(NotificationStatus.SENT)

    assert observer.statuses == [
        NotificationStatus.PROCESSING,
        NotificationStatus.SENT,
    ]