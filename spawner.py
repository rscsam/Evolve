import math
import random

from creature import *


#import tools


class Spawner:
    __timer = 100
    __current_time = 0
    __height = 0
    __width = 0
    __x = 0
    __y = 0
    spawning = False
    __spawn_x = 0
    __spawn_y = 0

    def __init__(self, timer, height, width, x, y):
        self.__timer = timer
        self.__current_time = timer
        self.__height = height
        self.__width = width
        self.__x = x
        self.__y = y

    def update(self):
        self.__current_time -= 1
        if self.__current_time <= 0:
            self.spawning = True
            self.__current_time = self.__timer

    def timer(self):
        return self.__timer

    def get_current_time(self):
        return self.__current_time

    def gct(self):
        return self.get_current_time()

    def set_current_time(self, o):
        self.__current_time = self.__current_time

    def countdown(self):
        self.__current_time -= 1

    def getx(self):
        return self.__x

    def gety(self):
        return self.__y

    def get_height(self):
        return self.__height

    def get_width(self):
        return self.__width

    def set_spawnx(self, x):
        self.__spawn_x = x

    def spawnx(self):
        return self.__spawn_x

    def spawny(self):
        return self.__spawn_y

    def set_spawny(self, y):
        self.__spawn_y = y

    def set_spawning(self, tf):
        self.spawning = tf

    def spawn(self):
        self.__spawn_x = (random.random() * (self.__width)) + self.__x
        self.__spawn_y = (random.random() * (self.__height)) + self.__y
        self.spawning = True
        return Occupant('#696969', 5, 1)


    def get_spawn_x(self):
        return self.__spawn_x

    def get_spawn_y(self):
        return self.__spawn_y


class PlantSpawner(Spawner):
    __plants = []

    def spawn(self):
        self.set_spawnx((random.random() * (self.get_width())) + self.getx())
        self.set_spawny((random.random() * (self.get_height())) + self.gety())
        shade = self._calculate_shade(self.get_spawn_x(), self.get_spawn_y())
        self.set_spawning(False)
        if random.random() > shade:
            return Plant(self.get_spawn_x(), self.get_spawn_y())
        else:
            print("Hi")

    def _calculate_shade(self, x, y):
        shade = 0
        for plant in self.__plants:
            size = 2 * plant.get_size()
            distance = math.sqrt(math.pow((x - plant.__get_x()), 2) - math.pow((y - plant.__get_y()), 2))
            shade += (size/distance)
        return shade


class SpecialSpawner(Spawner):
    __model = None

    def __init__(self, timer, height, width, x, y, occupant):
        Spawner.__init__(self, timer, height, width, x, y)
        self.__model = occupant

    def spawn(self):
        self.set_spawnx((random.random() * (self.get_width())) + self.getx())
        self.set_spawny((random.random() * (self.get_height())) + self.gety())
        self.set_spawning(False)
        return self.__model
