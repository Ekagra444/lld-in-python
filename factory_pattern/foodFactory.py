from food import Food 
from pizza import Pizza
from burger import Burger
class FoodFactory:
    @staticmethod
    def getFood(foodType:str)->Food|None:
        if foodType.lower()=="pizza":
            return Pizza()
        elif foodType.lower()=='burger':
            return Burger()
        else:
            return None