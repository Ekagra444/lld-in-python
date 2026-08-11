from .user import User
from .split_strategy import SplitStrategy
class EqualSplit(SplitStrategy):
    def calculate_shares(
        self,
        amount: int,
        participants: list[User],
    ) -> dict[User, int]:
        if not participants:
            raise ValueError("At least one participant is required")
        if amount <= 0:
            raise ValueError("Amount shpuld be greater than 0")
        if (len(set(participants))!=len(participants)):
            raise ValueError("Participants must be unique")
        participant_len = len(participants)
        base_share, remainder = divmod(amount, participant_len)
        shares:dict[User,int]={}
        # adjusting remainder 
        for index,user in enumerate(participants):
            shares[user]=(
                base_share+1
                if index<remainder
                else base_share
            )
        return shares