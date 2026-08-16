from datetime import datetime, timedelta

import pytest

from domain.movie import Movie
from domain.screen import Screen
from domain.seat import Seat, SeatType
from services.show_service import ShowService


@pytest.fixture
def seats():
    return {
        "A1": Seat("A1", SeatType.PREMIUM),
        "A2": Seat("A2", SeatType.PREMIUM),
        "B1": Seat("B1", SeatType.REGULAR),
        "B2": Seat("B2", SeatType.REGULAR),
    }


@pytest.fixture
def screen(seats):
    return Screen(
        id="screen-1",
        seats=seats,
    )


@pytest.fixture
def movie():
    return Movie(
        id="movie-1",
        title="Interstellar",
        duration_minutes=169,
    )


@pytest.fixture
def show_service():
    return ShowService(
        hold_duration=timedelta(minutes=5),
    )


@pytest.fixture
def show(show_service, movie, screen):
    return show_service.create_show(
        show_id="show-1",
        movie=movie,
        screen=screen,
        start_time=datetime(2026, 8, 16, 18, 0),
        end_time=datetime(2026, 8, 16, 21, 0),
    )