from laptop import Laptop
class LaptopBuilder:
    def __init__(self):
        self.__laptop = Laptop()
    def addOwner(self,owner):
        self.__laptop.owner= owner
        return self
    def add_manufacturing_year(self, yr):
        self.__laptop.manufacturingYear= yr
        return self    
    def addName(self,name):
        self.__laptop.name= name
        return self
    def addGeneration(self,gen):
        self.__laptop.gen= gen
        return self
    def build(self):
        return self.__laptop


