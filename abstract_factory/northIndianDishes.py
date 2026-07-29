from starter import Starter
from main_course import MainCourse
from sweetDish import SweetDish
class PaneerTikka(Starter):
    def prepare(self):
        print("Preparing Paneer Tikka (North Indian Starter)")


class ButterChicken(MainCourse):
    def prepare(self):
        print("Preparing Butter Chicken (North Indian Main Course)")


class GulabJamun(SweetDish):
    def prepare(self):
        print("Preparing Gulab Jamun (North Indian Dessert)")