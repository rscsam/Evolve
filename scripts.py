import random

class Script:
    '''reference = (0, 0)'''
    __x_offset = 0
    __y_offset = 0
    __nearby = []
    __max_speed = 0
    __adjustmentx = 0
    __adjustmenty = 0
    __occupant = None

    def get_adjustmentx(self):
        return self.__adjustmentx

    def set_adjustmentx(self, x):
        self.__adjustmentx = x

    def get_adjustmenty(self):
        return self.__adjustmenty

    def set_adjustmenty(self, y):
        self.__adjustmenty = y

    def get_max_speed(self):
        return self.__max_speed

    def get_nearby(self):
        return self.__nearby

    def _get_x_offset(self):
        return self.__x_offset

    def _get_y_offset(self):
        return self.__y_offset

    def update(self):
        """Change the adjustments"""

    def load(self, occupant):
        self.__occupant = occupant
        self.__max_speed = occupant.get_speed()

    def stop(self):
        self.__occupant = None
        self.__max_speed = 0
        self.__nearby = []


class StayStill(Script):
    def load(self, occupant):
        Script.load(self, occupant)
        self.set_adjustmentx(0)
        self.set_adjustmenty(0)


class MoveStraightRight(Script):
    def load(self, occupant):
        Script.load(self, occupant)
        self.set_adjustmentx(self.get_max_speed())
        self.set_adjustmenty(0)


class MoveStraightLeft(Script):
    def load(self, occupant):
        Script.load(self, occupant)
        self.set_adjustmentx(self.get_max_speed() * -1)
        self.set_adjustmenty(0)


class MoveStraightUp(Script):
    def load(self, occupant):
        Script.load(self, occupant)
        self.set_adjustmentx(0)
        self.set_adjustmenty(self.get_max_speed() * -1)


class MoveStraightDown(Script):
    def load(self, occupant):
        Script.load(self, occupant)
        self.set_adjustmentx(0)
        self.set_adjustmenty(self.get_max_speed())


class MoveLikeSquawker(Script):
    def update(self):
        if random.random() < .03:
            ms = self.get_max_speed()
            ax = random.random() * ms
            if random.random() > .5:
                ax *= -1
            ay = ((ms**2) - (ax**2)) ** 0.5
            if random.random() > .5:
                ay *= -1
            self.set_adjustmentx(ax)
            self.set_adjustmenty(ay)
