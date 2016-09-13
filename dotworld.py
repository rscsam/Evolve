'''
The module that handles the front-end representations of the backend
'''

from creature import *


class World:
    occupants = []

    def add_occupant(self, occupant):
        self.occupants.append(Dot(occupant))

    def add(self, x, y, size, speed):
        self.occupants.append(Dot(Occupant(x, y, size, speed)))


class DotList:
    __list = []


class Dot:
    __occupant = 0
    __x = 0
    __y = 0
    __radius = 0

    def __init__(self, occupant):
        self.__occupant = occupant
        self.__x = occupant.getx()
        self.__y = occupant.gety()
        self.__radius = occupant.get_size()

    def setx(self, x):
        self.__x = x

    def getx(self):
        return self.__x

    def sety(self, y):
        self.__y = y

    def gety(self):
        return self.__y

    def set_radius(self, radius):
        self.__radius = radius

    def get_radius(self):
        return self.__radius

    def get_occupant(self):
        return self.__occupant

    def move(self):
        self.__occupant.move()
        self.__x = self.__occupant.getx()
        self.__y = self.__occupant.gety()


