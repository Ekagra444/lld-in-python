from dataclasses import dataclass

from .split_strategy import SplitStrategy
from .user import User


BASIS_POINTS = 10_000


@dataclass(frozen=True, slots=True)
class PercentageSplit(SplitStrategy):
    percentages: dict[User, int]

    def calculate_shares(
        self,
        users: list[User],
        amount: int,
    ) -> dict[User, int]:

        if amount <= 0:
            raise ValueError(
                "Expense amount must be positive"
            )

        if set(self.percentages) != set(users):
            raise ValueError(
                "Percentages must match participants"
            )

        if any(
            percentage < 0
            for percentage in self.percentages.values()
        ):
            raise ValueError(
                "Percentage cannot be negative"
            )

        if sum(self.percentages.values()) != BASIS_POINTS:
            raise ValueError(
                "Percentages must sum to 100%"
            )

        shares: dict[User, int] = {}
        remainders: list[tuple[int, User]] = []

        for user in users:
            percentage = self.percentages[user]

            numerator = amount * percentage

            # Integer part of the share.
            share = numerator // BASIS_POINTS

            # Fractional remainder represented exactly.
            remainder = numerator % BASIS_POINTS

            shares[user] = share
            remainders.append((remainder, user))

        remaining = amount - sum(shares.values())

        # Largest remainder first.
        # User ID is the deterministic tie-breaker.
        remainders.sort(
            key=lambda item: (-item[0], item[1].id)
        )

        for _, user in remainders[:remaining]:
            shares[user] += 1

        return shares