from __future__ import annotations

from ..parking_lot import ParkingLot
from .spot_allocation import SpotAllocation
from ..vehicle import Vehicle

from .allocation_strategy import SpotAllocationStrategy

class FirstAvailableStrategy(SpotAllocationStrategy):
    def allocate(self, parking_lot:ParkingLot, vehicle:Vehicle)->SpotAllocation|None:
        for floor in parking_lot.iter_floors():
            for spot in floor.iter_spots():
                if not spot.is_available():
                    continue
                if not spot.can_fit(vehicle):
                    continue
                return SpotAllocation(
                    floor=floor,
                    spot=spot,
                )
        return None
    

        