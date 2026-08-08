from dataclasses import dataclass
from .enums import VehicleType
@dataclass(frozen=True, slots=True)
class Vehicle:
    registration_number:str
    vehicle_type:VehicleType