import pytest

from parking.enums import SpotType, VehicleType
from parking.parking_spot import ParkingSpot
from parking.vehicle import Vehicle
from concurrent.futures import ThreadPoolExecutor


def make_vehicle(vehicle_type: VehicleType) -> Vehicle:
    return Vehicle(
        registration_number="DL01AB1234",
        vehicle_type=vehicle_type,
    )


def test_new_spot_is_available():
    spot = ParkingSpot("C1", SpotType.COMPACT)

    assert spot.is_available()


def test_park_vehicle():
    spot = ParkingSpot("C1", SpotType.COMPACT)
    vehicle = make_vehicle(VehicleType.CAR)

    spot.park(vehicle)

    assert not spot.is_available()
    assert spot.get_vehicle() is vehicle


def test_cannot_park_incompatible_vehicle():
    spot = ParkingSpot("M1", SpotType.MOTORCYCLE)
    vehicle = make_vehicle(VehicleType.CAR)

    with pytest.raises(ValueError):
        spot.park(vehicle)

    assert spot.is_available()


def test_cannot_park_when_already_occupied():
    spot = ParkingSpot("C1", SpotType.COMPACT)

    first = make_vehicle(VehicleType.CAR)
    second = Vehicle(
        registration_number="DL01AB5678",
        vehicle_type=VehicleType.CAR,
    )

    spot.park(first)

    with pytest.raises(ValueError):
        spot.park(second)

    assert spot.get_vehicle() is first


def test_vacate_returns_vehicle():
    spot = ParkingSpot("C1", SpotType.COMPACT)
    vehicle = make_vehicle(VehicleType.CAR)

    spot.park(vehicle)

    removed = spot.vacate()

    assert removed is vehicle
    assert spot.is_available()


def test_cannot_vacate_empty_spot():
    spot = ParkingSpot("C1", SpotType.COMPACT)

    with pytest.raises(ValueError):
        spot.vacate()



def test_only_one_thread_can_occupy_spot():
    spot = ParkingSpot("C1", SpotType.COMPACT)

    vehicles = [
        Vehicle(
            registration_number=f"DL01AB{i:04d}",
            vehicle_type=VehicleType.CAR,
        )
        for i in range(100)
    ]

    def attempt(vehicle):
        try:
            spot.park(vehicle)
            return True
        except ValueError:
            return False

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(attempt, vehicles))

    assert sum(results) == 1
    assert not spot.is_available()