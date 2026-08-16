from dataclasses import dataclass
from .screen import Screen
@dataclass
class Theatre:
    id:str
    name:str
    screens:dict[str,Screen]
    