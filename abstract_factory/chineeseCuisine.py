from starter import Starter
from main_course import MainCourse
from sweetDish import SweetDish
from chineeseDisher import SpringRolls, FriedRice, FortuneCookie
from cuisineFactory import CuisineFactory
class ChineseCuisine(CuisineFactory):
    def create_starter(self) -> Starter:
        return SpringRolls()

    def create_main_course(self) -> MainCourse:
        return FriedRice()

    def create_dessert(self) -> SweetDish:
        return FortuneCookie()