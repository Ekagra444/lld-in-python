from __future__ import annotations

from dataclasses import dataclass

from .parking_spot import ParkingSpot
from .parking_ticket import ParkingTicket


@dataclass(slots=True)
class ActiveParkingSession:
    ticket: ParkingTicket
    spot: ParkingSpot