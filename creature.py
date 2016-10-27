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
    __toughness = 1
    __vision = -1
    __mutation_factors = [1, 1, 1, 1, 1, 1, 1]
    needs_vision = False
    __nearby = []
    scripts = {"": None}
    __current_script = None

    def __init__(self, color, size, speed, burst, vision, strength, energy):
        self.__color = color
        self.__size = size
        self.__speed = speed
        self.__burst = burst
        self.__vision = vision
        if self.__vision > 0:
            self.needs_vision = True
        self.__strength = strength
        self.__nearby.clear()
        self.__energy = energy
        self.scripts.clear()

    # Properties and property logic
    def randomize_properties(self, seed):
        self.__vision = int(seed * random.random())
        seed /= 10
        rand = random.random() * seed
        self.__strength = int(rand)
        seed = int(seed - rand)
        rand = random.random() * seed
        self.set_size(int(rand))
        seed = int(seed - rand)
        rand = random.random() * seed
        self.__speed = int(rand)/3
        if self.__speed < 1:
            if random.random() < 0.8:
                self.__speed = 1
        seed = int(seed - rand)
        rand = random.random() * seed
        self.__burst = int(seed - rand)
        self.__color = tools.random_color()

    # mutation_factors[0] = vision
    # mutation_factors[1] = strength
    # mutation_factors[2] = size
    # mutation_factors[3] = speed
    # mutation_factors[4] = burst
    # mutation_factors[5] = color
    def mutate_properties(self):
        if self.__mutation_factors[0] < random.random():
            m = 1
            if random.random() < 0.5:
                m = -1
            self.__vision += m
        if self.__mutation_factors[1] < random.random():
            m = 1
            if random.random() < 0.5:
                m = -1
            self.__strength += m
        if self.__mutation_factors[2] < random.random():
            m = 1
            if random.random() < 0.5:
                m = -1
            self.set_size(self.__size + m)
        if self.__mutation_factors[3] < random.random():
            m = 1
            if random.random() < 0.5:
                m = -1
            self.__speed += m
        if self.__mutation_factors[4] < random.random():
            m = 1
            if random.random() < 0.5:
                m = -1
            self.__burst += m
        if self.__mutation_factors[5] < random.random():
            self.set_color(tools.mix_colors(tools.mix_colors(self.get_color(), tools.random_color()), self.get_color()))

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

    def set_x_velocity(self, x):
        self.__x_velocity = x

    def get_x_velocity(self):
        return self.__x_velocity

    def set_y_velocity(self, y):
        self.__y_velocity = y

    def get_y_velocity(self):
        return self.__y_velocity

    def hit_side(self):
        self.set_x_velocity(self.get_x_velocity() * -1)

    def hit_lid(self):
        self.set_y_velocity(self.get_y_velocity() * -1)

    def set_color(self, color):
        self.__color = color

    def get_color(self):
        return self.__color

    def set_size(self, size):
        if size < 1:
            size = 1
        self.__size = size

    def get_size(self):
        return self.__size

    def get_base_energy(self):
        return self.__base_energy

    def set_energy(self, e):
        self.__energy = e

    def get_energy(self):
        return self.__energy

    def extract_energy(self):
        extracted = self.__size * self.__energy / (self.get_toughness()+1)
        self.__energy = 0
        return extracted

    def add_energy(self, e):
        self.__energy += e

    def subtract_energy(self, e):
        self.__energy -= e

    def respire(self):
        self.subtract_energy(self.__size * self.__current_speed/3 + self.get_size())

    def set_strength(self, s):
        self.__strength = s

    def get_strength(self):
        return self.__strength

    def get_power(self):
        return self.__strength * self.__energy * (self.__size**2)

    def set_toughness(self, t):
        self.__toughness = t

    def get_toughness(self):
        return self.__toughness

    def set_vision(self, v):
        self.__vision = v

    def get_vision(self):
        return self.__vision

    def set_mutation_factors(self, mf):
        self.__mutation_factors = mf

    def get_mutation_factors(self):
        return self.__mutation_factors

    def set_nearby(self, n):
        self.__nearby = n

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

    # Living and dying logic
    def die(self):
        self.__alive = False

    def alive(self):
        return self.__alive

    # Script logic
    def set_current_script(self, s):
        self.__current_script = s

    def get_current_script(self):
        return self.__current_script

    def adjust_velocity(self):
        xv = self.get_current_script().get_x_velocity()
        yv = self.get_current_script().get_y_velocity()
        self.set_x_velocity(xv)
        self.set_y_velocity(yv)
        self.__current_speed = ((xv**2)+(yv**2))**0.5

    # Main loop
    def update(self):
        """changes the position of the occupant"""
        self.__current_script.update()
        self.adjust_velocity()
        self.respire()
        if self.get_energy() < 0:
            self.die()


class ConvenientOccupant(Occupant):
    """An occupant designed to do whatever helps with debugging"""

    def __init__(self, color, size, speed, burst, vision, strength, energy):
        Occupant.__init__(self, color, size, speed, burst, vision, strength, energy)
        self.scripts.clear()
        self.scripts["Main"] = MoveLikeSquawker()
        self.set_current_script(self.scripts["Main"])
        self.get_current_script().load(self)
        self.adjust_velocity()


class Squawker(Occupant):
    """An occupant that moves according to the famous S Q U A W K B O Y S movement algorithm"""

    def __init__(self, color, size, speed, burst, vision, strength, energy):
        Occupant.__init__(self, color, size, speed, burst, vision, strength, energy)
        self.scripts.clear()
        self.scripts["Main"] = MoveLikeSquawker()
        self.set_current_script(self.scripts["Main"])
        self.get_current_script().load(self)
        self.adjust_velocity()


class ReproducingOccupant(Occupant):
    """An occupant capable of reproducing"""
    __reproducing = False
    __parent = None

    def __init__(self, color, size, speed, burst, vision, strength, energy, parent):
        Occupant.__init__(self, color, size, speed, burst, vision, strength, energy)
        mf = [1, 1, 1, 1, 1, 0.67]
        self.set_mutation_factors(mf)
        self.mutate_properties()
        self.__parent = parent
        self.scripts.clear()
        self.scripts["Main"] = MoveLikeSquawker()
        self.set_current_script(self.scripts["Main"])
        self.get_current_script().load(self)
        self.adjust_velocity()

    def get_parent(self):
        return self.__parent

    def set_reproducing(self, tf):
        self.__reproducing = tf

    def reproduce(self):
        self.__reproducing = False
        return ReproducingOccupant(self.get_color(), self.get_size(), self.get_speed(), self.get_burst(),
                                   self.get_vision(), self.get_strength(), self.get_base_energy(), self)

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
        Occupant.__init__(self, "#228B22", 10, 0, 0, -1, 0, energy)
        self.set_toughness(10)
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
    def __init__(self, color, size, speed, burst, vision, strength, energy, parent):
        ReproducingOccupant.__init__(self, color, size, speed, burst, vision, strength, energy, parent)
        mf = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
        self.set_mutation_factors(mf)
        self.mutate_properties()
        self.set_toughness(5)
        self.scripts.clear()
        self.scripts["Main"] = MoveTowardPlants()
        self.set_current_script(self.scripts["Main"])
        self.get_current_script().load(self)
        self.adjust_velocity()

    def reproduce(self):
        self.set_reproducing(False)
        self.set_energy(self.get_energy()/2)
        return Herbivore(self.get_color(), self.get_size(), self.get_speed(), self.get_burst(),
                         self.get_vision(), self.get_strength(), self.get_base_energy(), self)

    def update(self):
        """makes the creature change direction occasionally"""
        if self.get_energy() > 2*self.get_base_energy():
            if random.random() < 0.5:
                self.set_reproducing(True)
        Occupant.update(self)


class Carnivore(ReproducingOccupant):
    def __init__(self, color, size, speed, burst, vision, strength, energy, parent):
        ReproducingOccupant.__init__(self, color, size, speed, burst, vision, strength, energy, parent)
        mf = [0.9, 0.9, 0.9, 0.9, 0.9, 0.7]
        self.set_mutation_factors(mf)
        self.mutate_properties()
        self.set_toughness(2)
        self.scripts.clear()
        self.scripts["Main"] = HuntHerbivores()
        self.set_current_script(self.scripts["Main"])
        self.get_current_script().load(self)
        self.adjust_velocity()

    def reproduce(self):
        self.set_reproducing(False)
        self.set_energy(self.get_energy()/2)
        return Carnivore(self.get_color(), self.get_size(), self.get_speed(), self.get_burst(),
                         self.get_vision(), self.get_strength(), self.get_base_energy(), self)

    def update(self):
        """makes the creature change direction occasionally"""
        if self.get_energy() > 4*self.get_base_energy():
            if random.random() < .0001:
                self.set_reproducing(True)
        Occupant.update(self)


class PassiveCarnivore(ReproducingOccupant):
    def __init__(self, color, size, speed, burst, vision, strength, energy, parent):
        ReproducingOccupant.__init__(self, color, size, speed, burst, vision, strength, energy, parent)
        mf = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
        self.set_mutation_factors(mf)
        self.mutate_properties()
        self.set_toughness(2)
        self.scripts.clear()
        self.scripts["Main"] = HuntHerbivores()
        self.set_current_script(self.scripts["Main"])
        self.get_current_script().load(self)
        self.scripts["Main"].load_subscript(StayStill())
        self.adjust_velocity()

    def reproduce(self):
        self.set_reproducing(False)
        self.set_energy(self.get_energy()/2)
        return PassiveCarnivore(self.get_color(), self.get_size(), self.get_speed(), self.get_burst(),
                                self.get_vision(), self.get_strength(), self.get_base_energy(), self)

    def update(self):
        """makes the creature change direction occasionally"""
        if self.get_energy() > 4*self.get_base_energy():
            if random.random() < .001:
                self.set_reproducing(True)
        Occupant.update(self)


class Omnivore(ReproducingOccupant):
    def __init__(self, color, size, speed, burst, vision, strength, energy, parent):
        ReproducingOccupant.__init__(self, color, size, speed, burst, vision, strength, energy, parent)
        mf = [0.9, 0.9, 0.9, 0.9, 0.9, 0.7]
        self.set_mutation_factors(mf)
        self.mutate_properties()
        self.set_toughness(2)
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
        return Omnivore(self.get_color(), self.get_size(), self.get_speed(), self.get_burst(),
                        self.get_vision(), self.get_strength(), self.get_base_energy(), self)

    def update(self):
        """makes the creature change direction occasionally"""
        if self.get_energy() > 4*self.get_base_energy():
            if random.random() < .001:
                self.set_reproducing(True)
        Occupant.update(self)
