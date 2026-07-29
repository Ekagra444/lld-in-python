from weatherStation import WeatherStation
from mobile import  MobileObserver
from tv import TVObserver

WS = WeatherStation()
obs1 = MobileObserver()
obs2 = TVObserver()

WS.addObserver(obs1)
WS.addObserver(obs2)

WS.updateTemperature(35)
WS.updateTemperature(39)
WS.removeObserver(obs1)

WS.updateTemperature(25)
WS.updateTemperature(29)
WS.removeObserver(obs2)

WS.updateTemperature(-10)
WS.updateTemperature(-12)
WS.removeObserver(obs1)
WS.removeObserver(obs2)
