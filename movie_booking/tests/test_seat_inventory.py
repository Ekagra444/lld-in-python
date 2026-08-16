from datetime import datetime

from domain.show_seat import ShowSeatStatus


NOW = datetime(2026, 8, 16, 17, 0)


def test_user_can_hold_available_seats(show):
    show.seat_inventory.hold_seats(
        user_id="user-1",
        seat_ids=["A1", "A2"],
        now=NOW,
    )

    statuses = show.seat_inventory.get_seat_statuses()

    assert statuses["A1"] == ShowSeatStatus.HELD
    assert statuses["A2"] == ShowSeatStatus.HELD

import pytest


def test_cannot_hold_already_held_seat(show):
    show.seat_inventory.hold_seats(
        user_id="user-1",
        seat_ids=["A1"],
        now=NOW,
    )

    with pytest.raises(ValueError):
        show.seat_inventory.hold_seats(
            user_id="user-2",
            seat_ids=["A1"],
            now=NOW,
        )

def test_multi_seat_hold_is_atomic(show):
    show.seat_inventory.hold_seats(
        user_id="user-1",
        seat_ids=["A2"],
        now=NOW,
    )

    with pytest.raises(ValueError):
        show.seat_inventory.hold_seats(
            user_id="user-2",
            seat_ids=["A1", "A2"],
            now=NOW,
        )

    statuses = show.seat_inventory.get_seat_statuses()

    assert statuses["A1"] == ShowSeatStatus.AVAILABLE
    assert statuses["A2"] == ShowSeatStatus.HELD

def test_only_holder_can_confirm(show):
    show.seat_inventory.hold_seats(
        user_id="user-1",
        seat_ids=["A1"],
        now=NOW,
    )

    with pytest.raises(ValueError):
        show.seat_inventory.confirm_seats(
            user_id="user-2",
            seat_ids=["A1"],
            now=NOW,
        )

    assert (
        show.seat_inventory.get_seat_statuses()["A1"]
        == ShowSeatStatus.HELD
    )

def test_holder_can_confirm(show):
    show.seat_inventory.hold_seats(
        user_id="user-1",
        seat_ids=["A1"],
        now=NOW,
    )

    show.seat_inventory.confirm_seats(
        user_id="user-1",
        seat_ids=["A1"],
        now=NOW,
    )

    assert (
        show.seat_inventory.get_seat_statuses()["A1"]
        == ShowSeatStatus.BOOKED
    )

def test_expired_hold_becomes_available(show):
    show.seat_inventory.hold_seats(
        user_id="user-1",
        seat_ids=["A1"],
        now=NOW,
    )

    later = datetime(2026, 8, 16, 17, 6)

    show.seat_inventory.hold_seats(
        user_id="user-2",
        seat_ids=["A1"],
        now=later,
    )

    statuses = show.seat_inventory.get_seat_statuses()

    assert statuses["A1"] == ShowSeatStatus.HELD