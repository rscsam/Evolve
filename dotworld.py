"""The module that handles the front-end representations of the backend"""

from creature import *


class World:
    occupants = []

    def add_occupant(self, occupant, x, y):
        c = Dot(occupant, x, y)
        self.occupants.append(c)
        return c

    def add(self, x, y, color, size, speed):
        c = Dot(Occupant(color, size, speed), x, y)
        self.occupants.append(c)
        return c

    def add_squawker(self, x, y, color, size, speed):
        c = Dot(Squawker(color, size, speed), x, y)
        self.occupants.append(c)
        return c

    def add_dunkboy(self, x, y, color, size, speed):
        c = Dot(Dunkboy(color, size, speed), x, y)
        self.occupants.append(c)
        return c

    def add_reproducing(self, x, y, color, size, speed):
        c = Dot(ReproducingOccupant(color, size, speed), x, y)
        self.occupants.append(c)
        return c

    def handle_wall_collision(self):
        for dot in self.occupants:
            if dot.getx() < 0:
                dot.setx(0)
                dot.get_occupant().hit_side()
            elif dot.getx2() > 1000:
                dot.setx2(1000)
                dot.get_occupant().hit_side()
            if dot.gety() < 0:
                dot.sety(0)
                dot.get_occupant().hit_lid()
            elif dot.gety2() > 600:
                dot.sety2(600)
                dot.get_occupant().hit_lid()

    def detect_collision(self, dot):
        for c in self.occupants:
            if c != dot and not isinstance(c.get_occupant(), ReproducingOccupant):
                distance = int((((dot.get_centerx() - c.get_centerx())**2)
                                + ((dot.get_centery() - c.get_centery())**2)**0.5))-2
                if distance <= (dot.get_radius() + c.get_radius()):
                    c.collide_trigger()
                    dot.collide_trigger()


class Dot:
    __occupant = 0
    __x = 0
    __y = 0
    __x2 = 0
    __y2 = 0
    __radius = 0
    __reference = None
    __collide_trigger = False
    __highlight_trigger = False
    __color_trigger = False
    __reproducing_trigger = False
    HIGHLIGHT_OFFSET = "#22AAFF"

    def __init__(self, occupant, x, y):
        self.__occupant = occupant
        self.setx(x)
        self.sety(y)
        self.__color = occupant.get_color()
        self.__radius = occupant.get_size()

    def setx(self, x):
        self.__x = x
        self.__x2 = x + (2 * self.__radius)

    def getx(self):
        return self.__x

    def sety(self, y):
        self.__y = y
        self.__y2 = y + (2 * self.__radius)

    def gety(self):
        return self.__y

    def setx2(self, x2):
        self.__x2 = x2
        self.__x = x2 - (2 * self.__radius)

    def getx2(self):
        return self.__x2

    def sety2(self, y2):
        self.__y2 = y2
        self.__y = y2 - (2 * self.__radius)

    def gety2(self):
        return self.__y2

    def set_radius(self, radius):
        self.__radius = radius
        self.__occupant.set_size(radius)

    def get_radius(self):
        return self.__radius

    def get_occupant(self):
        return self.__occupant

    def set_color(self, color):
        self.__occupant.set_color(color)
        self.color_trigger()

    def get_color(self):
        return self.__occupant.get_color()

    def get_center(self):
        x = self.__x + self.__radius
        y = self.__y + self.__radius
        return x, y

    def get_centerx(self):
        return self.get_center()[0]

    def get_centery(self):
        return self.get_center()[1]

    def set_x_velocity(self, v):
        self.__occupant.set_x_velocity(v)

    def get_x_velocity(self):
        return self.__occupant.get_x_velocity()

    def set_y_velocity(self, v):
        self.__occupant.set_y_velocity(v)

    def get_y_velocity(self):
        return self.__occupant.get_y_velocity()

    def set_speed(self, v):
        self.__occupant.set_speed(v)

    def get_speed(self):
        return self.__occupant.get_speed()

    def set_reference(self, reference):
        self.__reference = reference
        self.__x2 = self.__x + (2 * self.__radius)
        self.__y2 = self.__y + (2 * self.__radius)

    def get_reference(self):
        return self.__reference

    def move(self):
        self.setx(self.__x + self.__occupant.get_x_velocity())
        self.sety(self.__y + self.__occupant.get_y_velocity())

    def reproduce(self):
        if isinstance(self.__occupant, ReproducingOccupant):
            self.__reproducing_trigger = False
            return self.__occupant.reproduce()

    def update(self):
        self.__occupant.update()
        self.move()
        if isinstance(self.__occupant, ReproducingOccupant):
            if self.__occupant.reproducing():
                self.reproducing_trigger()

    def collide_trigger(self):
        self.__collide_trigger = True

    def collide_triggered(self):
        return self.__collide_trigger

    def highlight_trigger(self):
        self.__highlight_trigger = not self.__highlight_trigger

    def highlight_triggered(self):
        return self.__highlight_trigger

    def color_trigger(self):
        self.__color_trigger = not self.__highlight_trigger

    def color_triggered(self):
        return self.__color_trigger

    def ucolor_triggered(self):
        tf = self.__color_trigger
        self.__color_trigger = False
        return tf

    def reproducing_trigger(self):
        self.__reproducing_trigger = not self.__reproducing_trigger

    def reproducing_triggered(self):
        return self.__reproducing_trigger
