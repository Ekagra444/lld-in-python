from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from .vehicle import Vehicle


@dataclass(slots=True)
class ParkingTicket:
    ticket_id: str
    vehicle: Vehicle
    floor_id: str
    spot_id: str
    entry_time: datetime

    exit_time: datetime | None = None
    fee: Decimal | None = None

    def is_closed(self) -> bool:
        return self.fee is not None

    def set_exit_time(
        self,
        exit_time: datetime,
    ) -> None:
        if self.exit_time is not None:
            raise ValueError(
                f"Ticket '{self.ticket_id}' is already closed."
            )

        self.exit_time = exit_time
    def set_fee(self,fee)->None:
        if  self.exit_time is None:
            raise ValueError(
                "Cannot set fee before exit time."
            )
        if self.fee is not None:
            raise ValueError(
                f"Fee already set for ticket: {self.ticket_id}"
            )
        self.fee=fee