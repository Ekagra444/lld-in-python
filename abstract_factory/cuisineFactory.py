from abc import ABC, abstractmethod
from starter import Starter
from main_course import MainCourse
from sweetDish import SweetDish

class CuisineFactory(ABC):
    @abstractmethod
    def create_starter(self) -> Starter:
        pass

    @abstractmethod
    def create_main_course(self) -> MainCourse:
        pass

    @abstractmethod
    def create_dessert(self) -> SweetDish:
        pass
