class Laptop:
    def __init__(self):
        self.name = None
        self.gen = None 
        self.owner = None
        self.manufacturingYear= None
    def show_info(self):
        if(self.name):
            print(self.name)
        if(self.gen):
            print(self.gen)
        if(self.owner):
            print(self.owner)
        if(self.manufacturingYear):
            print(self.manufacturingYear)
        
        