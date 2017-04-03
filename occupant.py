import copy
import math
import random

import tools


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
        self.__color_value = int(self.__color[1:], 16)
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

    def to_string(self):
        result = "Size: " + str(self.__size)
        result += "\nSpecies: " + self.__species
        result += "\nColor: " + str(self.__color)
        result += "\nSpeed: " + str(self.__speed)
        result += "\nBurst: " + str(self.__burst)
        result += "\nVision: " + str(self.__vision)
        result += "\nToughness: " + str(self.__toughness)
        return result

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
            result_color = tools.mix_colors(tools.mix_colors(self.__color,
                                                 tools.random_color()), self.__color)
            self.set_color(result_color)
        if random.random() < 0.99:
            m = 0.005
            if random.random() < 0.5:
                m *= -1
            self.__mutation_factors[0] += m
        if random.random() < 0.99:
            m = 0.005
            if random.random() < 0.5:
                m *= -1
            self.__mutation_factors[1] += m
        if random.random() < 0.99:
            m = 0.005
            if random.random() < 0.5:
                m *= -1
            self.__mutation_factors[2] += m
        if random.random() < 0.99:
            m = 0.005
            if random.random() < 0.5:
                m *= -1
            self.__mutation_factors[3] += m
        if random.random() < 0.99:
            m = 0.005
            if random.random() < 0.5:
                m *= -1
            self.__mutation_factors[4] += m
        if random.random() < 0.99:
            m = 0.008
            if random.random() < 0.5:
                m *= -1
            self.__mutation_factors[5] += m
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

    def get_color_value(self):
        return self.__color_value

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
        self.subtract_energy(self.__size * self.__current_speed + self.get_size())

    def set_strength(self, s):
        self.__strength = s

    def get_strength(self):
        return self.__strength

    def get_power(self):
        return self.__strength * self.__size*self.__size

    def set_toughness(self, t):
        self.__toughness = t

    def get_toughness(self):
        return self.__toughness

    def get_intimidation(self):
        return self.__strength + self.__size

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

    def get_nearby_weaker(self, times_weaker):
        nearby = []
        for i in range(0, len(self.__nearby)):
            if times_weaker * self.__nearby[i][0].get_intimidation() <= self.get_intimidation():
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
        self.__current_speed = math.sqrt((xv*xv)+(yv*yv))

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


def similarity(o1, o2):
    similar = -3
    cv1 = o1.get_color_value()
    cv2 = o2.get_color_value()

    similar += int(abs((((cv1 << 26) >> 26) & 0x3F) - (((cv2 << 26) >> 26) & 0x3F))/5) #compares red color
    similar += int(abs((((cv1 << 20) >> 26) & 0x3F) - (((cv2 << 20) >> 26) & 0x3F))/5) #compares green color
    similar += int(abs((((cv1 << 14) >> 26) & 0x3F) - (((cv2 << 14) >> 26) & 0x3F))/5) #bcompares blue color
    similar += abs(o1.get_size() - o2.get_size())
    similar += abs(o1.get_speed() - o2.get_speed())
    similar += abs(o1.get_strength() - o2.get_strength())
    similar += abs(o1.get_toughness() - o2.get_toughness())
    return similar
