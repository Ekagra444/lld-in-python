from abc import ABC,abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self,temp:int):
        pass