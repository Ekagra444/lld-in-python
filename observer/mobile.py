from observer import Observer
class MobileObserver(Observer):
    def update(self,temp:int):
        print(f'Mobile Update: temperature updated to {temp}')