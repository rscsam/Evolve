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
    __alive = True
    __energy = 500

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

    def get_energy(self):
        return self.__energy

    def set_energy(self, e):
        self.__energy = e

    def add_energy(self, e):
        self.__energy += e

    def subtract_energy(self, e):
        self.__energy -= e

    def die(self):
        self.__alive = False

    def alive(self):
        return self.__alive

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


class ConvenientOccupant(Occupant):
    def set_starting_velocity(self):
        self.set_x_velocity(self.get_speed())
        self.set_y_velocity(0)


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
    __parent = None

    def __init__(self, color, size, speed, parent):
        Occupant.__init__(self, color, size, speed)
        self.__parent = parent

    def get_parent(self):
        return self.__parent

    def reproduce(self):
        self.__reproducing = False
        if random.random() < .29:
            color = tools.mix_colors(self.get_color(), tools.random_color())
            return ReproducingOccupant(color, self.get_size(), self.get_speed(), self)
        return ReproducingOccupant(self.get_color(), self.get_size(), self.get_speed(), self)

    def reproducing(self):
        return self.__reproducing

    def update(self):
        """makes the creature change direction occasionally"""
        if random.random() < .13:
            self.set_starting_velocity()
        if random.random() < .008:
            self.__reproducing = True
        if self.get_energy() < 0:
            self.die()
        else:
            self.subtract_energy(1)


class Plant(Occupant):
    __x = 0
    __y = 0
    __growth_rate = random.normalvariate(2000,100)
    if __growth_rate < 0:
        __growth_rate = 100
    __counter = __growth_rate

    def __init__(self, x, y):
        Occupant.__init__(self, "#228B22", 10, 0)
        self.__x = x
        self.__y = y

    def update(self):
        if self.__counter < 1 and self.get_size() < 100:
            self.set_size(self.get_size() + 1)
            self.__counter = self.__growth_rate
            self.__energy = self.get_size()
        self.__counter -= 1

    def getx(self):
        return self.__x

    def gety(self):
        return self.__y