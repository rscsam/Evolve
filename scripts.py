import math
import random


class Script:
    '''reference = (0, 0)'''

    def __init__(self):
        self.nearby = []
        self.x_offset = 0
        self.y_offset = 0
        self.__max_speed = 0
        self.__x_velocity = 0
        self.__y_velocity = 0
        self.__occupant = None
        self.__random_seed = 1
        self.subscript = None

    def get_x_velocity(self):
        return self.__x_velocity

    def set_x_velocity(self, x):
        self.__x_velocity = x

    def get_y_velocity(self):
        return self.__y_velocity

    def set_y_velocity(self, y):
        self.__y_velocity = y

    def get_max_speed(self):
        return self.__max_speed

    def set_max_speed(self, s):
        self.__max_speed = s
        if self.subscript is not None:
            self.subscript.set_max_speed(s)

    def get_nearby(self):
        return self.__nearby

    def get_random_seed(self):
        return self.__random_seed

    def set_random_seed(self, r):
        self.__random_seed = r

    def _get_x_offset(self):
        return self.x_offset

    def _get_y_offset(self):
        return self.y_offset

    def get_occupant(self):
        return self.__occupant

    def update(self):
        """Change the adjustments"""

    def update_subscript(self):
        self.subscript.update()
        self.set_x_velocity(self.subscript.get_x_velocity())
        self.set_y_velocity(self.subscript.get_y_velocity())

    def load(self, occupant):
        self.__occupant = occupant
        self.__max_speed = occupant.get_speed()

    def load_subscript(self, s):
        if self.subscript is not None:
            self.subscript.stop()
        self.subscript = s
        s.load(self.__occupant)
        self.update_subscript()
        return s

    def stop(self):
        self.x_offset = 0
        self.y_offset = 0
        self.__nearby = []
        self.__max_speed = 0
        self.__x_velocity = 0
        self.__y_velocity = 0
        self.__occupant = None
        self.__random_seed = 1
        self.subscript = None


class StayStill(Script):
    def load(self, occupant):
        Script.load(self, occupant)
        self.set_x_velocity(0)
        self.set_y_velocity(0)


class MoveStraightRight(Script):
    def load(self, occupant):
        Script.load(self, occupant)
        self.set_x_velocity(self.get_max_speed())
        self.set_y_velocity(0)


class MoveStraightLeft(Script):
    def load(self, occupant):
        Script.load(self, occupant)
        self.set_x_velocity(self.get_max_speed() * -1)
        self.set_y_velocity(0)


class MoveStraightUp(Script):
    def load(self, occupant):
        Script.load(self, occupant)
        self.set_x_velocity(0)
        self.set_y_velocity(self.get_max_speed() * -1)


class MoveStraightDown(Script):
    def load(self, occupant):
        Script.load(self, occupant)
        self.set_x_velocity(0)
        self.set_y_velocity(self.get_max_speed())


class MoveLikeSquawker(Script):
    def load(self, occupant):
        Script.load(self, occupant)
        self.set_random_seed(.03)
        self._calculate()

    def update(self):
        if random.random() < self.get_random_seed():
            self._calculate()

    def _calculate(self):
        ms = self.get_max_speed()
        ax = random.random() * ms
        if random.random() > .5:
            ax *= -1
        ay = ((ms ** 2) - (ax ** 2)) ** 0.5
        if random.random() > .5:
            ay *= -1
        self.set_x_velocity(ax)
        self.set_y_velocity(ay)


class MoveInCircle(Script):
    __radius = 50
    __tick = 0

    def update(self):
        r = self.__radius
        ms = self.get_max_speed()
        ax = math.cos(self.__tick)
        ay = math.sin(self.__tick)
        m = (ax**2 + ay**2) ** 0.5
        ax /= m
        ay /= m
        ax *= ms
        ay *= ms
        self.x_offset += ax
        self.y_offset += ay
        self.set_x_velocity(ax)
        self.set_y_velocity(ay)
        self.__tick += (ms / (2*math.pi*r))


class MoveInSquare(Script):
    __length = 100
    __tick = 0
    __state = 0
    __states = [MoveStraightRight(), MoveStraightDown(), MoveStraightLeft(), MoveStraightUp()]

    def __init__(self, length):
        Script.__init__(self)
        self.__length = length

    def load(self, occupant):
        Script.load(self, occupant)
        self.load_subscript(self.__states[self.__state])

    def update(self):
        if self.__tick > self.__length:
            self.__state = (self.__state + 1) % 4
            self.load_subscript(self.__states[self.__state])
            Script.update_subscript(self)
            self.__tick = 0
        else:
            self.__tick += 1


class MoveTowardPlants(Script):

    def load(self, occupant):
        Script.load(self, occupant)
        self.load_subscript(StayStill())
        self.nearby = occupant.get_nearby()
        self.update()

    def update(self):
        self.nearby = self.get_occupant().get_nearby_plants()
        minimum = -1
        if len(self.nearby) > 0:
            for i in range(0, len(self.nearby)):
                if i == 0:
                    minimum = i
                elif self.nearby[i][3] < self.nearby[minimum][3]:
                    minimum = i
        else:
            self.update_subscript()
            return
        ms = self.get_max_speed() + self.get_occupant().get_burst()
        xv = self.nearby[minimum][1]
        yv = self.nearby[minimum][2]
        m = self.nearby[minimum][3]
        xv = (xv/m) * ms * -1
        yv = (yv/m) * ms * -1
        if abs(xv) > abs(self.nearby[minimum][1]):
            xv = self.nearby[minimum][1]
        if abs(yv) > abs(self.nearby[minimum][2]):
            yv = self.nearby[minimum][2]
        self.set_x_velocity(xv)
        self.set_y_velocity(yv)


class HuntHerbivores(Script):

    def load(self, occupant):
        Script.load(self, occupant)
        self.load_subscript(MoveLikeSquawker())
        self.nearby = occupant.get_nearby()
        self.update()

    def update(self):
        self.nearby = self.get_occupant().get_nearby_herbivores()
        minimum = -1
        if len(self.nearby) > 0:
            for i in range(0, len(self.nearby)):
                if i == 0:
                    minimum = i
                elif self.nearby[i][3] < self.nearby[minimum][3]:
                    minimum = i
        else:
            self.update_subscript()
            return
        ms = self.get_max_speed() + self.get_occupant().get_burst()
        xv = self.nearby[minimum][1]
        yv = self.nearby[minimum][2]
        m = self.nearby[minimum][3]
        xv = (xv/m) * ms * -1
        yv = (yv/m) * ms * -1
        self.set_x_velocity(xv)
        self.set_y_velocity(yv)


class HuntForMeat(Script):

    def load(self, occupant):
        Script.load(self, occupant)
        self.load_subscript(MoveLikeSquawker())
        self.nearby = occupant.get_nearby()
        self.update()

    def update(self):
        self.nearby = self.get_occupant().get_nearby_meat()
        minimum = -1
        if len(self.nearby) > 0:
            for i in range(0, len(self.nearby)):
                if i == 0:
                    minimum = i
                elif self.nearby[i][3] < self.nearby[minimum][3]:
                    minimum = i
        else:
            self.update_subscript()
            return
        ms = self.get_max_speed() + self.get_occupant().get_burst()
        xv = self.nearby[minimum][1]
        yv = self.nearby[minimum][2]
        m = self.nearby[minimum][3]
        xv = (xv/m) * ms * -1
        yv = (yv/m) * ms * -1
        self.set_x_velocity(xv)
        self.set_y_velocity(yv)
