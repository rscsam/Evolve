"""The program that will actually be run"""

from tkinter import *

import creature
import reference
import tools as tools
from dotworld import World


class App:
    """The primary program that will be run"""

    CANVAS_HEIGHT = 600
    CANVAS_WIDTH = 1200


    def __init__(self, speed):
        """initialization logic"""
        self.world = World()
        self.world.wheight = self.CANVAS_HEIGHT
        self.world.wwidth = self.CANVAS_WIDTH
        self.running = False
        self.speed = 10
        self.dot_parrallels = {None: None}
        self.spawn_map = {None: None}
        self.root = None
        self.canvas = None
        self.xEntry = None
        self.yEntry = None
        self.csSpeedEntry = None
        self.csSizeEntry = None
        self.csColorEntry = None
        self.current_selection = None
        self.__init_gui()
        self.set_current_selection(None)
        self.dot_parrallels.clear()
        self.spawn_map.clear()
        self._init_spawners()
        self._init_dots()
        self._draw_dots()
        self.canvas.bind("<Button-1>", self._canvas_on_click)
        self.canvas.pack(fill=BOTH, expand=TRUE)
        self.speed = speed
        self.root.after(speed, self.update)
        self.root.mainloop()

    def __init_gui(self):
        """initializes gui specific logic"""
        self.root = Tk()
        self.full_screen = False
        self.root.bind("<Tab>", self._toggle_fullscreen)
        self.root.bind("<Escape>", self._end_fullscreen)
        self.root.bind("<space>", self._pause)
        self.root.title = "Evolvarium"
        self.root.resizable(True, True)
        self.canvas = Canvas(self.root, width=self.CANVAS_WIDTH,
                             height=self.CANVAS_HEIGHT, borderwidth=0, highlightthickness=0, bg="black")
        self.canvas.pack()

        action_bar = Frame(self.root, width=self.CANVAS_WIDTH, height=58, borderwidth=0)
        Button(action_bar, text="Add occupant", command=self._add_callback).pack(fill=NONE, side=LEFT)
        Label(action_bar, text="X").pack(side=LEFT)
        self.xEntry = Entry(action_bar, width=5)
        self.xEntry.pack(side=LEFT)
        Label(action_bar, text="Y").pack(side=LEFT)
        self.yEntry = Entry(action_bar, width=5)
        self.yEntry.pack(side=LEFT)
        Button(action_bar, text="Pause", command=self._pause_callback).pack(fill=NONE, side=LEFT)
        Button(action_bar, text="Speed Up", command=self._speedup_callback).pack(fill=NONE, side=LEFT)
        Button(action_bar, text="Slow Down", command=self._slowdown_callback).pack(fill=NONE, side=LEFT)
        Label(action_bar, text="Speed: ").pack(side=LEFT)
        self.csSpeedEntry = Entry(action_bar, width=5)
        self.csSpeedEntry.pack(side=LEFT)
        Label(action_bar, text="Size: ").pack(side=LEFT)
        self.csSizeEntry = Entry(action_bar, width=5)
        self.csSizeEntry.pack(side=LEFT)
        Label(action_bar, text="Color: ").pack(side=LEFT)
        self.csColorEntry = Entry(action_bar, width=7)
        self.csColorEntry.pack(side=LEFT)
        Button(action_bar, text="Kill", command=self._kill_callback).pack(fill=NONE, side=LEFT)
        action_bar.pack(side=LEFT)
        Button(action_bar, text="Apply", command=self._apply_cs_changes).pack(fill=NONE, side=LEFT)
        action_bar.pack(side=LEFT)

    def _toggle_fullscreen(self, event=None):
        self.full_screen = not self.full_screen  # Just toggling the boolean
        self.root.attributes("-fullscreen", self.full_screen)
        return "break"

    def _end_fullscreen(self, event=None):
        self.full_screen = False
        self.root.attributes("-fullscreen", False)
        return "break"

    def _add_callback(self):
        """The method called when 'ADD' is clicked -- Adds a gray Occupant at the point of the event"""
        self.draw_dot(self.world.add_convenient(int(self.xEntry.get()), self.yEntry.get(),
                                                ["B", 250, 10, 15, 2, 1, tools.random_color(),
                                                 .99, .99, .99, .99, .99, .5, 2], reference.d_herbivore_scripts(),
                                                10000))

    def _apply_cs_changes(self):
        """Applies to the current selection the attributes typed into the text boxes"""
        self.current_selection.set_speed(int(self.csSpeedEntry.get()))
        self.current_selection.set_radius(int(self.csSizeEntry.get()))
        self.world.test_largest_radius(int(self.csSizeEntry.get()))
        self.current_selection.set_color(self.csColorEntry.get())
        self.canvas.update()

    def _canvas_on_click(self, event):
        """The method called when the canvas is clicked -- Adds a gray Squawker at the point of the event"""
        self.canvas.focus_set()
        self.draw_dot(self.world.add_convenient(event.x, event.y,
                                                ["B", 250, 10, 15, 2, 1, tools.random_color(),
                                                 .99, .99, .99, .99, .99, .5, 2], reference.d_versatile_scripts(),
                                                1000))

    def _create_circle(self, x, y, r, **kwargs):
        """Define a shortcut for creating circles"""
        return self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def _draw_dots(self):
        """"draw dots initialized previously"""
        for c in self.world.occupants:
            ref = self._create_circle(c.get_centerx(), c.get_centery(), c.get_radius(), fill=c.get_color(), width=0)
            c.set_reference(ref)
            self.dot_parrallels[ref] = c
            self.canvas.tag_bind(ref, "<Button-2>", lambda event, arg=ref: self.select_dot(event, arg))
            self.canvas.tag_bind(ref, "<Button-3>", lambda event, arg=ref: self.select_dot(event, arg))

    def _init_dots(self):
        """Initializes dots that will be present at the time the program begins"""
        # g = ["Species", vis, str, size, spe, bur, col, vmf, strmf, szmf, spmf, bmf, colmf, toughness]
        self.world.add_herbivore(300, 300, ["H", 75, 1, 3, 3, 4, tools.random_color(),
                                             .99, .99, .99, .99, .99, .9, 20], reference.d_herbivore_scripts(),
                                 10000, None).get_occupant().set_base_energy(10000)
        # self.world.add_omnivore(400, 100, ["C", 250, 25, 15, 1, 2, tools.random_color(),
        #                                    .99, .99, .99, .99, .99, .9, 2], reference.def_omnivore_scripts,
        #                         10000, None)
        # self.world.add_omnivore(400, 500, ["D", 250, 25, 15, 1, 2, tools.random_color(),
        #                                    .99, .99, .99, .99, .99, .9, 2], reference.def_omnivore_scripts,
        #                        10000, None)
        # self.world.add_versatile(200, 500, ["D", 250, 25, 15, 1, 2, tools.random_color(),
        #                                     .99, .99, .99, .99, .99, .9, 2], reference.d_versatile_scripts(),
        #                           20000, None).get_occupant().set_base_energy(20000)
        # self.world.add_versatile(400, 500, ["D", 250, 25, 15, 1, 2, tools.random_color(),
        #                                     .99, .99, .99, .99, .99, .9, 2], reference.d_versatile_scripts(),
        #                          20000, None).get_occupant().set_base_energy(20000)

    def _init_spawners(self):
        """Initializes spawners that will be present at the time the program begins"""
        ps1 = self.world.add_plant_spawner(4, self.CANVAS_HEIGHT, self.CANVAS_WIDTH/4, 0, 0)
        self.spawn_map[ps1.get_special_id()] = ps1
        ps2 = self.world.add_plant_spawner(4, self.CANVAS_HEIGHT, self.CANVAS_WIDTH/4, self.CANVAS_WIDTH*3/4, 0)
        self.spawn_map[ps2.get_special_id()] = ps2

    def _pause(self, event=None):
        self.running = not self.running

    def _pause_callback(self):
        """The method called when 'PAUSE' is clicked -- pauses the program"""
        self.running = not self.running

    def _kill_callback(self):
        """pauses the simulation"""
        self.current_selection.kill_trigger()

    def _slowdown_callback(self):
        """The method called when 'SLOW DOWN' is clicked -- Slows down the main loop"""
        self.speed += 1

    def _speedup_callback(self):
        """The method called when 'ADD' is clicked -- Speeds up the main loop"""
        if self.speed > 1:
            self.speed -= 1

    def draw_dot(self, c):
        """"Draw dot, which had not been initialized"""
        ref = self._create_circle(c.get_centerx(), c.get_centery(), c.get_radius(), fill=c.get_color(), width=0)
        c.set_reference(ref)
        self.dot_parrallels[ref] = c
        self.canvas.tag_bind(ref, "<Button-2>", lambda event, arg=ref: self.select_dot(event, arg))
        self.canvas.tag_bind(ref, "<Button-3>", lambda event, arg=ref: self.select_dot(event, arg))

    def remove_dot(self, dot):
        """""Destroys dot at every layer of abstraction"""
        if dot is self.current_selection:
            self.set_current_selection(None)
        del self.dot_parrallels[dot.get_reference()]
        self.canvas.delete(dot.get_reference())
        self.world.occupants.remove(dot)
        if dot.special != -1:
            self.spawn_map[dot.special].remove(dot.get_occupant())

    def select_dot(self, event, ref):
        """Highlights a dot and makes it the Current Selection (or deselects)"""
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

    def set_current_selection(self, dot):
        """Sets the current selection to @param dot and updates the text boxes"""
        self.current_selection = dot
        self.csSpeedEntry.delete(0, END)
        self.csSizeEntry.delete(0, END)
        self.csColorEntry.delete(0, END)
        if dot is None:
            self.csSpeedEntry.insert(0, "NA")
            self.csSizeEntry.insert(0, "NA")
            self.csColorEntry.insert(0, "NA")
        else:
            self.csSpeedEntry.insert(0, str(dot.get_speed()))
            self.csSizeEntry.insert(0, str(dot.get_radius()))
            self.csColorEntry.insert(0, dot.get_color())

    def update(self):
        """The main logic loop of the program"""
        if self.running:
            self.world.wheight = self.canvas.winfo_height()
            self.world.wwidth = self.canvas.winfo_width()
            for c in self.world.occupants:
                if c.needs_vision():
                    self.update_visions(c)
                c.update()
                self.update_collisions(c)
            self.world.handle_wall_collision()
            for c in self.world.occupants:
                if not c.kill_triggered():
                    self.canvas.coords(c.get_reference(), c.getx(), c.gety(), c.getx2(), c.gety2())
                self.handle_triggers(c)
            for s in self.world.spawners:
                s.update()
                if s.spawning:
                    d = self.world.add(s.spawn(), s.get_spawn_x(), s.get_spawn_y())
                    d.special = s.get_special_id()
                    self.draw_dot(d)
            self.canvas.update()
        self.root.after(self.speed, self.update)

    def update_color(self, dot):
        """Changes the visible color of the dot to its actual color"""
        self.canvas.itemconfigure(dot.get_reference(), fill=dot.get_color())

    def handle_triggers(self, c):
        """Handle the various Dot triggers"""
        if c.collide_triggered():
            if isinstance(c.get_occupant(), creature.Plant):
                c.kill_trigger()
        if c.ucolor_triggered():
            self.update_color(c)
        if c.reproducing_triggered():
            self.draw_dot(self.world.add(c.reproduce(), c.get_centerx(), c.get_centery()))
        if c.kill_triggered():
            self.remove_dot(c)

    def update_collisions(self, c):
        """Handles collision between dots"""
        overlaps = self.canvas.find_overlapping(c.getx(), c.gety(), c.getx2(), c.gety2())
        doverlaps = []
        for o in overlaps:
            if o != c.get_reference():
                doverlaps.append(self.dot_parrallels[o])
        self.world.handle_collisions(c, doverlaps)

    def update_visions(self, c):
        """Updates each dots vision of nearby dots"""
        cx = c.get_centerx()
        cy = c.get_centery()
        r = c.get_radius()
        vr = c.get_vision_radius()
        overlaps = self.canvas.find_overlapping(cx-(vr+r), cy+(vr+r), cx+(vr+r), cy-(vr+r))
        doverlaps = []
        for o in overlaps:
            if o != c.get_reference():
                doverlaps.append(self.dot_parrallels[o])
        self.world.update_visions(c, doverlaps)

App(1)
