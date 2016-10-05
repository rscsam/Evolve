"""The program that will actually be run"""

from tkinter import *
from dotworld import World

class App:
    running = True
    speed = 10
    world = World()

    root = None
    canvas = None
    xEntry = None
    yEntry = None

    def _create_circle(self, x, y, r, **kwargs):
        """Define a shortcut for creating circles"""
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    Canvas.create_circle = _create_circle

    def init_dots(self):
        self.world.add(100, 120, 5, 1)
        self.world.add(100, 150, 8, 1)
        self.world.add(100, 180, 10, 1)
        self.world.add(100, 210, 3, 1)
        self.world.add_squawker(200, 120, 5, 1)
        self.world.add_squawker(200, 150, 8, 1)
        self.world.add_squawker(200, 180, 10, 1)
        self.world.add_squawker(200, 210, 3, 1)
        self.world.add(300, 120, 5, 1)
        self.world.add(300, 150, 8, 1)
        self.world.add(300, 180, 10, 1)
        self.world.add(300, 210, 3, 1)
        self.world.add_dunkboy(400, 120, 5, 1)
        self.world.add_dunkboy(400, 150, 8, 1)
        self.world.add_dunkboy(400, 180, 10, 1)
        self.world.add_dunkboy(400, 210, 3, 1)
        self.world.add(100, 320, 5, 1)
        self.world.add(100, 350, 8, 1)
        self.world.add(100, 380, 10, 1)
        self.world.add(100, 410, 3, 1)
        self.world.add_squawker(200, 320, 5, 1)
        self.world.add_squawker(200, 350, 8, 1)
        self.world.add_squawker(200, 380, 10, 1)
        self.world.add_squawker(200, 410, 3, 1)
        self.world.add(300, 320, 5, 1)
        self.world.add(300, 350, 8, 1)
        self.world.add(300, 380, 10, 1)
        self.world.add(300, 410, 3, 1)
        self.world.add_dunkboy(400, 320, 5, 1)
        self.world.add_dunkboy(400, 350, 8, 1)
        self.world.add_dunkboy(400, 380, 10, 1)
        self.world.add_dunkboy(400, 410, 3, 1)

    def draw_dots(self):
        for c in self.world.occupants:
            c.set_reference(self.canvas.create_circle(c.getx(), c.gety(), c.get_radius(), fill="#424242", width=0))

    def draw_dot(self, c, str):
        fillcolor = str
        c.set_reference(self.canvas.create_circle(c.getx(), c.gety(), c.get_radius(), fill=fillcolor, width=0))

    def remove_dot(self, dot):
        self.canvas.delete(dot.get_reference())
        self.world.occupants.remove(dot)

    def canvas_on_click(self, event):
        self.canvas.focus_set()
        self.draw_dot(self.world.add_squawker(event.x, event.y, 3, 4), "blue")

    def update(self):
        if self.running:
            for c in self.world.occupants:
                c.update()
                self.world.detect_collision(c)
                if not c.triggered():
                    self.canvas.coords(c.get_reference(), c.getx(), c.gety(), c.getx2(), c.gety2())
            self.world.handle_wall_collision()
            for c in self.world.occupants:
                    if c.triggered():
                        self.remove_dot(c)
            self.canvas.update()
        self.root.after(self.speed, self.update)

    def add_callback(self):
        self.draw_dot(self.world.add(int(self.xEntry.get()), int(self.yEntry.get()), 3, 4), "red")

    def pause_callback(self):
        self.running = not self.running

    def __init__(self, speed):
        self.root = Tk()
        self.root.title = "Evolvarium"
        self.root.resizable(False, False)

        self.canvas = Canvas(self.root, width=1000, height=600, borderwidth=0, highlightthickness=0, bg="black")
        self.canvas.pack()

        action_bar = Frame(self.root, width=1000, height=58, borderwidth=0)
        Button(action_bar, text="Add an occupant", command=self.add_callback).pack(fill=NONE, side=LEFT)
        Label(action_bar, text="X").pack(side=LEFT)
        self.xEntry = Entry(action_bar, width=5)
        self.xEntry.pack(side=LEFT)
        Label(action_bar, text="Y").pack(side=LEFT)
        self.yEntry = Entry(action_bar, width=5)
        self.yEntry.pack(side=LEFT)
        Button(action_bar, text="Pause", command=self.pause_callback).pack(fill=NONE, side=LEFT)
        action_bar.pack(side=LEFT)
        self.init_dots()
        self.draw_dots()
        self.canvas.bind("<Button-1>", self.canvas_on_click)
        self.canvas.pack()
        self.speed = speed
        self.root.after(speed, self.update)
        self.root.mainloop()


class App2(App):
    def draw_dot(self, c, color):
        c.set_reference(self.canvas.create_circle(c.getx(), c.gety(), c.get_radius(), fill=color, width=0))

App(3)
