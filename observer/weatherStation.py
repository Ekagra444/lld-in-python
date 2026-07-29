from observer import Observer
from typing import List
class WeatherStation:
    def __init__(self):
        self.__observers:List[Observer] = []
        self.__temperature=-1
    def addObserver(self,obs:Observer):
        self.__observers.append(obs)
    def notifyAll(self):
        for observer in self.__observers:
            observer.update(self.__temperature)
    def updateTemperature(self,temp):
        self.__temperature= temp
        self.notifyAll()

    def removeObserver(self,obs):
        try:
            self.__observers.remove(obs)
            print(f'observer {obs} removed')
        except ValueError:
            print(f'no such observer found')
        
            
     