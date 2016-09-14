"""The program that will actually be run"""

from tkinter import *
from dotworld import World

class App:
    running = True
    world = World()

    root = Tk()
    root.title = "Evolvarium"

    canvas = Canvas(root, width=1000, height=600, borderwidth=0, highlightthickness=0, bg="black")
    canvas.grid()

    def _create_circle(self, x, y, r, **kwargs):
        """Define a shortcut for creating circles"""
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    Canvas.create_circle = _create_circle


    def init_dots(self):
        self.world.add(100, 120, 5, 1)
        self.world.add(100, 150, 8, 1)
        self.world.add(100, 180, 10, 1)
        self.world.add(100, 210, 3, 1)
        self.world.add(200, 120, 5, 1)
        self.world.add(200, 150, 8, 1)
        self.world.add(200, 180, 10, 1)
        self.world.add(200, 210, 3, 1)
        self.world.add(300, 120, 5, 1)
        self.world.add(300, 150, 8, 1)
        self.world.add(300, 180, 10, 1)
        self.world.add(300, 210, 3, 1)
        self.world.add(400, 120, 5, 1)
        self.world.add(400, 150, 8, 1)
        self.world.add(400, 180, 10, 1)
        self.world.add(400, 210, 3, 1)

    def draw_dots(self):
        for c in self.world.occupants:
            c.set_reference(self.canvas.create_circle(c.getx(), c.gety(), c.get_radius(), fill="yellow", width=0))

    def draw_dot(self, c):
        c.set_reference(self.canvas.create_circle(c.getx(), c.gety(), c.get_radius(), fill="blue", width=0))

    #Does not yet work
    def detect_collision(self, dot):
        for c in self.world.occupants:
            distance = ((dot.get_center()[0] - c.get_center()[0])**2) + ((dot.get_center()[1] - c.get_center()[1])**2)**0.5
            if distance <= (dot.get_radius() + c.get_radius()):
                return True
        return False

    #does not work as intended
    def remove_dot(self, dot):
        self.world.occupants.remove(dot)

    def canvas_on_click(self, event):
        self.canvas.focus_set()
        #self.running = not self.running
        self.draw_dot(self.world.add(event.x, event.y, 3, 2))
        print("Click:",event.x,",",event.y)

    def update(self):
        if self.running:
            for c in self.world.occupants:
                c.update()
                self.canvas.coords(c.get_reference(), c.getx(), c.gety(), c.getx2(), c.gety2())
            self.canvas.update()
        self.root.after(10, self.update)

    def __init__(self):
        self.init_dots()
        self.draw_dots()
        self.canvas.bind("<Button-1>", self.canvas_on_click)
        self.canvas.pack()
        self.root.after(10, self.update)
        self.root.mainloop()


App()