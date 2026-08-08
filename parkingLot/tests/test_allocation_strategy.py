import pytest

from parking.enums import SpotType, VehicleType
from parking.parking_spot import ParkingSpot
from parking.vehicle import Vehicle
from parking.parking_floor import ParkingFloor
from parking.parking_lot import ParkingLot
from parking.strategies.first_available_strategy import FirstAvailableStrategy


def test_returns_first_compatible_available_spot():
    lot = ParkingLot()

    floor = ParkingFloor("F1")

    motorcycle_spot = ParkingSpot(
        "M1",
        SpotType.MOTORCYCLE,
    )

    compact_spot = ParkingSpot(
        "C1",
        SpotType.COMPACT,
    )

    floor.add_spot(motorcycle_spot)
    floor.add_spot(compact_spot)
    lot.add_floor(floor)

    vehicle = Vehicle(
        registration_number="DL01AB1234",
        vehicle_type=VehicleType.CAR,
    )

    strategy = FirstAvailableStrategy()

    allocation = strategy.allocate(lot, vehicle)

    assert allocation is not None
    assert allocation.floor is floor
    assert allocation.spot is compact_spot

def test_skips_occupied_spots():
    lot = ParkingLot()
    floor = ParkingFloor("F1")

    first = ParkingSpot("C1", SpotType.COMPACT)
    second = ParkingSpot("C2", SpotType.COMPACT)

    floor.add_spot(first)
    floor.add_spot(second)
    lot.add_floor(floor)

    first.park(
        Vehicle(
            registration_number="DL01AB1111",
            vehicle_type=VehicleType.CAR,
        )
    )

    vehicle = Vehicle(
        registration_number="DL01AB2222",
        vehicle_type=VehicleType.CAR,
    )

    allocation = FirstAvailableStrategy().allocate(
        lot,
        vehicle,
    )

    assert allocation is not None
    assert allocation.spot is second

def test_returns_none_when_no_spot_available():
    lot = ParkingLot()
    floor = ParkingFloor("F1")

    floor.add_spot(
        ParkingSpot("M1", SpotType.MOTORCYCLE)
    )

    lot.add_floor(floor)

    vehicle = Vehicle(
        registration_number="DL01AB1234",
        vehicle_type=VehicleType.CAR,
    )

    allocation = FirstAvailableStrategy().allocate(
        lot,
        vehicle,
    )

    assert allocation is None