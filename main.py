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
        return self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def init_dots(self):
        self.world.add(100, 120, "#424242", 5, 1)
        self.world.add(100, 150, "#424242", 8, 1)
        self.world.add(100, 180, "#424242", 10, 1)
        self.world.add(100, 210, "#424242", 3, 1)
        self.world.add_squawker(200, 120, "#424242", 5, 1)
        self.world.add_squawker(200, 150, "#424242", 8, 1)
        self.world.add_squawker(200, 180, "#424242", 10, 1)
        self.world.add_squawker(200, 210, "#424242", 3, 1)
        self.world.add(300, 120, "#424242", 5, 1)
        self.world.add(300, 150, "#424242", 8, 1)
        self.world.add(300, 180, "#424242", 10, 1)
        self.world.add(300, 210, "#424242", 3, 1)
        self.world.add_dunkboy(400, 120, "#424242", 5, 1)
        self.world.add_dunkboy(400, 150, "#424242", 8, 1)
        self.world.add_dunkboy(400, 180, "#424242", 10, 1)
        self.world.add_dunkboy(400, 210, "#424242", 3, 1)
        self.world.add(100, 320, "#424242", 5, 1)
        self.world.add(100, 350, "#424242", 8, 1)
        self.world.add(100, 380, "#424242", 10, 1)
        self.world.add(100, 410, "#424242", 3, 1)
        self.world.add_squawker(200, 320, "#424242", 5, 1)
        self.world.add_squawker(200, 350, "#424242", 8, 1)
        self.world.add_squawker(200, 380, "#424242", 10, 1)
        self.world.add_squawker(200, 410, "#424242", 3, 1)
        self.world.add(300, 320, "#424242", 5, 1)
        self.world.add(300, 350, "#424242", 8, 1)
        self.world.add(300, 380, "#424242", 10, 1)
        self.world.add(300, 410, "#424242", 3, 1)
        self.world.add_dunkboy(400, 320, "#424242", 5, 1)
        self.world.add_dunkboy(400, 350, "#424242", 8, 1)
        self.world.add_dunkboy(400, 380, "#424242", 10, 1)
        self.world.add_dunkboy(400, 410, "#424242", 3, 1)

    def draw_dots(self):
        """"draw dots initialized previously"""
        for c in self.world.occupants:
            c.set_reference(self._create_circle(c.getx(), c.gety(), c.get_radius(), fill="#424242", width=0))

    def draw_dot(self, c):
        """"draw dot, which had not been initialized"""
        c.set_reference(self._create_circle(c.getx(), c.gety(), c.get_radius(), fill=c.get_color(), width=0))

    def remove_dot(self, dot):
        """""destroys dot at every layer of abstraction"""
        self.canvas.delete(dot.get_reference())
        self.world.occupants.remove(dot)

    def canvas_on_click(self, event):
        """adds a new dot at the specified location"""
        self.canvas.focus_set()
        self.draw_dot(self.world.add_squawker(event.x, event.y, "blue", 3, 4))

    def update(self):
        if self.running:
            for c in self.world.occupants:
                c.update()
                self.world.detect_collision(c)
                if not c.kill_triggered():
                    self.canvas.coords(c.get_reference(), c.getx(), c.gety(), c.getx2(), c.gety2())
            self.world.handle_wall_collision()
            for c in self.world.occupants:
                    if c.kill_triggered():
                        self.remove_dot(c)
            self.canvas.update()
        self.root.after(self.speed, self.update)

    def add_callback(self):
        self.draw_dot(self.world.add(int(self.xEntry.get()), int(self.yEntry.get()), "red", 3, 4))

    def pause_callback(self):
        """pauses the simulation"""
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


App(25)
