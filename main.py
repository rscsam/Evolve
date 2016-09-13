'''
The program that will actually be run
'''

from tkinter import *
import time
from dotworld import World
from dotworld import Dot

root = Tk()
root.title = "Evolvarium"

canvas = Canvas(root, width=1000, height=600, borderwidth=0, highlightthickness=0, bg="black")
canvas.grid()


#Define a shortcut for creating circles
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

Canvas.create_circle = _create_circle


world = World()
world.add(100, 120, 5, 1)
world.add(100, 150, 8, 1)
world.add(100, 180, 10, 1)
world.add(100, 210, 3, 1)

dots = []
for c in world.occupants:
    dots.append(canvas.create_circle(c.getx(), c.gety(), c.getradius(), fill="blue", width=0))

while True:
    for c in world.occupants:
        c.move()
    for circle in dots:
        canvas.move(circle, 5, 0)
        canvas.update()
    time.sleep(0.1)
root.mainloop()