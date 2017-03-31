"""This module defines a series of spawners capable of spawning occupants into their world"""

from creature import *


class Spawner:
    """A superclass that defines a spawner capable of keeping track of its own occupants
        and deciding when to spawn a new one in the world it is created in"""

    """Initialization logic
        Args:
            timer: the time in update cycles between each attempted spawn
            height: the height of the spawner
            width: the width of the spawner
            x: the x-value of the spawner in its world
            y: the y-value of the spawner in its world"""
    def __init__(self, timer, height, width, x, y):
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

    """Initializes a special id used to keep track of occupants by the world"""
    def __init_special_id(self):
        self.__special_id = random.random() * 999999999

    """The primary logic loop that is run during every cycle of the program"""
    def update(self):
        self.__current_time -= 1
        if self.__current_time <= 0:
            self.spawning = True
            self.__current_time = self.__timer

    """Getter for the timer
        Return:
            the spawner's timer"""
    def timer(self):
        return self.__timer

    """Getter for the current state of the timer.  If it is zero, it is time to spawn
        Return:
            the current time of the timer"""
    def get_current_time(self):
        return self.__current_time

    """Getter for the current state of the timer.  If it is zero, it is time to spawn
        Return:
            the current time of the timer"""
    def gct(self):
        return self.get_current_time()

    """Sets the current state of the timer to a specified value
        Args:
            o: the new current time of the timer"""
    def set_current_time(self, o):
        self.__current_time = o

    """Decrements the current state of the timer by 1"""
    def countdown(self):
        self.__current_time -= 1

    """Getter for the x-value of the spawner
        Return:
            The x-value of the spawner"""
    def getx(self):
        return self.__x

    """Getter for the y-value of the spawner
        Return:
            The y-value of the spawner"""
    def gety(self):
        return self.__y

    """Getter for the height of the spawner
        Return:
            The height of the spawner"""
    def get_height(self):
        return self.__height

    """Getter for the width of the spawner
        Return:
            The width of the spawner"""
    def get_width(self):
        return self.__width

    """Adds an occupant to its list of occupants to keep track of
        Args:
            o: the occupant to add to its list of occupants"""
    def add(self, o):
        self.__occupants.append(o)

    """Removes an occupant from its list of occupants to keep track of
        Args:
            o: the occupant to remove from the list of occupants"""
    def remove(self, occupant):
        if occupant in self.__occupants:
            self.__occupants.remove(occupant)

    """Getter for the list of occupants the spawner is tracking
        Return:
            the list of occupants the spawner is tracking"""
    def occupants(self):
        return self.__occupants

    """Sets the x-location of the next spawn
        Args:
            x: the next x-location for the spawn"""
    def set_spawnx(self, x):
        self.__spawn_x = x

    """Getter for x-location of the next spawn
        Return:
            the x-value of the next spawn"""
    def spawnx(self):
        return self.__spawn_x

    """Sets the y-location of the next spawn
        Args:
            y: the next y-location for the spawn"""
    def spawny(self):
        return self.__spawn_y

    """Getter for y-location of the next spawn
        Return:
            the y-value of the next spawn"""
    def set_spawny(self, y):
        self.__spawn_y = y

    """Sets the spawning trigger to a specified value
        Args:
            tf: whether or not the spawner will now be spawning"""
    def set_spawning(self, tf):
        self.spawning = tf

    """Sets spawning trigger and creates the spawned occupant
        Return:
            an Occupant that is to be spawn"""
    def spawn(self):
        self.__spawn_x = random.random() * self.__width + self.__x
        self.__spawn_y = random.random() * self.__height + self.__y
        self.spawning = True
        return Occupant('#696969', 5, 1)

    """Getter for x-location of the next spawn
        Return:
            the x-value of the next spawn"""
    def get_spawn_x(self):
        return self.__spawn_x

    """Getter for y-location of the next spawn
        Return:
            the y-value of the next spawn"""
    def get_spawn_y(self):
        return self.__spawn_y

    """Getter for the special id, used to keep track of occupants in the world
        Return:
            the special id for this spawner"""
    def get_special_id(self):
        return self.__special_id


class PlantSpawner(Spawner):
    """A spawner that only spawns plants"""

    """Creates a plant to spawn, and adds it to its tracked occupants
        Return:
            a plant to be spawned in the world"""
    def spawn(self):
        self.set_spawning(False)
        p = Plant(self.get_spawn_x(), self.get_spawn_y(), (random.random()*7500))
        self.add(p)
        return p

    """The primary logic loop that is run during every cycle of the program
    
        Only selectively spawns based on shade in the area"""
    def update(self):
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

    """Calculates the shade for a new potential plant
        Args:
            x: the new x-value of the potential plant
            y: the new y-value of the potential plant"""
    def _calculate_shade(self, x, y):
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

    """Initialization logic
        Args:
            timer: the time in update cycles between each attempted spawn
            height: the height of the spawner
            width: the width of the spawner
            x: the x-value of the spawner in its world
            y: the y-value of the spawner in its world
            occupant: the template occupant to base spawns off of"""
    def __init__(self, timer, height, width, x, y, occupant):
        Spawner.__init__(self, timer, height, width, x, y)
        self.__model = occupant

    """Spawns an instance of the provided model
        Return:
            an instance of the template occupant"""
    def spawn(self):
        self.set_spawnx((random.random() * (self.get_width())) + self.getx())
        self.set_spawny((random.random() * (self.get_height())) + self.gety())
        self.set_spawning(False)
        return self.__model
