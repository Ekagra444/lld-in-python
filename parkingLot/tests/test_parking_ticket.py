import pytest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from parking.enums import VehicleType
from parking.parking_ticket import ParkingTicket
from parking.vehicle import Vehicle

def make_open_ticket() -> ParkingTicket:
    entry = datetime(
        2026, 1, 1, 10, 0, tzinfo=timezone.utc
    )

    ticket = ParkingTicket(
        ticket_id="T1",
        vehicle=Vehicle(
            registration_number="DL01AB1234",
            vehicle_type=VehicleType.CAR,
        ),
        floor_id="F1",
        spot_id="C1",
        entry_time=entry,
    )

    return ticket

def test_ticket_starts_open():
    ticket = make_open_ticket()

    assert not ticket.is_closed()
    assert ticket.exit_time is None
    assert ticket.fee is None


def test_set_exit_time():
    ticket = make_open_ticket()
    exit_time = ticket.entry_time + timedelta(hours=2)

    ticket.set_exit_time(exit_time)

    assert ticket.exit_time == exit_time
    assert not ticket.is_closed()


def test_cannot_set_exit_time_twice():
    ticket = make_open_ticket()

    ticket.set_exit_time(
        ticket.entry_time + timedelta(hours=1)
    )

    with pytest.raises(ValueError):
        ticket.set_exit_time(
            ticket.entry_time + timedelta(hours=2)
        )


def test_fee_requires_exit_time():
    ticket = make_open_ticket()

    with pytest.raises(ValueError):
        ticket.set_fee(Decimal("50"))


def test_ticket_closes_after_fee_is_set():
    ticket = make_open_ticket()

    ticket.set_exit_time(
        ticket.entry_time + timedelta(hours=1)
    )
    ticket.set_fee(Decimal("50"))

    assert ticket.is_closed()
    assert ticket.fee == Decimal("50")


def test_cannot_set_fee_twice():
    ticket = make_open_ticket()

    ticket.set_exit_time(
        ticket.entry_time + timedelta(hours=1)
    )
    ticket.set_fee(Decimal("50"))

    with pytest.raises(ValueError):
        ticket.set_fee(Decimal("100"))