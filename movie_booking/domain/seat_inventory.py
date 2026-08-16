from datetime import datetime, timedelta
from threading import Lock

from .show_seat import ShowSeat, ShowSeatStatus


class SeatInventory:
    def __init__(
        self,
        seats,
        hold_duration: timedelta,
    ):
        # creating dict seat.id->ShowSeat object 
        self._show_seats = {
            seat.id: ShowSeat(seat)
            for seat in seats
        }

        self._hold_duration = hold_duration
        self._lock = Lock()

    def get_seat_statuses(self) -> dict:
        with self._lock:
            return {
                seat_id: show_seat.status
                for seat_id, show_seat in self._show_seats.items()
            }

    def hold_seats(
        self,
        user_id: str,
        seat_ids: list[str],
        now: datetime,
    ) -> None:

        with self._lock:
            show_seats = self._get_and_validate(
                seat_ids
            )

            for show_seat in show_seats:
                self._expire_if_needed(show_seat, now)

            for show_seat in show_seats:
                if show_seat.status != ShowSeatStatus.AVAILABLE:
                    raise ValueError(
                        f"Seat {show_seat.seat.id} is unavailable"
                    )

            expiry = now + self._hold_duration

            for show_seat in show_seats:
                show_seat.status = ShowSeatStatus.HELD
                show_seat.held_by = user_id
                show_seat.hold_expires_at = expiry

    def confirm_seats(
        self,
        user_id: str,
        seat_ids: list[str],
        now: datetime,
    ) -> None:

        with self._lock:
            show_seats = self._get_and_validate(
                seat_ids
            )

            # for show_seat in show_seats:
            #     if show_seat.is_hold_expired(now):
            #         self._release(show_seat)

            for show_seat in show_seats:
                if (
                    show_seat.is_hold_expired(now)
                    or show_seat.status != ShowSeatStatus.HELD
                    or show_seat.held_by != user_id
                ):
                    raise ValueError(
                        "Seat hold is no longer valid"
                    )

            for show_seat in show_seats:
                show_seat.status = ShowSeatStatus.BOOKED
                show_seat.held_by = None
                show_seat.hold_expires_at = None

    def release_held_seats(
        self,
        user_id: str,
        seat_ids: list[str],
        now: datetime,
    ) -> None:

        with self._lock:
            show_seats = self._get_and_validate(
                seat_ids
            )

            # for show_seat in show_seats:
            #     if show_seat.is_hold_expired(now):
            #         self._release(show_seat)

            for show_seat in show_seats:
                if (
                    show_seat.is_hold_expired(now)
                    or show_seat.status != ShowSeatStatus.HELD
                    or show_seat.held_by != user_id
                ):
                    raise ValueError(
                        "Seat is not held by this user"
                    )

            for show_seat in show_seats:
                self._release(show_seat)

    def release_booked_seats(
        self,
        seat_ids: list[str],
    ) -> None:

        with self._lock:
            show_seats = self._get_and_validate(
                seat_ids
            )

            for show_seat in show_seats:
                if show_seat.status != ShowSeatStatus.BOOKED:
                    raise ValueError(
                        "Seat is not booked"
                    )

            for show_seat in show_seats:
                self._release(show_seat)

    def _get_and_validate(self, seat_ids):
        if not seat_ids:
            raise ValueError("No seats selected")

        if len(seat_ids) != len(set(seat_ids)):
            raise ValueError("Duplicate seats selected")

        try:
            return [
                self._show_seats[seat_id]
                for seat_id in seat_ids
            ]
        except KeyError as exc:
            raise ValueError(
                f"Unknown seat: {exc.args[0]}"
            ) from exc

    @staticmethod
    def _expire_if_needed(show_seat, now):
        if show_seat.is_hold_expired(now):
            SeatInventory._release(show_seat)

    @staticmethod
    def _release(show_seat):
        show_seat.status = ShowSeatStatus.AVAILABLE
        show_seat.held_by = None
        show_seat.hold_expires_at = None