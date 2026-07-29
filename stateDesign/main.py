from bus import Bus
from walk import Walk
from transportService import TransportService
bus = Bus()
walk = Walk()
transport1 = TransportService(bus)
transport2 = TransportService(walk)
transport1.route()
transport1.eta()

transport2.route()
transport2.eta()