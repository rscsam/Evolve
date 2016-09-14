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


class Dot:
    __occupant = 0
    __x = 0
    __y = 0
    __x2 = 0
    __y2 = 0
    __radius = 0
    __reference = None

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
        x = (self.__x + self.__x2) / 2
        y = (self.__y + self.__y2) / 2
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
