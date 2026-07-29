from starter import Starter
from main_course import MainCourse
from sweetDish import SweetDish
from northIndianDishes import PaneerTikka, ButterChicken, GulabJamun
from cuisineFactory import CuisineFactory
class NorthIndianCuisine(CuisineFactory):
    def create_starter(self) -> Starter:
        return PaneerTikka()

    def create_main_course(self) -> MainCourse:
        return ButterChicken()

    def create_dessert(self) -> SweetDish:
        return GulabJamun()
