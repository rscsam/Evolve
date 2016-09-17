"""The module that handles the front-end representations of the backend"""

from creature import *


class World:
    occupants = []

    def add_occupant(self, occupant):
        self.occupants.append(Dot(occupant))

    def add(self, x, y, size, speed):
        c = Dot(Occupant(x, y, size, speed))
        self.occupants.append(c)
        return c

    def add_squawker(self, x, y, size, speed):
        c = Dot(Squawker(x, y, size, speed))
        self.occupants.append(c)
        return c

    def add_dunkboy(self, x, y, size, speed):
        c = Dot(Dunkboy(x, y, size, speed))
        self.occupants.append(c)
        return c

    def handle_wall_collision(self):
        for dot in self.occupants:
            if (dot.getx() + (2 * dot.get_radius())) > 1000 or dot.getx() < 0:
                dot.get_occupant().hit_side()
            if (dot.gety() + (2 * dot.get_radius())) > 600 or dot.gety() < 0:
                dot.get_occupant().hit_lid()

    def detect_collision(self, dot):
        for c in self.occupants:
            if c != dot:
                distance = int(((dot.get_centerx() - c.get_centerx())**2) + ((dot.get_centery() - c.get_centery())**2)**0.5)+1
                if distance <= (dot.get_radius() + c.get_radius()):
                    return True
        return False


class Dot:
    __occupant = 0
    __x = 0
    __y = 0
    __x2 = 0
    __y2 = 0
    __radius = 0
    __reference = None
    __trigger = False

    def __init__(self, occupant):
        self.__occupant = occupant
        self.setx(occupant.getx())
        self.sety(occupant.gety())
        self.__radius = occupant.get_size()

    def setx(self, x):
        self.__x = x
        self.__x2 = x + (2 * self.__radius)

    def getx(self):
        return self.__x

    def sety(self, y):
        self.__y = y
        self.__y2 = y + (2 * self.__radius)

    def gety(self):
        return self.__y

    def getx2(self):
        return self.__x2

    def gety2(self):
        return self.__y2

    def set_radius(self, radius):
        self.__radius = radius

    def get_radius(self):
        return self.__radius

    def get_occupant(self):
        return self.__occupant

    def get_center(self):
        x = self.__x + self.__radius
        y = self.__y + self.__radius
        return (x, y)

    def get_centerx(self):
        return self.get_center()[0]

    def get_centery(self):
        return self.get_center()[1]

    def set_reference(self, reference):
        self.__reference = reference
        self.__x2 = self.__x + (2 * self.__radius)
        self.__y2 = self.__y + (2 * self.__radius)

    def get_reference(self):
        return self.__reference

    def move(self):
        self.__occupant.move()
        self.setx(self.__occupant.getx())
        self.sety(self.__occupant.gety())

    def update(self):
        self.move()

    def trigger(self):
        self.__trigger = True

    def triggered(self):
        return self.__trigger