from transportMode import TransportMode

class Bus(TransportMode):
    def route(self):
        print("for bus transport take flyover")
    def eta(self):
        print("bus takes 39 minutes")