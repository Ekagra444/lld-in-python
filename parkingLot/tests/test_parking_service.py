from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

import pytest

from parking.enums import SpotType, VehicleType
from parking.parking_floor import ParkingFloor
from parking.parking_lot import ParkingLot
from parking.parking_service import ParkingService
from parking.parking_spot import ParkingSpot
from parking.vehicle import Vehicle
from parking.strategies.allocation_strategy import SpotAllocationStrategy
from parking.strategies.first_available_strategy import FirstAvailableStrategy
from parking.strategies.hourly_pricing_strategy import HourlyPricingStrategy
from parking.strategies.spot_allocation import SpotAllocation


def make_vehicle(
    registration_number: str,
    vehicle_type: VehicleType = VehicleType.CAR,
) -> Vehicle:
    return Vehicle(
        registration_number=registration_number,
        vehicle_type=vehicle_type,
    )


def build_parking_lot() -> ParkingLot:
    lot = ParkingLot()

    floor = ParkingFloor("F1")

    floor.add_spot(
        ParkingSpot("C1", SpotType.COMPACT)
    )
    floor.add_spot(
        ParkingSpot("C2", SpotType.COMPACT)
    )

    lot.add_floor(floor)

    return lot


def build_service(
    parking_lot: ParkingLot,
    max_retry_attempts: int = 3,
) -> ParkingService:
    return ParkingService(
        parking_lot=parking_lot,
        allocation_strategy=FirstAvailableStrategy(),
        pricing_strategy=HourlyPricingStrategy(),
        max_retry_attempts=max_retry_attempts,
    )


def get_floor(
    parking_lot: ParkingLot,
    floor_id: str,
) -> ParkingFloor:
    for floor in parking_lot.iter_floors():
        if floor.floor_id == floor_id:
            return floor

    raise AssertionError(
        f"Floor '{floor_id}' not found."
    )


def get_spot(
    parking_lot: ParkingLot,
    spot_id: str,
) -> ParkingSpot:
    for floor in parking_lot.iter_floors():
        for spot in floor.iter_spots():
            if spot.spot_id == spot_id:
                return spot

    raise AssertionError(
        f"Spot '{spot_id}' not found."
    )


def test_park_creates_active_session():
    lot = build_parking_lot()
    service = build_service(lot)

    vehicle = make_vehicle("DL01AB1234")

    ticket = service.park(vehicle)

    assert ticket.vehicle is vehicle
    assert ticket.floor_id == "F1"
    assert ticket.spot_id == "C1"

    spot = get_spot(lot, ticket.spot_id)

    assert not spot.is_available()
    assert spot.get_vehicle() is vehicle

    assert ticket.ticket_id in service._active_sessions

    session = service._active_sessions[ticket.ticket_id]

    assert session.ticket is ticket
    assert session.spot is spot


def test_exit_releases_spot_and_returns_fee():
    lot = build_parking_lot()
    service = build_service(lot)

    vehicle = make_vehicle("DL01AB1234")

    ticket = service.park(vehicle)

    fee = service.exit(ticket.ticket_id)

    assert isinstance(fee, Decimal)
    assert fee > Decimal("0")

    spot = get_spot(lot, ticket.spot_id)

    assert spot.is_available()
    assert spot.get_vehicle() is None

    assert ticket.is_closed()
    assert ticket.fee == fee
    assert ticket.exit_time is not None

    assert ticket.ticket_id not in service._active_sessions


def test_exit_unknown_ticket_fails():
    lot = build_parking_lot()
    service = build_service(lot)

    with pytest.raises(ValueError):
        service.exit("does-not-exist")


def test_park_fails_when_lot_is_full():
    lot = build_parking_lot()

    first_spot = get_spot(lot, "C1")
    second_spot = get_spot(lot, "C2")

    first_spot.park(
        make_vehicle("DL01AB0001")
    )
    second_spot.park(
        make_vehicle("DL01AB0002")
    )

    service = build_service(lot)

    with pytest.raises(ValueError):
        service.park(
            make_vehicle("DL01AB0003")
        )


def test_concurrent_parking_allows_only_available_spots_to_be_claimed():
    lot = ParkingLot()

    floor = ParkingFloor("F1")

    floor.add_spot(
        ParkingSpot("C1", SpotType.COMPACT)
    )

    lot.add_floor(floor)

    service = build_service(
        lot,
        max_retry_attempts=10,
    )

    vehicles = [
        make_vehicle(f"DL01AB{i:04d}")
        for i in range(50)
    ]

    def attempt(vehicle: Vehicle):
        try:
            return service.park(vehicle)
        except ValueError:
            return None

    with ThreadPoolExecutor(max_workers=20) as executor:
        tickets = list(
            executor.map(attempt, vehicles)
        )

    successful_tickets = [
        ticket
        for ticket in tickets
        if ticket is not None
    ]

    assert len(successful_tickets) == 1

    spot = next(floor.iter_spots())

    assert not spot.is_available()
    assert len(service._active_sessions) == 1



def test_failed_parking_does_not_create_active_session():
    lot = ParkingLot()

    floor = ParkingFloor("F1")

    spot = ParkingSpot(
        "C1",
        SpotType.COMPACT,
    )

    floor.add_spot(spot)
    lot.add_floor(floor)

    spot.park(
        make_vehicle("DL01AB9999")
    )

    service = build_service(
        lot,
        max_retry_attempts=3,
    )

    with pytest.raises(ValueError):
        service.park(
            make_vehicle("DL01AB1234")
        )

    assert len(service._active_sessions) == 0