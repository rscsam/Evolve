"""The program that will actually be run"""

from tkinter import *
import tkinter as tk
from dotworld import World
import tools as tools


class App:
    running = True
    speed = 10
    world = World()

    dot_parrallels = {None: None}
    root = None
    canvas = None
    xEntry = None
    yEntry = None
    csXSpeedEntry = None
    csYSpeedEntry = None
    csSizeEntry = None
    csColorEntry = None
    current_selection = None

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
            ref = self._create_circle(c.getx(), c.gety(), c.get_radius(), fill="#424242", width=0)
            c.set_reference(ref)
            self.dot_parrallels[ref] = c
            self.canvas.tag_bind(ref, "<Button-2>", lambda event, arg=ref: self.highlight_dot(event, arg))

    def draw_dot(self, c):
        """"draw dot, which had not been initialized"""
        ref = self._create_circle(c.getx(), c.gety(), c.get_radius(), fill="#424242", width=0)
        c.set_reference(ref)
        self.dot_parrallels[ref] = c
        self.canvas.tag_bind(ref, "<Button-2>", lambda event, arg=ref: self.highlight_dot(event, arg))

    def remove_dot(self, dot):
        """""destroys dot at every layer of abstraction"""
        if dot is self.current_selection:
            self.set_current_selection(None)
        del self.dot_parrallels[dot.get_reference()]
        self.canvas.delete(dot.get_reference())
        self.world.occupants.remove(dot)

    def canvas_on_click(self, event):
        """adds a new dot at the specified location"""
        self.canvas.focus_set()
        self.draw_dot(self.world.add_squawker(event.x, event.y, "#424242", 3, 4))

    def highlight_dot(self, event, ref):
        if not self.dot_parrallels[ref].highlight_triggered():
            dot = self.dot_parrallels[ref]
            if self.current_selection is not None:
                self.current_selection.highlight_trigger()
                color = self.current_selection.get_color()
                self.canvas.itemconfigure(self.current_selection.get_reference(), fill=color)
            self.set_current_selection(dot)
            dot.highlight_trigger()
            self.canvas.itemconfigure(ref, fill=tools.mix_colors(dot.get_color(), dot.HIGHLIGHT_OFFSET))
        else:
            self.set_current_selection(None)
            self.dot_parrallels[ref].highlight_trigger()
            color = self.dot_parrallels[ref].get_color()
            self.canvas.itemconfigure(ref, fill=color)

    def update_color(self, dot):
        self.canvas.itemconfigure(dot.get_reference(), fill=dot.get_color())

    def set_current_selection(self, dot):
        self.current_selection = dot
        self.csXSpeedEntry.delete(0, END)
        self.csYSpeedEntry.delete(0, END)
        self.csSizeEntry.delete(0, END)
        self.csColorEntry.delete(0, END)
        if dot is None:
            self.csXSpeedEntry.insert(0, "NA")
            self.csYSpeedEntry.insert(0, "NA")
            self.csSizeEntry.insert(0, "NA")
            self.csColorEntry.insert(0, "NA")
        else:
            self.csXSpeedEntry.insert(0, str(dot.get_x_velocity()))
            self.csYSpeedEntry.insert(0, str(dot.get_y_velocity()))
            self.csSizeEntry.insert(0, str(dot.get_radius()))
            self.csColorEntry.insert(0, dot.get_color())

    def apply_cs_changes(self):
        self.current_selection.set_x_velocity(float(self.csXSpeedEntry.get()))
        self.current_selection.set_y_velocity(float(self.csYSpeedEntry.get()))
        self.current_selection.set_radius(float(self.csSizeEntry.get()))
        self.current_selection.set_color(self.csColorEntry.get())
        self.canvas.update()

    def update(self):
        if self.running:
            for c in self.world.occupants:
                c.update()
                if c.ucolor_triggered():
                    self.update_color(c)
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
        self.draw_dot(self.world.add(int(self.xEntry.get()), int(self.yEntry.get()), "#545454", 3, 4))

    def pause_callback(self):
        """pauses the simulation"""
        self.running = not self.running

    def speedup_callback(self):
        if self.speed >= 1:
            self.speed -= 1

    def slowdown_callback(self):
        self.speed += 1

    def __init__(self, speed):
        self.root = Tk()
        self.root.title = "Evolvarium"
        self.root.resizable(False, False)

        self.canvas = Canvas(self.root, width=1000, height=600, borderwidth=0, highlightthickness=0, bg="black")
        self.canvas.pack()

        action_bar = Frame(self.root, width=1000, height=58, borderwidth=0)
        Button(action_bar, text="Add occupant", command=self.add_callback).pack(fill=NONE, side=LEFT)
        Label(action_bar, text="X").pack(side=LEFT)
        self.xEntry = Entry(action_bar, width=5)
        self.xEntry.pack(side=LEFT)
        Label(action_bar, text="Y").pack(side=LEFT)
        self.yEntry = Entry(action_bar, width=5)
        self.yEntry.pack(side=LEFT)
        Button(action_bar, text="Pause", command=self.pause_callback).pack(fill=NONE, side=LEFT)
        Button(action_bar, text="Speed Up", command=self.speedup_callback).pack(fill=NONE, side=LEFT)
        Button(action_bar, text="Slow Down", command=self.slowdown_callback).pack(fill=NONE, side=LEFT)
        Label(action_bar, text="xSpeed: ").pack(side=LEFT)
        self.csXSpeedEntry = Entry(action_bar, width=5)
        self.csXSpeedEntry.pack(side=LEFT)
        Label(action_bar, text="ySpeed: ").pack(side=LEFT)
        self.csYSpeedEntry = Entry(action_bar, width=5)
        self.csYSpeedEntry.pack(side=LEFT)
        Label(action_bar, text="Size: ").pack(side=LEFT)
        self.csSizeEntry = Entry(action_bar, width=5)
        self.csSizeEntry.pack(side=LEFT)
        Label(action_bar, text="Color: ").pack(side=LEFT)
        self.csColorEntry = Entry(action_bar, width=7)
        self.csColorEntry.pack(side=LEFT)
        Button(action_bar, text="Apply", command=self.apply_cs_changes).pack(fill=NONE, side=LEFT)

        action_bar.pack(side=LEFT)
        self.set_current_selection(None)
        self.dot_parrallels.clear()
        self.init_dots()
        self.draw_dots()
        self.canvas.bind("<Button-1>", self.canvas_on_click)
        self.canvas.pack()
        self.speed = speed
        self.root.after(speed, self.update)
        self.root.mainloop()

App(5)
