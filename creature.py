"""The module that contains all of the backend creature data"""

import copy

import tools
from scripts import *


class Occupant:
    """Defines a parallel to tangible, visible, interacting occupants inside the world"""

    def __init__(self, g, behaviors, energy):
        """GenCode: An array containing each individual gene
                        G[0] = special identifier
                        G[1] = vision
                        G[2] = strength
                        G[3] = size
                        G[4] = speed
                        G[5] = burst
                        G[6] = color
                        G[7] = vision mf
                        G[8] = strength mf
                        G[9] = size mf
                        G[10] = speed mf
                        G[11] = burst mf
                        G[12] = color mf
                        G[13] = toughness"""
        self.__size = 0
        self.__speed = 0
        self.__current_speed = 0
        self.__y_velocity = 0
        self.__x_velocity = 0
        self.__alive = True
        self.__species = ""
        self.__gencode = []
        self.__base_energy = 10000
        self.needs_vision = False

        self.__gencode = g
        self.__species = g[0]
        self.__color = g[6]
        self.__size = g[3]
        self.__speed = g[4]
        self.__burst = g[5]
        self.__vision = g[1]
        if self.__vision > 0:
            self.needs_vision = True
        self.__strength = g[2]
        self.__mutation_factors = [g[7], g[8], g[9], g[10], g[11], g[12]]
        self.__toughness = g[13]
        self.__nearby = []
        self.__energy = energy

        self.__scripts = {"": None}
        self.__behaviors = behaviors
        self.__scripts.clear()
        curr = copy.deepcopy(behaviors[0][0])
        self.__scripts["Main"] = curr
        self.__scripts["Main"].load(self)
        for i in range(1, len(behaviors[0])):
            curr = curr.load_subscript(copy.deepcopy(behaviors[0][i]))
        curr = copy.deepcopy(behaviors[1][0])
        self.__scripts["Hungry"] = curr
        self.__scripts["Hungry"].load(self)
        for i in range(1, len(behaviors[1])):
            curr = curr.load_subscript(copy.deepcopy(behaviors[1][i]))
        curr = copy.deepcopy(behaviors[2][0])
        self.__scripts["Scared"] = curr
        self.__scripts["Scared"].load(self)
        for i in range(1, len(behaviors[2])):
            curr = curr.load_subscript(copy.deepcopy(behaviors[2][i]))
        self.__current_script = self.__scripts["Main"]

    # Properties and property logic
    def set_gencode(self, g):
        self.__gencode = g

    def get_gencode(self):
        return self.__gencode

    def get_species(self):
        return self.__species

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
        self.set_gencode(self.generate_gencode())

    # mutation_factors[0] = vision
    # mutation_factors[1] = strength
    # mutation_factors[2] = size
    # mutation_factors[3] = speed
    # mutation_factors[4] = burst
    # mutation_factors[5] = color
    def mutate_properties(self):
        changed = False
        change = 0
        if self.__mutation_factors[0] < random.random():
            change += 1
            m = 1
            if random.random() < 0.5:
                m = -1
            self.__vision += m
        if self.__mutation_factors[1] < random.random():
            change += 2
            m = 1
            if random.random() < 0.5:
                m = -1
            self.__strength += m
        if self.__mutation_factors[2] < random.random():
            change += 4
            m = 1
            if random.random() < 0.5:
                m = -1
            self.set_size(self.__size + m)
        if self.__mutation_factors[3] < random.random():
            change += 8
            m = 1
            if random.random() < 0.5:
                m = -1
            self.__speed += m
        if self.__mutation_factors[4] < random.random():
            change += 16
            m = 1
            if random.random() < 0.5:
                m = -1
            self.__burst += m
        if self.__mutation_factors[5] < random.random():
            change += 32
            self.set_color(tools.mix_colors(tools.mix_colors(self.get_color(), tools.random_color()), self.get_color()))
        if random.random() < 0.99:
            m = 0.005
            if random.random() < 0.5:
                changed = True
                m *= -1
                self.__mutation_factors[0] += m
        if random.random() < 0.99:
            changed = True
            m = 0.005
            if random.random() < 0.5:
                m *= -1
                self.__mutation_factors[1] += m
        if random.random() < 0.99:
            changed = True
            m = 0.005
            if random.random() < 0.5:
                m *= -1
                self.__mutation_factors[2] += m
        if random.random() < 0.99:
            changed = True
            changed = True
            m = 0.005
            if random.random() < 0.5:
                m *= -1
                self.__mutation_factors[3] += m
        if random.random() < 0.99:
            changed = True
            m = 0.005
            if random.random() < 0.5:
                m *= -1
                self.__mutation_factors[4] += m
        if random.random() < 0.99:
            changed = True
            m = 0.005
            if random.random() < 0.5:
                m *= -1
                self.__mutation_factors[5] += m
        if change != 0:
            if change == 63:
                self.__species += "$"
            elif change <= 10:
                self.__species += chr(change + 47)
            elif change <= 36:
                self.__species += chr(change + 54)
            else:
                self.__species += chr(change + 60)
            self.set_gencode(self.generate_gencode())
        elif changed:
            self.set_gencode(self.generate_gencode())

    def generate_gencode(self):
        """GenCode: An array containing each individual gene
                        G[0] = special identifier
                        G[1] = vision
                        G[2] = strength
                        G[3] = size
                        G[4] = speed
                        G[5] = burst
                        G[6] = color
                        G[7] = vision mf
                        G[8] = strength mf
                        G[9] = size mf
                        G[10] = speed mf
                        G[11] = burst mf
                        G[12] = color mf
                        G[13] = toughness"""
        g = [self.__species, self.__vision, self.__strength, self.__size, self.__speed, self.__burst, self.__color,
             self.__mutation_factors[0], self.__mutation_factors[1], self.__mutation_factors[2],
             self.__mutation_factors[3], self.__mutation_factors[4], self.__mutation_factors[5], self.__toughness]
        return g

    def set_speed(self, speed):
        self.__speed = speed
        self.get_current_script().set_max_speed(speed)

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

    def set_base_energy(self, e):
        self.__base_energy = e

    def get_base_energy(self):
        return self.__base_energy

    def set_energy(self, e):
        self.__energy = e

    def get_energy(self):
        return self.__energy

    def extract_energy(self):
        extracted = self.__size * self.__energy / (self.get_toughness())
        self.__energy = 0
        return extracted

    def add_energy(self, e):
        self.__energy += e

    def subtract_energy(self, e):
        self.__energy -= e
        if self.__energy <= 0:
            self.__energy = 0

    def respire(self):
        self.subtract_energy((self.__size**1.5)*self.__current_speed/3 + self.get_size())

    def set_strength(self, s):
        self.__strength = s

    def get_strength(self):
        return self.__strength

    def get_power(self):
        return self.__strength * ((self.__size**2) + (self.__energy**0.5))

    def set_toughness(self, t):
        self.__toughness = t

    def get_toughness(self):
        return self.__toughness

    def get_intimidation(self):
        return self.__strength + (self.__size**2)

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
    def get_scripts(self):
        return self.__scripts

    def get_behaviors(self):
        return self.__behaviors

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
        if self.__energy < self.get_base_energy():
            if self.get_current_script() is not self.get_scripts()["Hungry"]:
                self.set_current_script(self.get_scripts()["Hungry"])
        else:
            if self.get_current_script() is not self.get_scripts()["Main"]:
                self.set_current_script(self.get_scripts()["Main"])
        self.get_current_script().update()
        self.adjust_velocity()
        self.respire()
        if self.get_energy() <= 0:
            self.die()


class ConvenientOccupant(Occupant):
    """An occupant designed to do whatever helps with debugging"""

    def __init__(self, g, behaviors, energy):
        Occupant.__init__(self, g, behaviors, energy)
        self.randomize_properties(300)
        self.adjust_velocity()


class Squawker(Occupant):
    """An occupant that moves according to the famous S Q U A W K B O Y S movement algorithm"""

    def __init__(self, g, behaviors, energy):
        Occupant.__init__(self, g, behaviors, energy)
        self.get_current_script().load(self)
        self.adjust_velocity()


class ReproducingOccupant(Occupant):
    """An occupant capable of reproducing"""
    __reproducing = False
    __parent = None

    def __init__(self, g, behaviors, energy, parent):
        Occupant.__init__(self, g, behaviors, energy)
        self.mutate_properties()
        self.__parent = parent
        self.adjust_velocity()

    def get_parent(self):
        return self.__parent

    def set_reproducing(self, tf):
        self.__reproducing = tf

    def reproduce(self):
        self.__reproducing = False
        return ReproducingOccupant(self.get_gencode(), self.get_behaviors(), self.get_base_energy(), self)

    def reproducing(self):
        return self.__reproducing

    def update(self):
        """makes the creature change direction occasionally"""
        if random.random() < .008:
            self.__reproducing = True
        Occupant.update(self)


class Plant(Occupant):
    """An occupant that does not move, but grows in place"""
    __growth_rate = random.normalvariate(2000, 100)
    if __growth_rate < 0:
        __growth_rate = 100
    __counter = __growth_rate

    def __init__(self, x, y, energy):
        g = ["plant", -1, 0, 10, 0, 0, '#228B22', 1, 1, 1, 1, 1, 1, 5]
        behaviors = [[StayStill()], [StayStill()], [StayStill()]]
        Occupant.__init__(self, g, behaviors, energy)
        self.set_base_energy(energy*3)
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
    def __init__(self, g, behaviors, energy, parent):
        ReproducingOccupant.__init__(self, g, behaviors, energy, parent)
        self.mutate_properties()

    def reproduce(self):
        self.set_reproducing(False)
        self.set_energy(self.get_energy() / 2)
        return Herbivore(self.get_gencode(), self.get_behaviors(), self.get_base_energy(), self)

    def update(self):
        """makes the creature change direction occasionally"""
        if self.get_energy() > (self.get_size()**0.5)*self.get_base_energy():
            self.set_reproducing(True)
        Occupant.update(self)


class Carnivore(ReproducingOccupant):
    def __init__(self, g, behaviors, energy, parent):
        ReproducingOccupant.__init__(self, g, behaviors, energy, parent)
        self.mutate_properties()
        self.adjust_velocity()

    def reproduce(self):
        self.set_reproducing(False)
        self.set_energy(self.get_energy() / 2)
        return Carnivore(self.get_gencode(), self.get_behaviors(), self.get_base_energy(), self)

    def update(self):
        """makes the creature change direction occasionally"""
        if self.get_energy() > (self.get_size())*self.get_base_energy():
            if random.random() < .0001:
                self.set_reproducing(True)
        Occupant.update(self)


class Omnivore(ReproducingOccupant):
    def __init__(self, g, behaviors, energy, parent):
        ReproducingOccupant.__init__(self, g, behaviors, energy, parent)
        self.mutate_properties()
        self.set_base_energy(30000)
        self.adjust_velocity()

    def reproduce(self):
        self.set_reproducing(False)
        self.set_energy(self.get_energy()/2)
        return Omnivore(self.get_gencode(), self.get_behaviors(), self.get_base_energy(), self)

    def update(self):
        """makes the creature change direction occasionally"""
        if self.get_energy() > (self.get_size()**0.5)*self.get_base_energy():
            self.set_reproducing(True)
        Occupant.update(self)


class VersatileOccupant(ReproducingOccupant):
    def reproduce(self):
        self.set_reproducing(False)
        self.subtract_energy(self.get_base_energy()*2)
        return VersatileOccupant(self.get_gencode(), self.get_behaviors(), self.get_base_energy(), self)

    def update(self):
        """makes the creature change direction occasionally"""
        if self.get_energy() > (self.get_size() ** 0.75) * self.get_base_energy():
            self.set_reproducing(True)
        Occupant.update(self)
