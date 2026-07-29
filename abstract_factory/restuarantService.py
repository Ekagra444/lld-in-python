from cuisineFactory import CuisineFactory
from northIndianCuisine import NorthIndianCuisine
from chineeseCuisine import ChineseCuisine
class RestaurantService:
    def __init__(self, factory: CuisineFactory):
        self.__factory = factory

    def create_meal(self):
        starter = self.__factory.create_starter()
        main_course = self.__factory.create_main_course()
        dessert = self.__factory.create_dessert()

        starter.prepare()
        main_course.prepare()
        dessert.prepare()

    def change_cuisine(self, new_factory: CuisineFactory):
        self.__factory = new_factory


north_indian_cuisine = NorthIndianCuisine()
restaurant_service = RestaurantService(north_indian_cuisine)
restaurant_service.create_meal()

chinese = ChineseCuisine()
restaurant_service.change_cuisine(chinese)
restaurant_service.create_meal()