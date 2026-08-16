from dataclasses import dataclass
from datetime import datetime

from .movie import Movie
from .screen import Screen
from .seat_inventory import SeatInventory


@dataclass
class Show:
    id: str
    movie: Movie
    screen: Screen
    start_time: datetime
    end_time: datetime
    seat_inventory: SeatInventory