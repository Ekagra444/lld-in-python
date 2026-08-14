from uuid import uuid4

from notification.enums import ChannelType, NotificationStatus
from notification.models import Notification


def make_notification():
    return Notification(
        sender=uuid4(),
        receiver=uuid4(),
        message="Hello",
        channel_type=ChannelType.EMAIL,
    )


def test_notification_defaults_to_pending():
    notification = make_notification()

    assert notification.status == NotificationStatus.PENDING
    assert notification.attempts == 0


def test_notification_has_unique_id():
    notification1 = make_notification()
    notification2 = make_notification()

    assert notification1.id != notification2.id