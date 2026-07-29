from foodFactory import FoodFactory

class FoodService:
    def prepare_food(self,foodType:str):
        f = FoodFactory.getFood(foodType)
        if(f==None):
            print(r"We don't make this yet, sorry")
            return None
        return f.prepare()
    