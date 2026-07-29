from abc import ABC , abstractmethod
class NotificationInterface(ABC):
    @abstractmethod
    def send(self,sender:str,to:str,msg:str):
        pass
    
