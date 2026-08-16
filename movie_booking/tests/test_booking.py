from datetime import datetime

import pytest

from domain.booking import BookingStatus
from domain.show_seat import ShowSeatStatus
from payment.payment import (
    FakePaymentProcessor,
    PaymentProcessor,
)
from policies.cancellation import (
    StandardCancellationPolicy,
)
from services.booking_service import BookingService


NOW = datetime(2026, 8, 16, 17, 0)

@pytest.fixture
def booking_service():
    return BookingService(
        payment_processor=FakePaymentProcessor(),
        cancellation_policy=StandardCancellationPolicy(),
    )

def test_successful_booking(
    booking_service,
    show,
):
    booking = booking_service.book(
        booking_id="booking-1",
        user_id="user-1",
        show=show,
        seat_ids=["A1", "A2"],
        amount=500,
        now=NOW,
    )

    assert booking.status == BookingStatus.CONFIRMED
    assert booking.seat_ids == ("A1", "A2")

    statuses = show.seat_inventory.get_seat_statuses()

    assert statuses["A1"] == ShowSeatStatus.BOOKED
    assert statuses["A2"] == ShowSeatStatus.BOOKED


"""
    ====================================================
            Testing failing payment now
    ==================================================== 
"""
class FailingPaymentProcessor(PaymentProcessor):

    def pay(self, payment_id, amount):
        raise RuntimeError("Payment failed")

    def refund(self, payment_id):
        raise AssertionError(
            "Refund should not happen"
        )

def test_payment_failure_releases_hold(show):
    service = BookingService(
        payment_processor=FailingPaymentProcessor(),
        cancellation_policy=StandardCancellationPolicy(),
    )

    with pytest.raises(RuntimeError, match="Payment failed"):
        service.book(
            booking_id="booking-1",
            user_id="user-1",
            show=show,
            seat_ids=["A1"],
            amount=250,
            now=NOW,
        )

    assert (
        show.seat_inventory.get_seat_statuses()["A1"]
        == ShowSeatStatus.AVAILABLE
    )
