from observer import Observer
class TVObserver(Observer):
    def update(self,temp:int):
        print(f'TV Update: temperature updated to {temp}')