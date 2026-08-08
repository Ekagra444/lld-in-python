from abc import ABC, abstractmethod
from decimal import Decimal

from ..parking_ticket import ParkingTicket

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(
        self,
        ticket:ParkingTicket,
    )->Decimal:
        """
        Calculates the parking fee for a completed parking session.
        """
        pass