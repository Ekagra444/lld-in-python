from dataclasses import dataclass

from ..parking_floor import ParkingFloor
from ..parking_spot import ParkingSpot


@dataclass(frozen=True, slots=True)
class SpotAllocation:
    floor: ParkingFloor
    spot: ParkingSpot