from tools import *
from creature import *
import math
import random


class Spawner:
    __timer = 0
    __current_time = 0
    __height = 0
    __width = 0
    __x = 0
    __y = 0
    __plants = []
    __spawning = False
    __spawn_x = 0
    __spawn_y = 0

    def __init__(self, timer, height, width, x, y):
        self.__timer = timer
        self.__current_time = timer
        self.__height = height
        self.__width = width
        self.__x = x
        self.__y = y

    def _update(self):
        self.__current_time -= 1
        if self.__current_time <= 0:
            self._spawning = True
            self.__current_time = self.__timer

    def _spawn(self):
        self.__spawn_x = (random.random() * (self.__width)) + self.__x
        self.__spawn_y = (random.random() * (self.__height)) + self.__y
        shade = self._calculate_shade(self.__spawn_x, self.__spawn_y)
        self.__spawning = False
        if random.random() > shade:
            return Plant(self.__spawn_x, self.__spawn_y)

    def _calculate_shade(self, x, y):
        shade = 0
        for plant in self.__plants:
            size = 2 * plant._getSize()
            distance = math.sqrt(math.pow((x - plant.__get_x), 2) - math.pow((y - plant.__get_y), 2))
            shade += (size/distance)
        return shade

    def __get_spawn_x(self):
        return self.__spawn_x

    def __get_spawn_y(self):
        return self.__spawn_y