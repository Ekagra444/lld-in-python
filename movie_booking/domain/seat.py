from dataclasses import dataclass
from enum import Enum

class SeatType(Enum):
    REGULAR = "regular"
    PREMIUM = "premium"
    RECLINER = "recliner"


@dataclass(frozen=True)
class Seat:
    id:str
    seat_type: SeatType

