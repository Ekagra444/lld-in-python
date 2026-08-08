from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4
from decimal import Decimal

from .active_parking_session import ActiveParkingSession
from .strategies.allocation_strategy import SpotAllocationStrategy
from .parking_lot import ParkingLot
from .parking_ticket import ParkingTicket
from .strategies.pricing_strategy import PricingStrategy
from .vehicle import Vehicle


class ParkingService:

    def __init__(
        self,
        parking_lot: ParkingLot,
        allocation_strategy: SpotAllocationStrategy,
        pricing_strategy: PricingStrategy,
        max_retry_attempts: int = 3,
    ):
        if max_retry_attempts <= 0:
            raise ValueError(
                "max_retry_attempts must be greater than zero."
            )

        self._parking_lot = parking_lot
        self._allocation_strategy = allocation_strategy
        self._pricing_strategy = pricing_strategy
        self._max_retry_attempts = max_retry_attempts

        self._active_sessions: dict[
            str,
            ActiveParkingSession,
        ] = {}

        self._active_sessions_lock = Lock()

    def park(self, vehicle: Vehicle) -> ParkingTicket:
        for _ in range(self._max_retry_attempts):

            allocation = self._allocation_strategy.allocate(
                self._parking_lot,
                vehicle,
            )
            if allocation is None:
                raise ValueError(
                    "No suitable parking spot available."
                )
            spot = allocation.spot
            floor = allocation.floor
            if spot is None:
                raise ValueError(
                    "No suitable parking spot available."
                )

            try:
                spot.park(vehicle)

            except ValueError:
                # The spot may have been occupied by another
                # thread after the strategy selected it.
                continue

            ticket = ParkingTicket(
                ticket_id=str(uuid4()),
                vehicle=vehicle,
                floor_id=floor.floor_id,
                spot_id=spot.spot_id,
                entry_time=datetime.now(timezone.utc),
            )

            session = ActiveParkingSession(
                ticket=ticket,
                spot=spot,
            )

            with self._active_sessions_lock:
                self._active_sessions[
                    ticket.ticket_id
                ] = session

            return ticket

        raise ValueError(
            "Unable to park vehicle after retry attempts."
        )

    def exit(self, ticket_id: str) -> Decimal:
        with self._active_sessions_lock:
            session = self._active_sessions.pop(
                ticket_id,
                None,
            )

        if session is None:
            raise ValueError(
                f"Active ticket '{ticket_id}' not found."
            )

        ticket = session.ticket
        spot = session.spot

        exit_time = datetime.now(timezone.utc)

        ticket.set_exit_time(exit_time)

        fee = self._pricing_strategy.calculate_fee(ticket)

        ticket.set_fee(fee)

        spot.vacate()

        return fee

    