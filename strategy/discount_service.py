from discount_strategy import DiscountStrategy

class DiscountService:
    def __init__(self, strategy:DiscountStrategy):
        self.__strategy = strategy
    def setStrategy(self, str:DiscountStrategy):
        self.__strategy = str
    def apply(self):
        self.__strategy.discount()
