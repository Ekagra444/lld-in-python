from abc import ABC, abstractmethod

from .user import User

class SplitStrategy(ABC):
    @abstractmethod
    def calculate_shares(
        self,
        amount: int,
        participants: list[User],
    ) -> dict[User, int]:
        ...