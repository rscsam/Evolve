"""The program that will actually be run"""

from tkinter import *
from dotworld import World

root = Tk()
root.title = "Evolvarium"

canvas = Canvas(root, width=1000, height=600, borderwidth=0, highlightthickness=0, bg="black")
canvas.grid()


def _create_circle(self, x, y, r, **kwargs):
    """Define a shortcut for creating circles"""
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

Canvas.create_circle = _create_circle


world = World()
dots = []


def init_dots():
    world.add(100, 120, 5, 1)
    world.add(100, 150, 8, 1)
    world.add(100, 180, 10, 1)
    world.add(100, 210, 3, 1)
    world.add(200, 120, 5, 1)
    world.add(200, 150, 8, 1)
    world.add(200, 180, 10, 1)
    world.add(200, 210, 3, 1)
    world.add(300, 120, 5, 1)
    world.add(300, 150, 8, 1)
    world.add(300, 180, 10, 1)
    world.add(300, 210, 3, 1)
    world.add(400, 120, 5, 1)
    world.add(400, 150, 8, 1)
    world.add(400, 180, 10, 1)
    world.add(400, 210, 3, 1)


def draw_dots():
    for c in world.occupants:
        c.set_reference(canvas.create_circle(c.getx(), c.gety(), c.get_radius(), fill="yellow", width=0))


def draw_dot(c):
    c.set_reference(canvas.create_circle(c.getx(), c.gety(), c.get_radius(), fill="blue", width=0))

#Does not yet work
def detect_collision(dot):
    for c in world.occupants:
        distance = ((dot.get_center()[0] - c.get_center()[0])**2) + ((dot.get_center()[1] - c.get_center()[1])**2)**0.5
        if distance <= (dot.get_radius() + c.get_radius()):
            return True
    return False



def remove_dot(dot):
    world.occupants.remove(dot)


def update():
    count = 0
    for c in world.occupants:
        c.update()
        canvas.coords(c.get_reference(), c.getx(), c.gety(), c.getx2(), c.gety2())
    # for c in world.occupants:
    #     if detect_collision(c):
    #         remove_dot(c)
    canvas.update()
    root.after(10, update)

init_dots()
draw_dots()
running = True
root.after(10, update)

root.mainloop()