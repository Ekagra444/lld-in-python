from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field

from .parking_spot import ParkingSpot


@dataclass(slots=True)
class ParkingFloor:
    floor_id: str

    _spots: list[ParkingSpot] = field(
        default_factory=list,
        init=False,
        repr=False,
    )

    def add_spot(self, spot: ParkingSpot) -> None:
        for existing in self._spots:
            if existing.spot_id == spot.spot_id:
                raise ValueError(
                    f"Spot '{spot.spot_id}' already exists "
                    f"on floor '{self.floor_id}'."
                )

        self._spots.append(spot)

    def iter_spots(self) -> Iterator[ParkingSpot]:
        return iter(self._spots)