from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field

from .parking_floor import ParkingFloor


@dataclass(slots=True)
class ParkingLot:
    _floors: list[ParkingFloor] = field(
        default_factory=list,
        init=False,
        repr=False,
    )

    def add_floor(self, floor: ParkingFloor) -> None:
        for existing in self._floors:
            if existing.floor_id == floor.floor_id:
                raise ValueError(
                    f"Floor '{floor.floor_id}' already exists."
                )

        self._floors.append(floor)

    def iter_floors(self) -> Iterator[ParkingFloor]:
        return iter(self._floors)