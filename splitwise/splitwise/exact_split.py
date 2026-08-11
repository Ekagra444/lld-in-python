from dataclasses import dataclass

from .user import User
from .split_strategy import SplitStrategy


@dataclass(frozen=True, slots=True)
class ExactSplit(SplitStrategy):
    shares: dict[User, int]

    def calculate_shares(
        self,
        users: list[User],
        amount: int,
    ) -> dict[User, int]:

        if amount <= 0:
            raise ValueError(
                "Expense amount must be positive"
            )

        if set(self.shares) != set(users):
            raise ValueError(
                "Shares must match participants"
            )

        if any(
            share < 0
            for share in self.shares.values()
        ):
            raise ValueError(
                "Share cannot be negative"
            )

        if sum(self.shares.values()) != amount:
            raise ValueError(
                "Shares must sum to expense amount"
            )

        return dict(self.shares)