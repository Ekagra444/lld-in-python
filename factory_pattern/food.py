from abc import ABC, abstractmethod

class Food(ABC):
    @abstractmethod
    def prepare(self):
        pass
