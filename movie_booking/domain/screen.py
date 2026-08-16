from __future__ import annotations
from dataclasses import dataclass,field
from datetime import datetime
from typing import TYPE_CHECKING

from .seat import Seat

if TYPE_CHECKING:
    from .show import Show
    
@dataclass

class Screen:
    id:str
    seats:dict[str,Seat]
    shows:list["Show"] = field(default_factory=list)

    def can_schedule(
            self,
            start_time: datetime,
            end_time: datetime,
    )->bool:
        for show in self.shows:
            if(start_time<show.end_time and end_time>show.start_time):
                return False
        return True

    def add_show(self,show:"Show")->None:
        if not self.can_schedule(
            show.start_time,
            show.end_time
        ):
            raise ValueError("Screen is already occupied")
        self.shows.append(show)

        