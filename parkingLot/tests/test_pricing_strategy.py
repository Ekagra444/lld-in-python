import pytest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from parking.enums import VehicleType
from parking.parking_ticket import ParkingTicket
from parking.vehicle import Vehicle
from parking.strategies.hourly_pricing_strategy import HourlyPricingStrategy

def make_ticket(duration: timedelta) -> ParkingTicket:
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

    ticket.set_exit_time(entry + duration)

    return ticket

def test_less_than_one_hour_is_charged_one_hour():
    ticket = make_ticket(timedelta(minutes=30))

    fee = HourlyPricingStrategy().calculate_fee(ticket)

    assert fee == Decimal("50")


def test_exactly_one_hour():
    ticket = make_ticket(timedelta(hours=1))

    fee = HourlyPricingStrategy().calculate_fee(ticket)

    assert fee == Decimal("50")


def test_one_hour_and_one_minute():
    ticket = make_ticket(
        timedelta(hours=1, minutes=1)
    )

    fee = HourlyPricingStrategy().calculate_fee(ticket)

    assert fee == Decimal("100")

@pytest.mark.parametrize(
    ("vehicle_type", "expected"),
    [
        (VehicleType.MOTORCYCLE, Decimal("20")),
        (VehicleType.CAR, Decimal("50")),
        (VehicleType.TRUCK, Decimal("100")),
    ],
)
def test_vehicle_specific_rates(vehicle_type, expected):
    entry = datetime(
        2026, 1, 1, 10, 0, tzinfo=timezone.utc
    )

    ticket = ParkingTicket(
        ticket_id="T1",
        vehicle=Vehicle(
            registration_number="DL01AB1234",
            vehicle_type=vehicle_type,
        ),
        floor_id="F1",
        spot_id="C1",
        entry_time=entry,
    )

    ticket.set_exit_time(
        entry + timedelta(hours=1)
    )

    fee = HourlyPricingStrategy().calculate_fee(ticket)

    assert fee == expected

def test_cannot_calculate_fee_for_active_ticket():
    ticket = ParkingTicket(
        ticket_id="T1",
        vehicle=Vehicle(
            registration_number="DL01AB1234",
            vehicle_type=VehicleType.CAR,
        ),
        floor_id="F1",
        spot_id="C1",
        entry_time=datetime.now(timezone.utc),
    )

    with pytest.raises(ValueError):
        HourlyPricingStrategy().calculate_fee(ticket)