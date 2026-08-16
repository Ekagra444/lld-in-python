from dataclasses import dataclass
from .theatre import Theatre

@dataclass
class MovieComplex:
    id:str
    name:str
    theatres:dict[str,Theatre]

