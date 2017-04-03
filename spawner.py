"""This module defines a series of spawners capable of spawning occupants into their world"""

from creature import *
from plant import *

class Spawner:
    """A superclass that defines a spawner capable of keeping track of its own occupants
        and deciding when to spawn a new one in the world it is created in"""

    def __init__(self, timer, height, width, x, y):
        """Initialization logic
            Args:
                timer: the time in update cycles between each attempted spawn
                height: the height of the spawner
                width: the width of the spawner
                x: the x-value of the spawner in its world
                y: the y-value of the spawner in its world"""
        self.__timer = 100
        self.__current_time = 0
        self.__height = 0
        self.__width = 0
        self.__x = 0
        self.__y = 0
        self.spawning = False
        self.__spawn_x = 0
        self.__spawn_y = 0
        self.__special_id = 0
        self.__occupants = []
        self.__init_special_id()
        self.__timer = timer
        self.__current_time = timer
        self.__height = height
        self.__width = width
        self.__x = x
        self.__y = y

    def __init_special_id(self):
        """Initializes a special id used to keep track of occupants by the world"""
        self.__special_id = random.random() * 999999999

    def update(self):
        """The primary logic loop that is run during every cycle of the program"""
        self.__current_time -= 1
        if self.__current_time <= 0:
            self.spawning = True
            self.__current_time = self.__timer

    def timer(self):
        """Getter for the timer
            Return:
                the spawner's timer"""
        return self.__timer

    def get_current_time(self):
        """Getter for the current state of the timer.  If it is zero, it is time to spawn
            Return:
                the current time of the timer"""
        return self.__current_time

    def gct(self):
        """Getter for the current state of the timer.  If it is zero, it is time to spawn
            Return:
                the current time of the timer"""
        return self.get_current_time()

    def set_current_time(self, o):
        """Sets the current state of the timer to a specified value
            Args:
                o: the new current time of the timer"""
        self.__current_time = o

    def countdown(self):
        """Decrements the current state of the timer by 1"""
        self.__current_time -= 1

    def getx(self):
        """Getter for the x-value of the spawner
            Return:
                The x-value of the spawner"""
        return self.__x

    def gety(self):
        """Getter for the y-value of the spawner
            Return:
                The y-value of the spawner"""
        return self.__y

    def get_height(self):
        """Getter for the height of the spawner
            Return:
                The height of the spawner"""
        return self.__height

    def get_width(self):
        """Getter for the width of the spawner
            Return:
                The width of the spawner"""
        return self.__width

    def add(self, o):
        """Adds an occupant to its list of occupants to keep track of
            Args:
                o: the occupant to add to its list of occupants"""
        self.__occupants.append(o)

    def remove(self, occupant):
        """Removes an occupant from its list of occupants to keep track of
            Args:
                occupant: the occupant to remove from the list of occupants"""
        if occupant in self.__occupants:
            self.__occupants.remove(occupant)

    def occupants(self):
        """Getter for the list of occupants the spawner is tracking
            Return:
                the list of occupants the spawner is tracking"""
        return self.__occupants

    def set_spawnx(self, x):
        """Sets the x-location of the next spawn
            Args:
                x: the next x-location for the spawn"""
        self.__spawn_x = x

    def spawnx(self):
        """Getter for x-location of the next spawn
            Return:
                the x-value of the next spawn"""
        return self.__spawn_x

    def spawny(self):
        """Getter for y-location of the next spawn
            Return:
                the y-value of the next spawn"""
        return self.__spawn_y

    def set_spawny(self, y):
        """Sets y-location of the next spawn
            Args:
                the y-value of the next spawn"""
        self.__spawn_y = y

    def set_spawning(self, tf):
        """Sets the spawning trigger to a specified value
            Args:
                tf: whether or not the spawner will now be spawning"""
        self.spawning = tf

    def spawn(self):
        """Sets spawning trigger and creates the spawned occupant
            Return:
                an Occupant that is to be spawn"""
        self.__spawn_x = random.random() * self.__width + self.__x
        self.__spawn_y = random.random() * self.__height + self.__y
        self.spawning = True
        return Occupant('#696969', 5, 1)

    def get_spawn_x(self):
        """Getter for x-location of the next spawn
            Return:
                the x-value of the next spawn"""
        return self.__spawn_x

    def get_spawn_y(self):
        """Getter for y-location of the next spawn
            Return:
                the y-value of the next spawn"""
        return self.__spawn_y

    def get_special_id(self):
        """Getter for the special id, used to keep track of occupants in the world
            Return:
                the special id for this spawner"""
        return self.__special_id


class PlantSpawner(Spawner):
    """A spawner that only spawns plants"""

    def spawn(self):
        """Creates a plant to spawn, and adds it to its tracked occupants
            Return:
                a plant to be spawned in the world"""
        self.set_spawning(False)
        p = Plant(self.get_spawn_x(), self.get_spawn_y(), (random.random()*10000))
        self.add(p)
        return p

    def update(self):
        """The primary logic loop that is run during every cycle of the program

            Only selectively spawns based on shade in the area"""
        self.countdown()
        if self.get_current_time() <= 0:
            spawnx = ((random.random() * (self.get_width())) + self.getx())
            spawny = ((random.random() * (self.get_height())) + self.gety())
            shade = self._calculate_shade(spawnx, spawny)
            if random.random() > shade:
                self.set_spawnx(spawnx)
                self.set_spawny(spawny)
                self.set_spawning(True)
            self.set_current_time(self.timer())

    def _calculate_shade(self, x, y):
        """Calculates the shade for a new potential plant
            Args:
                x: the new x-value of the potential plant
                y: the new y-value of the potential plant"""
        shade = 0
        for plant in self.occupants():
            size = 2 * plant.get_size()
            distance = int(math.sqrt((((x-plant.getx())*(x-plant.getx()))+((y-plant.gety())*(y-plant.gety())))))
            if distance != 0:
                shade += (size/distance)
            else:
                shade = 2
        return shade


class SpecialSpawner(Spawner):
    """A spawner that spawns objects using a provided template"""

    def __init__(self, timer, height, width, x, y, occupant):
        """Initialization logic
            Args:
                timer: the time in update cycles between each attempted spawn
                height: the height of the spawner
                width: the width of the spawner
                x: the x-value of the spawner in its world
                y: the y-value of the spawner in its world
                occupant: the template occupant to base spawns off of"""
        Spawner.__init__(self, timer, height, width, x, y)
        self.__model = occupant

    def spawn(self):
        """Spawns an instance of the provided model
            Return:
                an instance of the template occupant"""
        self.set_spawnx((random.random() * (self.get_width())) + self.getx())
        self.set_spawny((random.random() * (self.get_height())) + self.gety())
        self.set_spawning(False)
        return self.__model
