"""The module that contains all of the backend creature data"""

import tools
from scripts import *


class Occupant:
    """Defines a parallel to tangible, visible, interacting occupants inside the world"""
    __size = 0
    __speed = 0
    __current_speed = 0
    __y_velocity = 0
    __x_velocity = 0
    __burst = 0
    __color = "#FFFFFF"
    __alive = True
    __base_energy = 10000
    __energy = __base_energy
    __strength = 0
    __vision = -1
    needs_vision = False
    __nearby = []
    scripts = {"": None}
    __current_script = None

    def __init__(self, color, size, speed, energy):
        self.__color = color
        self.__size = size
        self.__speed = speed
        self.__nearby.clear()
        self.__energy = energy
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

    def get_current_speed(self):
        return self.__current_speed

    def set_burst(self, burst):
        self.__burst = burst

    def get_burst(self):
        return self.__burst

    def get_base_energy(self):
        return self.__base_energy

    def get_energy(self):
        return self.__energy

    def set_energy(self, e):
        self.__energy = e

    def extract_energy(self):
        extracted = self.__size * self.__energy / 10
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

    def respire(self):
        self.subtract_energy(self.__size * self.__current_speed/3 + self.get_size())

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

    def get_nearby_herbivores(self):
        nearby = []
        for i in range(0, len(self.__nearby)):
            if isinstance(self.__nearby[i][0], Herbivore):
                nearby.append(self.__nearby[i])
        return nearby

    def get_nearby_meat(self):
        nearby = []
        for i in range(0, len(self.__nearby)):
            if not isinstance(self.__nearby[i][0], Plant):
                if self.__nearby[i][0].get_color() is not self.__color\
                    and (not isinstance(self, ReproducingOccupant)
                        and not isinstance(self.__nearby[i][0], ReproducingOccupant))\
                    and isinstance(self, ReproducingOccupant)\
                    and self.__nearby[i][0].get_parent() != self\
                        and self.get_parent():
                        nearby.append(self.get_nearby()[i][0])
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
        xv = self.get_current_script().get_x_velocity()
        yv = self.get_current_script().get_y_velocity()
        self.set_x_velocity(xv)
        self.set_y_velocity(yv)
        self.__current_speed = ((xv**2)+(yv**2))**0.5

    def update(self):
        """changes the position of the occupant"""
        self.__current_script.update()
        self.adjust_velocity()


class ConvenientOccupant(Occupant):
    """An occupant designed to do whatever helps with debugging"""
    def __init__(self, color, size, speed, energy):
        Occupant.__init__(self, color, size, speed, energy)
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
    def __init__(self, color, size, speed, energy):
        Occupant.__init__(self, color, size, speed, energy)
        self.scripts.clear()
        self.scripts["Main"] = MoveLikeSquawker()
        self.set_current_script(self.scripts["Main"])
        self.get_current_script().load(self)
        self.adjust_velocity()


class ReproducingOccupant(Occupant):
    """An occupant capable of reproducing"""
    __reproducing = False
    __parent = None

    def __init__(self, color, size, speed, energy, parent):
        Occupant.__init__(self, color, size, speed, energy)
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
            return ReproducingOccupant(color, self.get_size(), self.get_speed(), self.get_base_energy(), self)
        return ReproducingOccupant(self.get_color(), self.get_size(), self.get_speed(), self.get_base_energy(), self)

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
    __growth_rate = random.normalvariate(2000, 100)
    if __growth_rate < 0:
        __growth_rate = 100
    __counter = __growth_rate

    def __init__(self, x, y, energy):
        Occupant.__init__(self, "#228B22", 10, 0, energy)
        self.__x = x
        self.__y = y

    def update(self):
        if self.__counter < 1 and self.get_size() < 230:
            self.set_size(self.get_size() + 1)
            self.__counter = self.__growth_rate
            self.__energy = self.get_size()
        self.__counter -= 1

    def getx(self):
        return self.__x

    def gety(self):
        return self.__y


class Herbivore(ReproducingOccupant):
    def __init__(self, color, size, speed, parent, energy):
        ReproducingOccupant.__init__(self, color, size, speed, parent, energy)
        self.needs_vision = True
        self.set_vision(int(random.random()*400))
        self.set_burst(3)
        self.set_strength(1)
        self.scripts.clear()
        self.scripts["Main"] = MoveTowardPlants()
        self.set_current_script(self.scripts["Main"])
        self.get_current_script().load(self)
        self.adjust_velocity()

    def reproduce(self):
        self.set_reproducing(False)
        self.set_energy(self.get_energy()/2)
        if random.random() < .1:
            color = tools.mix_colors(tools.mix_colors(self.get_color(), tools.random_color()), self.get_color())
            return Herbivore(color, self.get_size(), self.get_speed(), self.get_energy(), self)
        return Herbivore(self.get_color(), self.get_size(), self.get_speed(), self.get_energy(), self)

    def update(self):
        """makes the creature change direction occasionally"""
        if self.get_energy() > self.get_base_energy():
            if random.random() < 0.5:
                self.set_reproducing(True)
        if self.get_energy() < 0:
            self.die()
        else:
            self.respire()
        Occupant.update(self)


class Carnivore(ReproducingOccupant):
    def __init__(self, color, size, speed, energy, parent):
        ReproducingOccupant.__init__(self, color, size, speed, energy, parent)
        self.needs_vision = True
        self.set_vision(int(random.random()*600))
        self.set_burst(2)
        self.set_strength(1000)
        self.scripts.clear()
        self.scripts["Main"] = HuntHerbivores()
        self.set_current_script(self.scripts["Main"])
        self.get_current_script().load(self)
        self.adjust_velocity()

    def reproduce(self):
        self.set_reproducing(False)
        self.set_energy(self.get_energy()/2)
        if random.random() < .3:
            color = tools.mix_colors(tools.mix_colors(self.get_color(), tools.random_color()), self.get_color())
            return Carnivore(color, self.get_size(), self.get_speed(), self.get_energy(), self)
        return Carnivore(self.get_color(), self.get_size(), self.get_speed(), self.get_energy(), self)

    def update(self):
        """makes the creature change direction occasionally"""
        if self.get_energy() > 4*self.get_base_energy():
            if random.random() < .0001:
                self.set_reproducing(True)
        if self.get_energy() < 0:
            self.die()
        else:
            self.respire()
        Occupant.update(self)

class PassiveCarnivore(ReproducingOccupant):
    def __init__(self, color, size, speed, energy, parent):
        ReproducingOccupant.__init__(self, color, size, speed, energy, parent)
        self.needs_vision = True
        self.set_vision(int(random.random()*600))
        self.set_burst(2)
        self.set_strength(1000)
        self.scripts.clear()
        self.scripts["Main"] = HuntHerbivores()
        self.set_current_script(self.scripts["Main"])
        self.get_current_script().load(self)
        self.scripts["Main"].load_subscript(StayStill())
        self.adjust_velocity()

    def reproduce(self):
        self.set_reproducing(False)
        self.set_energy(self.get_energy()/2)
        if random.random() < .3:
            color = tools.mix_colors(tools.mix_colors(self.get_color(), tools.random_color()), self.get_color())
            return PassiveCarnivore(color, self.get_size(), self.get_speed(), self.get_energy(), self)
        return PassiveCarnivore(self.get_color(), self.get_size(), self.get_speed(), self.get_energy(), self)

    def update(self):
        """makes the creature change direction occasionally"""
        if self.get_energy() > 4*self.get_base_energy():
            if random.random() < .001:
                self.set_reproducing(True)
        if self.get_energy() < 0:
            self.die()
        else:
            self.respire()
        Occupant.update(self)


class Omnivore(ReproducingOccupant):
    def __init__(self, color, size, speed, energy, parent):
        ReproducingOccupant.__init__(self, color, size, speed, energy, parent)
        self.needs_vision = True
        self.set_vision(int(random.random()*600))
        self.set_burst(2)
        self.set_strength(1000)
        self.scripts.clear()
        self.scripts["Main"] = HuntHerbivores()
        self.set_current_script(self.scripts["Main"])
        self.get_current_script().load(self)
        self.scripts["Main"].load_subscript(MoveTowardPlants())
        self.scripts["Main"].subscript.load_subscript(StayStill())
        self.adjust_velocity()

    def reproduce(self):
        self.set_reproducing(False)
        self.set_energy(self.get_energy()/2)
        if random.random() < .3:
            color = tools.mix_colors(tools.mix_colors(self.get_color(), tools.random_color()), self.get_color())
            return Omnivore(color, self.get_size(), self.get_speed(), self.get_energy(), self)
        return Omnivore(self.get_color(), self.get_size(), self.get_speed(), self.get_energy(), self)

    def update(self):
        """makes the creature change direction occasionally"""
        if self.get_energy() > 4*self.get_base_energy():
            if random.random() < .001:
                self.set_reproducing(True)
        if self.get_energy() < 0:
            self.die()
        else:
            self.respire()
        Occupant.update(self)