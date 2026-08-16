from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod


class PaymentStatus(Enum):
    SUCCESS = "success"
    REFUNDED = "refunded"


@dataclass
class Payment:
    id: str
    amount: int
    status: PaymentStatus


class PaymentProcessor(ABC):

    @abstractmethod
    def pay(self, payment_id: str, amount: int) -> Payment:
        pass

    @abstractmethod
    def refund(self, payment_id: str) -> None:
        pass


class FakePaymentProcessor(PaymentProcessor):

    def pay(self, payment_id: str, amount: int) -> Payment:
        return Payment(
            id=payment_id,
            amount=amount,
            status=PaymentStatus.SUCCESS,
        )

    def refund(self, payment_id: str) -> None:
        pass