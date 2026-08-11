from dataclasses import dataclass, field

from .user import User
from .split_strategy import SplitStrategy

@dataclass(slots=True)
class Expense:   
    id:str
    payer:User
    amount:int
    participants: list[User]
    split_strategy:SplitStrategy
    shares:dict[User,int] = field(init=False)

    def __post_init__(self):
        # validate expense
        if self.amount <=0:
            raise ValueError("Expense amount must be positive")
        if not self.participants:
            raise ValueError("There should be participants in an expense")
        if self.payer not in self.participants:
            raise ValueError("Payer must be in Participants")
        self.shares = self.split_strategy.calculate_shares(amount=self.amount,participants=self.participants)
        # validate share sum 
        if sum(self.shares.values())!=self.amount:
            raise ValueError("Split shares must be to original amount")