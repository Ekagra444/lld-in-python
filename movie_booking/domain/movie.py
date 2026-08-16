from dataclasses import dataclass

@dataclass(frozen=True)
class Movie:
    id:str
    title:str
    duration_minutes:int