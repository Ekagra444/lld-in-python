from laptopBuilder import LaptopBuilder
lp = LaptopBuilder().addName('lenovoLq').add_manufacturing_year('2016').addGeneration('i7').addOwner('superuser').build()
lp.show_info()