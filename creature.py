"""The module that contains all of the backend creature data"""

from occupant import Occupant
from scripts import *


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


class Creature(ReproducingOccupant):
    def reproduce(self):
        self.set_reproducing(False)
        self.set_energy(self.get_base_energy())
        return Creature(self.get_gencode(), self.get_behaviors(), self.get_base_energy(), self)

    def update(self):
        """makes the creature change direction occasionally"""
        if self.get_energy() > math.sqrt(self.get_size()) * self.get_base_energy():
            self.set_reproducing(True)
        Occupant.update(self)
