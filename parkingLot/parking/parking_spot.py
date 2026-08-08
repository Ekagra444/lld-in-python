from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock

from .enums import SpotType, VehicleType
from .vehicle import Vehicle
from .exceptions import VehicleNotCompatibleError,SpotEmptyError,SpotOccupiedError

@dataclass(slots=True)
class ParkingSpot:
    spot_id: str
    spot_type: SpotType

    _parked_vehicle: Vehicle | None = field(
        default=None,
        init=False,
        repr=False,
    )

    _lock: Lock = field(
        default_factory=Lock,
        init=False,
        repr=False,
    )

    _COMPATIBILITY = {
        SpotType.MOTORCYCLE: {
            VehicleType.MOTORCYCLE,
        },
        SpotType.COMPACT: {
            VehicleType.MOTORCYCLE,
            VehicleType.CAR,
        },
        SpotType.LARGE: {
            VehicleType.MOTORCYCLE,
            VehicleType.CAR,
            VehicleType.TRUCK,
        },
    }

    def is_available(self) -> bool:
        with self._lock:
            return self._parked_vehicle is None

    def can_fit(self, vehicle: Vehicle) -> bool:
        return (
            vehicle.vehicle_type
            in self._COMPATIBILITY[self.spot_type]
        )

    def park(self, vehicle: Vehicle) -> None:
        with self._lock:
            if self._parked_vehicle is not None:
                raise ValueError(
                    f"Spot '{self.spot_id}' is already occupied."
                )

            if not self.can_fit(vehicle):
                raise ValueError(
                    f"{vehicle.vehicle_type.name} "
                    f"cannot park in {self.spot_type.name}."
                )

            self._parked_vehicle = vehicle

    def vacate(self) -> Vehicle:
        with self._lock:
            if self._parked_vehicle is None:
                raise ValueError(
                    f"Spot '{self.spot_id}' is already empty."
                )

            vehicle = self._parked_vehicle
            self._parked_vehicle = None
            return vehicle

    def get_vehicle(self) -> Vehicle | None:
        with self._lock:
            return self._parked_vehicle