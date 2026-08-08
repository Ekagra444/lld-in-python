import pytest
from parking.parking_spot import ParkingSpot
from parking.parking_floor import ParkingFloor
from parking.parking_lot import ParkingLot
def test_lot_stores_floors():
    lot = ParkingLot()

    floor1 = ParkingFloor("F1")
    floor2 = ParkingFloor("F2")

    lot.add_floor(floor1)
    lot.add_floor(floor2)

    assert list(lot.iter_floors()) == [floor1, floor2]


def test_duplicate_floor_id_is_rejected():
    lot = ParkingLot()

    lot.add_floor(ParkingFloor("F1"))

    with pytest.raises(ValueError):
        lot.add_floor(ParkingFloor("F1"))