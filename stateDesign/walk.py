from transportMode import TransportMode

class Walk(TransportMode):
    def route(self):
        print("for walking go straight")
    def eta(self):
        print("walking takes 1 hr")