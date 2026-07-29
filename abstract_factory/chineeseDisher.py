from starter import Starter
from main_course import MainCourse
from sweetDish import SweetDish
class SpringRolls(Starter):
    def prepare(self):
        print("Preparing Spring Rolls (Chinese Starter)")


class FriedRice(MainCourse):
    def prepare(self):
        print("Preparing Fried Rice (Chinese Main Course)")


class FortuneCookie(SweetDish):
    def prepare(self):
        print("Preparing Fortune Cookie (Chinese Dessert)")