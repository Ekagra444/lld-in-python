from discount_service import DiscountService
from diwali import Diwali
from holi import Holi

festive1 = Diwali()
DS = DiscountService(festive1)
DS.apply()

festive2 = Holi()
DS.setStrategy(festive2)
DS.apply()
