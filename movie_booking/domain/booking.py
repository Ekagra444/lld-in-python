from dataclasses import dataclass
from enum import Enum


class BookingStatus(Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass
class Booking:
    id: str
    user_id: str
    show_id: str
    seat_ids: tuple[str, ...]
    amount: int
    payment_id: str
    status: BookingStatus = BookingStatus.CONFIRMED