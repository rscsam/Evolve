"""The module that contains all of the backend creature data"""

import random
import math


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
    __genecode = "O5200FF00"
    __mutationfactor = 10  # 0 for no mutation, 1000 for complete randomisation
    __species = "O"

    def __init__(self, genecode):
        self.__genecode = genecode
        self.set_starting_velocity()
        color = "#" + genecode[3] + genecode[4] + genecode[5] + genecode[6] + genecode[7] + genecode[8]
        super(ReproducingOccupant, self).__init__(color, genecode[1], genecode[2])

    def mutate(self):
        species = self.__genecode[0]
        size = self.__genecode[1]
        speed = self.__genecode[2]
        if random.randint(0, 1000) < self.__mutationfactor:
            species -= 1
        if random.randint(0, 1000) < self.__mutationfactor:
            size += 1
        if random.randint(0, 1000) < self.__mutationfactor:
            speed += 1
        return "" + species + size + speed
