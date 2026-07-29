from abc import ABC, abstractmethod

class InteratorInterface(ABC):
    @abstractmethod
    def next():
        pass
    @abstractmethod
    def has_next():
        pass
