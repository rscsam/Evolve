"""The module that contains all of the backend creature data"""

import math
import random

import tools


class Occupant:
    __size = 0
    __speed = 0
    __y_velocity = 0
    __x_velocity = 0
    __color = "#FFFFFF"

    def __init__(self, color, size, speed):
        self.__color = color
        self.__size = size
        self.__speed = speed
        self.set_starting_velocity()

    def set_x_velocity(self, x):
        self.__x_velocity = x

    def get_x_velocity(self):
        return self.__x_velocity

    def set_y_velocity(self, y):
        self.__y_velocity = y

    def set_color(self, color):
        self.__color = color

    def get_color(self):
        return self.__color

    def hit_side(self):
        self.set_x_velocity(self.get_x_velocity() * -1)

    def hit_lid(self):
        self.set_y_velocity(self.get_y_velocity() * -1)

    def get_y_velocity(self):
        return self.__y_velocity

    def set_size(self, size):
        self.__size = size

    def get_size(self):
        return self.__size

    def set_speed(self, speed):
        self.__speed = speed

    def get_speed(self):
        return self.__speed

    def set_starting_velocity(self):
        """sets the starting velocity of the creature"""
        self.__x_velocity = random.random() * self.__speed
        if random.random() > .5:
            self.__x_velocity *= -1

        self.__y_velocity = math.sqrt(math.pow(self.__speed, 2) - math.pow(self.__x_velocity, 2))
        if random.random() > .5:
            self.__y_velocity *= -1

    def update(self):
        """changes the position of the occupant"""


class Squawker(Occupant):
    def set_starting_velocity(self):
        """sets the starting velocity of the creature"""
        self.set_x_velocity(random.random() * self.get_speed())
        if random.random() > .5:
            self.set_x_velocity(self.get_x_velocity() * -1)

        self.set_y_velocity(math.sqrt(math.pow(self.get_speed(), 2) - math.pow(self.get_x_velocity(), 2)))
        if random.random() > .5:
            self.set_y_velocity(self.get_y_velocity() * -1)

    def update(self):
        """makes the creature change direction occasionally"""
        if random.random() < .03:
            self.set_starting_velocity()


class Dunkboy(Occupant):
    def set_starting_velocity(self):
        """sets the starting velocity of the creature"""
        self.set_x_velocity(random.random() * self.get_speed())
        if random.random() > .5:
            self.set_x_velocity(self.get_x_velocity() * -1)

        # Pythagorean Theorum
        self.set_y_velocity(math.sqrt(math.pow(self.get_speed(), 2) - math.pow(self.get_x_velocity(), 2)))
        if random.random() > .5:
            self.set_y_velocity(self.get_y_velocity() * -1)

    def update(self):
        """"makes the creature change direction occasionally"""
        if random.random() < .23:
            self.set_starting_velocity()


class ReproducingOccupant(Occupant):
    __reproducing = False

    def reproduce(self):
        self.__reproducing = False
        if random.random() < 0.01:
            return ReproducingOccupant(tools.random_color(), self.get_size() + 1, self.get_speed())
        return ReproducingOccupant(self.get_color(), self.get_size() + 1, self.get_speed())

    def reproducing(self):
        return self.__reproducing

    def update(self):
        """makes the creature change direction occasionally"""
        if random.random() < .03:
            self.set_starting_velocity()
        if random.random() < .0003:
            self.__reproducing = True
