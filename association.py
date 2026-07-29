# One object knows about another.
# Neither owns the other's lifetime.

class Teacher:
    def __init__(self):
        pass
    def teach(self):
        print("teaching ....")
    def scold(self):
        print('scolding....')
class Student:
    def __init__(self,teacher:"Teacher"):
        self.teacher = teacher
    def study(self):
        self.teacher.teach()
    def getScolded(self):
        self.teacher.scold()

teacher1 = Teacher()
student1 = Student(teacher1)

student1.getScolded()
student1.study()

