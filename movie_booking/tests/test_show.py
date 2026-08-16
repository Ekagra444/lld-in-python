from domain.show_seat import ShowSeatStatus


def test_all_show_seats_start_available(show):
    statuses = show.seat_inventory.get_seat_statuses()

    assert all(
        status == ShowSeatStatus.AVAILABLE
        for status in statuses.values()
    )

def test_show_creates_show_seats_from_screen(show):
    statuses = show.seat_inventory.get_seat_statuses()

    assert set(statuses.keys()) == {
        "A1",
        "A2",
        "B1",
        "B2",
    }

from datetime import datetime

import pytest


def test_overlapping_show_is_rejected(
    show_service,
    movie,
    screen,
):
    show_service.create_show(
        show_id="show-1",
        movie=movie,
        screen=screen,
        start_time=datetime(2026, 8, 16, 18, 0),
        end_time=datetime(2026, 8, 16, 21, 0),
    )

    with pytest.raises(ValueError, match="already occupied"):
        show_service.create_show(
            show_id="show-2",
            movie=movie,
            screen=screen,
            start_time=datetime(2026, 8, 16, 20, 0),
            end_time=datetime(2026, 8, 16, 23, 0),
        )

def test_back_to_back_shows_are_allowed(
    show_service,
    movie,
    screen,
):
    show_service.create_show(
        show_id="show-1",
        movie=movie,
        screen=screen,
        start_time=datetime(2026, 8, 16, 18, 0),
        end_time=datetime(2026, 8, 16, 21, 0),
    )

    show_service.create_show(
        show_id="show-2",
        movie=movie,
        screen=screen,
        start_time=datetime(2026, 8, 16, 21, 0),
        end_time=datetime(2026, 8, 16, 23, 0),
    )

    assert len(screen.shows) == 2