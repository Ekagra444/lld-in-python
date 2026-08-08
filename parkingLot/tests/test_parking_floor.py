import pytest

from parking.enums import SpotType
from parking.parking_spot import ParkingSpot
from parking.parking_floor import ParkingFloor

def test_floor_stores_spots():
    floor = ParkingFloor("F1")

    spot1 = ParkingSpot("C1", SpotType.COMPACT)
    spot2 = ParkingSpot("C2", SpotType.COMPACT)

    floor.add_spot(spot1)
    floor.add_spot(spot2)

    assert list(floor.iter_spots()) == [spot1, spot2]


def test_duplicate_spot_id_is_rejected():
    floor = ParkingFloor("F1")

    floor.add_spot(
        ParkingSpot("C1", SpotType.COMPACT)
    )

    with pytest.raises(ValueError):
        floor.add_spot(
            ParkingSpot("C1", SpotType.LARGE)
        )


def test_iterator_does_not_expose_internal_list():
    floor = ParkingFloor("F1")

    floor.add_spot(
        ParkingSpot("C1", SpotType.COMPACT)
    )

    spots = list(floor.iter_spots())

    spots.clear()

    assert len(list(floor.iter_spots())) == 1