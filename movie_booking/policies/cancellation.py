from abc import ABC, abstractmethod
from datetime import datetime

from domain.booking import Booking


class CancellationPolicy(ABC):

    @abstractmethod
    def can_cancel(
        self,
        booking: Booking,
        show_start_time: datetime,
        now: datetime,
    ) -> bool:
        pass


class StandardCancellationPolicy(CancellationPolicy):

    def can_cancel(
        self,
        booking,
        show_start_time,
        now,
    ) -> bool:
        return (
            booking.status.name == "CONFIRMED"
            and now < show_start_time
        )