# Strongest relationship.
# Part cannot exist independently.

class Room:

    def __init__(self, number):
        self.number = number


class House:

    def __init__(self):
        self.rooms = [
            Room(1),
            Room(2),
            Room(3)
        ]

# House creates Rooms.
# Nobody else owns them.
# Delete House.
# Rooms disappear.

