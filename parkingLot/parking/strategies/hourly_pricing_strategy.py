from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from math import ceil

from ..enums import VehicleType
from ..parking_ticket import ParkingTicket

from .pricing_strategy import PricingStrategy


class HourlyPricingStrategy(PricingStrategy):

    _RATES = {
        VehicleType.MOTORCYCLE: Decimal("20"),
        VehicleType.CAR: Decimal("50"),
        VehicleType.TRUCK: Decimal("100"),
    }

    def calculate_fee(
        self,
        ticket: ParkingTicket,
    ) -> Decimal:

        if ticket.exit_time is None:
            raise ValueError(
                "Cannot calculate fee for an active ticket."
            )

        duration = (
            ticket.exit_time - ticket.entry_time
        ).total_seconds()

        hours = max( 1,ceil(duration / 3600) )

        return (
            self._RATES[ticket.vehicle.vehicle_type]
            * Decimal(hours)
        )