import math
import random


class Script:
    """A defined movement/action pattern to be carried out by a creature"""

    def __init__(self):
        """Initializes a script"""
        self.nearby = []
        self.x_offset = 0
        self.y_offset = 0
        self.__max_speed = 0
        self.__x_velocity = 0
        self.__y_velocity = 0
        self.__nearby = []
        self.__occupant = None
        self.__random_seed = 1
        self.subscript = None

    def get_x_velocity(self):
        """Getter for x-velocity
            Return:
                the x-velocity"""
        return self.__x_velocity

    def set_x_velocity(self, x):
        """Setter for x-velocity
            Args:
                x: the new x-velocity"""
        self.__x_velocity = x

    def get_y_velocity(self):
        """Getter for y-velocity
            Return:
                the y-velocity"""
        return self.__y_velocity

    def set_y_velocity(self, y):
        """Setter for y-velocity
            Args:
                y: the new y-velocity"""
        self.__y_velocity = y

    def get_max_speed(self):
        """Getter for max speed
            Return:
                the max speed"""
        return self.__max_speed

    def set_max_speed(self, s):
        """Setter for max speed
            Args:
                s: the new max speed"""
        self.__max_speed = s
        if self.subscript is not None:
            self.subscript.set_max_speed(s)

    def get_nearby(self):
        """Getter for the list of nearby creatures
            Return:
                a list containing all nearby creatures"""
        return self.__nearby

    def get_random_seed(self):
        """Getter for random seed
            Return:
                the random seed"""
        return self.__random_seed

    def set_random_seed(self, r):
        """Setter for random seed
            Args:
                r: the new random seed"""
        self.__random_seed = r

    def _get_x_offset(self):
        """Getter for x-offset, which is the x distance from its initial reference point
            Return:
                the x-offset"""
        return self.x_offset

    def _get_y_offset(self):
        """Getter for y-offset, which is the y distance from its initial reference point
            Return:
                the y-offset"""
        return self.y_offset

    def get_occupant(self):
        """Getter for the occupant who is running this script
            Return:
                the occupant"""
        return self.__occupant

    def update(self):
        """The primary loop that contains all script logic which should be overridden in all subclasses"""
        """Handle logic here"""

    def update_subscript(self):
        """Updates the script's subscript and changes velocity accordingly"""
        self.subscript.update()
        self.set_x_velocity(self.subscript.get_x_velocity())
        self.set_y_velocity(self.subscript.get_y_velocity())

    def load(self, occupant):
        """Loads the script with an occupant.  This must always be called before a script can be run
            Args:
                occupant: the occupant that is taking over the script"""
        self.__occupant = occupant
        self.__max_speed = occupant.get_speed()

    def load_subscript(self, s):
        """Loads a subscript into
            Args:
                s: the subscript to load"""
        if self.subscript is not None:
            self.subscript.stop()
        self.subscript = s
        s.load(self.__occupant)
        self.update_subscript()
        return s

    def stop(self):
        """Resets the script to its original state
            Note that this should not be called in order to pause the script,
            as this clears all previous data from the script.  Rather, you
            should use this method when you are switching scripts"""
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
    """A script that makes the occupant not move at all"""

    def load(self, occupant):
        """Loads the script with an occupant.  This must always be called before a script can be run
            Args:
                occupant: the occupant that is taking over the script"""
        Script.load(self, occupant)
        self.set_x_velocity(0)
        self.set_y_velocity(0)


class MoveStraightRight(Script):
    """A script that makes the occupant move straight right"""

    def load(self, occupant):
        """Loads the script with an occupant.  This must always be called before a script can be run
            Args:
                occupant: the occupant that is taking over the script"""
        Script.load(self, occupant)
        self.set_x_velocity(self.get_max_speed())
        self.set_y_velocity(0)


class MoveStraightLeft(Script):
    """A script that makes the occupant move straight left"""

    def load(self, occupant):
        """Loads the script with an occupant.  This must always be called before a script can be run
            Args:
                occupant: the occupant that is taking over the script"""
        Script.load(self, occupant)
        self.set_x_velocity(self.get_max_speed() * -1)
        self.set_y_velocity(0)


class MoveStraightUp(Script):
    """A script that makes the occupant move straight up"""

    def load(self, occupant):
        """Loads the script with an occupant.  This must always be called before a script can be run
            Args:
                occupant: the occupant that is taking over the script"""
        Script.load(self, occupant)
        self.set_x_velocity(0)
        self.set_y_velocity(self.get_max_speed() * -1)


class MoveStraightDown(Script):
    """A script that makes the occupant move straight down"""

    def load(self, occupant):
        """Loads the script with an occupant.  This must always be called before a script can be run
            Args:
                occupant: the occupant that is taking over the script"""
        Script.load(self, occupant)
        self.set_x_velocity(0)
        self.set_y_velocity(self.get_max_speed())


class MoveLikeSquawker(Script):
    """A script that makes the occupant move, then randomly change direction"""

    def load(self, occupant):
        """Loads the script with an occupant.  This must always be called before a script can be run
            Args:
                occupant: the occupant that is taking over the script"""
        Script.load(self, occupant)
        self.set_random_seed(.17)
        self._randomize()

    def update(self):
        """Primary logic loop for the script"""
        if random.random() < self.get_random_seed():
            self._randomize()

    def _randomize(self):
        """Randomizes the occupants direction"""
        ms = self.get_max_speed()
        ax = random.random() * ms
        if random.random() > .5:
            ax *= -1
        ay = math.sqrt(((math.pow(ms, 2)) - math.pow(ax, 2)))
        if random.random() > .5:
            ay *= -1
        self.set_x_velocity(ax)
        self.set_y_velocity(ay)


class MoveInSquare(Script):
    """A script that makes the occupant move in a square of specified length"""
    __length = 0
    __tick = 0
    __state = 0
    __states = [MoveStraightRight(), MoveStraightDown(), MoveStraightLeft(), MoveStraightUp()]

    def __init__(self, length):
        """Initializes the script
            Args:
                length: the length of one side of the square"""
        Script.__init__(self)
        self.__length = length

    def load(self, occupant):
        """Loads the script with an occupant.  This must always be called before a script can be run
            Args:
                occupant: the occupant that is taking over the script"""
        Script.load(self, occupant)
        self.load_subscript(self.__states[self.__state])

    def update(self):
        """Primary logic loop for the script"""
        if self.__tick > self.__length:
            self.__state = (self.__state + 1) % 4
            self.load_subscript(self.__states[self.__state])
            Script.update_subscript(self)
            self.__tick = 0
        else:
            self.__tick += 1


class MoveTowardPlants(Script):
    """A script that makes occupants move towards occupants of class type Plant"""

    def load(self, occupant):
        """Loads the script with an occupant.  This must always be called before a script can be run
            Args:
                occupant: the occupant that is taking over the script"""
        Script.load(self, occupant)
        self.load_subscript(StayStill())
        self.nearby = occupant.get_nearby()
        self.update()

    def update(self):
        """Primary logic loop for the script"""
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


class HuntWeaker(Script):
    """A script that makes the occupant move towards occupants it perceives to be weaker"""

    def load(self, occupant):
        """Loads the script with an occupant.  This must always be called before a script can be run
            Args:
                occupant: the occupant that is taking over the script"""
        Script.load(self, occupant)
        self.load_subscript(MoveLikeSquawker())
        self.nearby = occupant.get_nearby()
        self.update()

    def update(self):
        """Primary logic loop for the script"""
        self.nearby = self.get_occupant().get_nearby_weaker(1.5)
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
        xv = (xv / m) * ms * -1
        yv = (yv / m) * ms * -1
        if abs(xv) > abs(self.nearby[minimum][1]):
            xv = self.nearby[minimum][1]
        if abs(yv) > abs(self.nearby[minimum][2]):
            yv = self.nearby[minimum][2]
        self.set_x_velocity(xv)
        self.set_y_velocity(yv)
