from datetime import datetime

from domain.seat_inventory import SeatInventory
from domain.show import Show
from domain.screen import Screen

class ShowService:
    def __init__(self,hold_duration):
        self._hold_duration = hold_duration

    def create_show(
            self,
            show_id,
            movie,
            screen:"Screen",
            start_time,
            end_time,
    ) -> Show:
        if end_time<=start_time:
            raise ValueError("Invalid show timing")

        if not screen.can_schedule(start_time=start_time,end_time=end_time):
            raise ValueError("Screen is already occupied")

        inventory = SeatInventory(
            seats=screen.seats.values(),
            hold_duration=self._hold_duration
        )
        show = Show(
            id = show_id,
            movie=movie,
            screen=screen,
            start_time=start_time,
            end_time=end_time,
            seat_inventory=inventory
        )

        screen.shows.append(show)

        return show