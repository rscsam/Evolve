from tkinter import *
import time
from world import Dot

root = Tk()
root.title = "Evolution Simulation"

canvas = Canvas(root, width=1000, height=600, borderwidth=0, highlightthickness=0, bg="black")
canvas.grid()

#Define a shortcut for creating circles
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

creature = Dot(100, 120, 5)
circle1 = canvas.create_circle(100, 120, 5, fill="blue", width=0)
circle2 = canvas.create_circle(100, 150, 5, fill="red", width=0)

for i in range(100):
    canvas.move(circle1, 10, 0)
    canvas.update()
    time.sleep(0.1)
root.mainloop()