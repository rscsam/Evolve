import random

from occupant import Occupant
from scripts import StayStill


class Plant(Occupant):
    """An occupant that does not move, but grows in place"""
    __growth_rate = random.normalvariate(2000, 100)
    if __growth_rate < 0:
        __growth_rate = 100
    __counter = __growth_rate

    def __init__(self, energy):
        g = ["plant", -1, 0, 10, 10, 0, '#228B22', 1, 1, 1, 1, 1, 1, 5]
        behaviors = [[StayStill()], [StayStill()], [StayStill()]]
        Occupant.__init__(self, g, behaviors, energy)
        self.set_base_energy(energy)

    def update(self):
        if self.__counter < 1 and self.get_size() < 230:
            self.set_size(self.get_size() + 1)
            self.__counter = self.__growth_rate
            self.set_energy(self.get_energy() + (self.get_base_energy()/10))
        self.__counter -= 1

    def get_intimidation(self):
        return 0
