"""The module that contains all of the backend creature data"""

import tools
from scripts import *


class Occupant:
    """Defines a parallel to tangible, visible, interacting occupants inside the world"""
    __size = 0
    __speed = 0
    __y_velocity = 0
    __x_velocity = 0
    __burst = 0
    __color = "#FFFFFF"
    __alive = True
    __energy = 1000
    __strength = 0
    __vision = -1
    needs_vision = False
    __nearby = []
    scripts = {"": None}
    __current_script = None

    def __init__(self, color, size, speed):
        self.__color = color
        self.__size = size
        self.__speed = speed
        self.__nearby.clear()
        self.scripts.clear()

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
        self.__current_script.set_max_speed(speed)

    def get_speed(self):
        return self.__speed

    def set_burst(self, burst):
        self.__burst = burst

    def get_burst(self):
        return self.__burst

    def get_energy(self):
        return self.__energy

    def set_energy(self, e):
        self.__energy = e

    def extract_energy(self):
        extracted = self.__size * self.__energy / 20
        self.__energy = 0
        return extracted

    def get_strength(self):
        return self.__strength

    def set_strength(self, s):
        self.__strength = s

    def get_power(self):
        return self.__strength * self.__energy

    def add_energy(self, e):
        self.__energy += e

    def subtract_energy(self, e):
        self.__energy -= e

    def get_vision(self):
        return self.__vision

    def set_vision(self, v):
        self.__vision = v

    def get_nearby(self):
        return self.__nearby

    def get_nearby_plants(self):
        nearby = []
        for i in range(0, len(self.__nearby)):
            if isinstance(self.__nearby[i][0], Plant):
                nearby.append(self.__nearby[i])
        return nearby

    def set_nearby(self, n):
        self.__nearby = n

    def die(self):
        self.__alive = False

    def alive(self):
        return self.__alive

    def get_current_script(self):
        return self.__current_script

    def set_current_script(self, s):
        self.__current_script = s

    def adjust_velocity(self):
        self.set_x_velocity(self.get_current_script().get_x_velocity())
        self.set_y_velocity(self.get_current_script().get_y_velocity())

    def update(self):
        """changes the position of the occupant"""
        self.__current_script.update()
        self.adjust_velocity()


class ConvenientOccupant(Occupant):
    """An occupant designed to do whatever helps with debugging"""
    def __init__(self, color, size, speed):
        Occupant.__init__(self, color, size, speed)
        self.needs_vision = True
        self.set_vision(300)
        self.set_burst(9)
        self.scripts.clear()
        self.scripts["Main"] = MoveTowardPlants()
        self.set_current_script(self.scripts["Main"])
        self.get_current_script().load(self)
        self.adjust_velocity()


class Squawker(Occupant):
    """An occupant that moves according to the famous S Q U A W K B O Y S movement algorithm"""
    def __init__(self, color, size, speed):
        Occupant.__init__(self, color, size, speed)
        self.scripts.clear()
        self.scripts["Main"] = MoveLikeSquawker()
        self.set_current_script(self.scripts["Main"])
        self.get_current_script().load(self)
        self.adjust_velocity()


class ReproducingOccupant(Occupant):
    """An occupant capable of reproducing"""
    __reproducing = False
    __parent = None

    def __init__(self, color, size, speed, parent):
        Occupant.__init__(self, color, size, speed)
        self.__parent = parent
        self.scripts.clear()
        self.scripts["Main"] = MoveLikeSquawker()
        self.set_current_script(self.scripts["Main"])
        self.get_current_script().load(self)
        self.get_current_script().set_random_seed(0.2)
        self.adjust_velocity()

    def get_parent(self):
        return self.__parent

    def set_reproducing(self, tf):
        self.__reproducing = tf

    def reproduce(self):
        self.__reproducing = False
        if random.random() < .33:
            color = tools.mix_colors(tools.mix_colors(self.get_color(), tools.random_color()), self.get_color())
            color = tools.mix_colors(self.get_color(), color)
            return ReproducingOccupant(color, self.get_size(), self.get_speed(), self)
        return ReproducingOccupant(self.get_color(), self.get_size(), self.get_speed(), self)

    def reproducing(self):
        return self.__reproducing

    def update(self):
        """makes the creature change direction occasionally"""
        if random.random() < .008:
            self.__reproducing = True
        if self.get_energy() < 0:
            self.die()
        else:
            self.subtract_energy(1)
        Occupant.update(self)


class Plant(Occupant):
    """An occupant that does not move, but grows in place"""
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


class Herbivore(ReproducingOccupant):
    def __init__(self, color, size, speed, parent):
        ReproducingOccupant.__init__(self, color, size, speed, parent)
        self.needs_vision = True
        self.set_vision(int(random.random()*400))
        self.set_burst(4)
        self.set_strength(1)
        self.scripts.clear()
        self.scripts["Main"] = MoveTowardPlants()
        self.set_current_script(self.scripts["Main"])
        self.get_current_script().load(self)
        self.adjust_velocity()

    def reproduce(self):
        self.set_reproducing(False)
        if random.random() < .5:
            color = tools.mix_colors(tools.mix_colors(self.get_color(), tools.random_color()), self.get_color())
            return Herbivore(color, self.get_size(), self.get_speed(), self)
        return Herbivore(self.get_color(), self.get_size(), self.get_speed(), self)

    def update(self):
        """makes the creature change direction occasionally"""
        if self.get_energy() > 2000:
            if random.random() < .007:
                self.subtract_energy(1000)
                self.set_reproducing(True)
        if self.get_energy() < 0:
            self.die()
        else:
            self.subtract_energy(1)
        Occupant.update(self)


class Carnivore(ReproducingOccupant):
    def __init__(self, color, size, speed, parent):
        ReproducingOccupant.__init__(self, color, size, speed, parent)
        self.needs_vision = True
        self.set_vision(int(random.random()*400))
        self.set_burst(4)
        self.set_strength(5)
        self.scripts.clear()
        self.scripts["Main"] = MoveTowardPlants()
        self.set_current_script(self.scripts["Main"])
        self.get_current_script().load(self)
        self.adjust_velocity()