from dataclasses import dataclass

from .user import User

@dataclass(frozen=True,slots=True)
class Settlement:
    payer:User
    receiver:User
    amount:int