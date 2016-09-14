'''
The program that will actually be run
'''

from tkinter import *
from dotworld import World

root = Tk()
root.title = "Evolvarium"

canvas = Canvas(root, width=1000, height=600, borderwidth=0, highlightthickness=0, bg="black")
canvas.grid()


#Define a shortcut for creating circles
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

Canvas.create_circle = _create_circle


world = World()
dots = []


def init_dots():
    world.add(100, 120, 5, 1)
    world.add(100, 150, 8, 1)
    world.add(100, 180, 10, 1)
    world.add(100, 210, 3, 1)


def draw_dots():
    for c in world.occupants:
        c.set_reference(canvas.create_circle(c.getx(), c.gety(), c.get_radius(), fill="blue", width=0))


def draw_dot(c):
    c.set_reference(canvas.create_circle(c.getx(), c.gety(), c.get_radius(), fill="blue", width=0))


def remove_dot(dot):
    dots.remove(dot)


def update():
    for c in world.occupants:
        c.update()
        canvas.coords(c.get_reference(), c.getx(), c.gety(), c.getx2(), c.gety2())
    canvas.update()
    root.after(10, update)

init_dots()
draw_dots()
running = True
root.after(10, update)

root.mainloop()