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
world.add(100, 120, 5)
world.add(100, 150, 8)
world.add(100, 180, 10)
world.add(100, 210, 3)

occupants = []
for c in world.occupants:
    occupants.append(canvas.create_circle(c.getx(), c.gety(), c.getradius(), fill="blue", width=0))
for circle in occupants:
    for i in range(100):
        canvas.move(circle, 5, 0)
        canvas.update()
        time.sleep(0.1)
root.mainloop()