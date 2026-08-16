from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .seat import Seat

class ShowSeatStatus(Enum):
    AVAILABLE="available"
    HELD="held"
    BOOKED="booked"

@dataclass
class ShowSeat:
    seat:Seat
    status:ShowSeatStatus=ShowSeatStatus.AVAILABLE
    held_by:str|None = None
    hold_expires_at:datetime|None=None

    def is_hold_expired(self, now:datetime) -> bool:
        return (
            self.status == ShowSeatStatus.HELD
            and self.hold_expires_at is not None
            and self.hold_expires_at <= now
        )       