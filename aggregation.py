# A stronger Association.
# Whole contains parts.
# Parts can live independently.
class Employee:

    def __init__(self, name):
        self.name = name


class Department:

    def __init__(self):
        self.employees = []

    def add(self, emp):
        self.employees.append(emp)

e1 = Employee("Ram")
e2 = Employee("Sham")
dept = Department()

dept.add(e1)
dept.add(e2)

# Delete Department.
# Employee still exists.