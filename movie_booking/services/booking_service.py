from datetime import datetime
from decimal import Decimal

from domain.booking import Booking, BookingStatus
from domain.show import Show
from policies.cancellation import CancellationPolicy
from payment.payment import PaymentProcessor
from domain.booking import Booking
class BookingService:

    def __init__(
        self,
        payment_processor:PaymentProcessor,
        cancellation_policy:CancellationPolicy,
    ):
        self._payment = payment_processor
        self._cancellation_policy = cancellation_policy
        self._bookings:dict[str,Booking] = {}

    def book(
        self,
        booking_id,
        user_id,
        show:Show,
        seat_ids,
        amount,
        now,
    ):
        # Phase 1: acquire seats atomically.
        show.seat_inventory.hold_seats(
            user_id=user_id,
            seat_ids=seat_ids,
            now=now,
        )

        payment_id = f"payment-{booking_id}"
        payment=None
        try:
            payment = self._payment.pay(
                payment_id=payment_id,
                amount=amount,
            )

            # Payment succeeded, but hold could have expired.
            show.seat_inventory.confirm_seats(
                user_id=user_id,
                seat_ids=seat_ids,
                now=now,
            )

        except Exception:
            if payment is not None:
                try:
                    self._payment.refund(payment.id)
                except Exception:
                    raise RuntimeError(
                        "Booking failed and payment compensation failed"
                    )
            show.seat_inventory.release_held_seats(
                user_id=user_id,
                seat_ids=seat_ids,
                now=now,
            )
            raise

        booking = Booking(
            id=booking_id,
            user_id=user_id,
            show_id=show.id,
            seat_ids=tuple(seat_ids),
            amount=amount,
            payment_id=payment.id,
        )

        self._bookings[booking_id] = booking

        return booking

    def cancel(
        self,
        booking_id,
        show:Show,
        now,
    ):
        booking = self._bookings.get(booking_id)

        if booking is None:
            raise ValueError("Booking not found")

        if not self._cancellation_policy.can_cancel(
            booking,
            show.start_time,
            now,
        ):
            raise ValueError(
                "Booking cannot be cancelled"
            )

        # Refund first.
        self._payment.refund(
            booking.payment_id
        )

        # Internal seat release.
        show.seat_inventory.release_booked_seats(
            booking.seat_ids
        )

        booking.status = BookingStatus.CANCELLED