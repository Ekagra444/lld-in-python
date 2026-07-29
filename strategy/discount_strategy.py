from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod 
    def discount(self):
        pass