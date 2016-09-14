"""The module that contains all of the backend creature data"""

import random
import math


class Occupant:
    __x = 0
    __y = 0
    __size = 0
    __visible = False
    __speed = 0
    __y_velocity = 0
    __x_velocity = 0

    def __init__(self, x, y, size, speed):
        self.__x = x
        self.__y = y
        self.__size = size
        self.__speed = speed
        self.set_starting_velocity()

    def setx(self, x):
        self.__x = x

    def getx(self):
        return self.__x

    def sety(self, y):
        self.__y = y

    def gety(self):
        return self.__y

    def set_size(self, size):
        self.__size = size

    def get_size(self):
        return self.__size

    def set_starting_velocity(self):
        """sets the starting velocity of the creature"""
        self.__x_velocity = random.random() * self.__speed
        if random.random() > .5:
            self.__x_velocity *= -1

        self.__y_velocity = math.sqrt(math.pow(self.__speed, 2) - math.pow(self.__x_velocity, 2))
        if random.random() > .5:
            self.__y_velocity *= -1

    def move(self):
        """reverses direction if hits a wall"""
        if self.__x > 1000 or self.__x < 0:
            self.__x_velocity *= -1
        if self.__y > 600 or self.__y < 0:
            self.__y_velocity *= -1

        """changes the position of the occupant"""
        self.setx(self.getx() + self.__x_velocity)
        self.sety(self.gety() + self.__y_velocity)

        """makes the creature change direction occasionally"""
        if random.random() < .03:
            self.set_starting_velocity()
