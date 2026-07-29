from transportMode import TransportMode

class TransportService:
    def __init__(self, mode:TransportMode):
        self.__transportMode:TransportMode = mode
    def setMode(self, new_mode:TransportMode):
        self.__transportMode:TransportMode = new_mode
    def eta(self):
        self.__transportMode.eta()
    def route(self):
        self.__transportMode.route()

