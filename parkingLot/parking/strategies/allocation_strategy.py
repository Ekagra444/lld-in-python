from __future__ import annotations

from abc import ABC, abstractmethod

from ..parking_lot import ParkingLot
from ..parking_spot import ParkingSpot
from ..vehicle import Vehicle
from .spot_allocation import SpotAllocation


class SpotAllocationStrategy(ABC):

    @abstractmethod
    def allocate(
        self,
        parking_lot: ParkingLot,
        vehicle: Vehicle,
    ) -> SpotAllocation | None:
        """
        Returns the most suitable parking spot for the given vehicle.

        Returns None if no suitable spot exists.
        """
        pass 