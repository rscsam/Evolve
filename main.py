"""This module defines run configurations that can be useed to run the simulation itself"""

from tkinter import *

import reference
import tools as tools
from dotworld import World
from plant import Plant


class Simulation:
    """A run configuration that sets all parameters and initializations for the simulation"""

    CANVAS_HEIGHT = 600
    CANVAS_WIDTH = 1200

    def __init__(self, speed, world=World()):
        """initialization logic
            Args:
                speed: the inverse of targeted fps.  FPStarget = (60/speed)"""
        self.world = world
        self.world.wheight = self.CANVAS_HEIGHT
        self.world.wwidth = self.CANVAS_WIDTH
        self.running = False
        self.visible_x = 0
        self.visible_y = 0
        self.speed = 10
        self.dot_parrallels = {}
        self.spawn_map = {}
        self.current_selection = None
        self.init_gui()
        self.set_current_selection(None)
        self.dot_parrallels.clear()
        self.init_spawners()
        self.init_dots()
        self._draw_dots()
        self.canvas.pack(fill=BOTH, expand=TRUE)
        self.speed = speed
        self.root.after(speed, self.update)
        self.root.mainloop()

    def init_gui(self):
        """initializes gui specific logic"""
        self.root = Tk()
        self.full_screen = False
        self.root.title = "Evolvarium"
        self.root.resizable(True, True)
        self.canvas = Canvas(self.root, width=self.CANVAS_WIDTH,
                             height=self.CANVAS_HEIGHT, borderwidth=0, highlightthickness=0, bg="black")
        self.canvas.bind("<Button-1>", self.canvas_on_click)
        self.canvas.pack()
        self.init_additional_gui_elements()
        self.configure_hotkeys()

    def init_additional_gui_elements(self):
        """Initialize any additional UI elements you want"""

    def configure_hotkeys(self):
        """Initialize all baseline hotkeys that apply to the whole simulation"""

    def toggle_fullscreen(self, event=None):
        """switches between fullscreen and not fullscreen"""
        self.full_screen = not self.full_screen  # Just toggling the boolean
        self.root.attributes("-fullscreen", self.full_screen)
        return "break"

    def end_fullscreen(self, event=None):
        """forces the screen not to be fullscreen"""
        self.full_screen = False
        self.root.attributes("-fullscreen", False)
        return "break"

    def apply_cs_changes(self):
        """"Applies to the current selection the attributes typed into the text boxes"""

    def canvas_on_click(self, event):
        """The method called when the canvas is clicked -- Adds a gray Squawker at the point of the event
            Args:
                event: the mouse click"""
        self.canvas.focus_set()
        self.draw_dot(self.world.add_convenient(event.x, event.y,
                                                ["B", 250, 10, 15, 2, 1, tools.random_color(),
                                                 .99, .99, .99, .99, .99, .5, 2], reference.d_versatile_scripts(),
                                                1000))

    def _create_circle(self, x, y, r, **kwargs):
        """A shortcut for creating circles
            Args:
                x: the x value of the center of the circle
                y: the y value of the center of the circle
                r: the radius of the circle
                kwargs: additional styling
            Return:
                an oval widget that represents the circle"""
        return self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def scroll_down(self, event=None):
        self.canvas.yview_scroll(1, what="units")

    def scroll_up(self, event=None):
        self.canvas.yview_scroll(-1, what="units")

    def scroll_left(self, event=None):
        self.canvas.xview_scroll(-1, what="units")

    def scroll_right(self, event=None):
        self.canvas.xview_scroll(1, what="units")

    def _draw_dots(self):
        """"draw dots initialized previously"""
        for c in self.world.occupants:
            self.draw_dot(c)

    def init_dots(self):
        """Initializes dots that will be present at the time the program begins"""
        # g = ["Species", vis, str, size, spe, bur, col, vmf, strmf, szmf, spmf, bmf, colmf, toughness]
        self.world.add_creature(300, 300, ["H", 75, 1, 3, 3, 4, tools.random_color(),
                                            .95, .95, .95, .95, .95, .95, 20], reference.d_versatile_scripts(),
                                 10000, None).get_occupant().set_base_energy(10000)
        self.world.add_creature(900, 300, ["G", 75, 10, 3, 3, 4, tools.random_color(),
                                            .95, .95, .95, .95, .95, .95, 20], reference.d_versatile_scripts(),
                                 10000, None).get_occupant().set_base_energy(10000)
        self.world.add_creature(900, 100, ["I", 75, 10, 3, 3, 4, tools.random_color(),
                                            .95, .95, .95, .95, .95, .95, 20], reference.d_versatile_scripts(),
                                 10000, None).get_occupant().set_base_energy(10000)

    def init_spawners(self):
        """Initializes spawners that will be present at the time the program begins"""
        ps1 = self.world.add_plant_spawner(4, self.CANVAS_HEIGHT, self.CANVAS_WIDTH/4, 0, 0)
        self.spawn_map[ps1.get_special_id()] = ps1
        ps2 = self.world.add_plant_spawner(4, self.CANVAS_HEIGHT, self.CANVAS_WIDTH/4, self.CANVAS_WIDTH*3/4, 0)
        self.spawn_map[ps2.get_special_id()] = ps2
        ps3 = self.world.add_plant_spawner(4, self.CANVAS_HEIGHT / 20, self.CANVAS_WIDTH / 4, self.CANVAS_WIDTH*(3/8), self.CANVAS_HEIGHT*(7/16))
        self.spawn_map[ps3.get_special_id()] = ps3
        ps4 = self.world.add_plant_spawner(4, self.CANVAS_HEIGHT / 20, self.CANVAS_WIDTH / 4,
                                           self.CANVAS_WIDTH * (3 / 8), self.CANVAS_HEIGHT * (15 / 16))
        self.spawn_map[ps4.get_special_id()] = ps4

    def pause(self, event=None):
        """Pauses the simulation"""
        self.running = not self.running

    def draw_dot(self, c):
        """"Draw dot, which had not been initialized
            Args:
                c: the dot reference which needs to be drawn"""
        ref = self._create_circle(c.get_centerx(), c.get_centery(), c.get_radius(), fill=c.get_color(), width=0)
        c.set_reference(ref)
        self.dot_parrallels[ref] = c
        self.canvas.tag_bind(ref, "<Button-2>", lambda event, arg=ref: self.select_dot(event, arg))
        self.canvas.tag_bind(ref, "<Button-3>", lambda event, arg=ref: self.select_dot(event, arg))

    def remove_dot(self, dot):
        """"Destroys dot at every layer of abstraction
            Args:
                dot: the dot that needs to be deleted
            """
        if dot is self.current_selection:
            self.set_current_selection(None)
        del self.dot_parrallels[dot.get_reference()]
        self.canvas.delete(dot.get_reference())
        self.world.occupants.remove(dot)
        if dot.special != -1:
            self.spawn_map[dot.special].remove(dot.get_occupant())

    def select_dot(self, event, ref):
        """Highlights a dot and makes it the Current Selection (or deselects)
            Args:
                event: the mouse click that selects the dot
                ref: the circle reference for the dot"""
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
        """Sets the current selection to and updates the text boxes
            Args:
                dot: the dot to be set as current selection"""
        self.current_selection = dot

    def update(self):
        """The main logic loop of the program"""
        if self.running:
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
        """Changes the visible color of the dot to its actual color
            Args:
                dot: the dot whose color needs to be updated"""
        self.canvas.itemconfigure(dot.get_reference(), fill=dot.get_color())

    def handle_triggers(self, c):
        """Handle the various Dot triggers
            Args:
                c: the dot whose triggers need to be handled"""
        if c.collide_triggered():
            if isinstance(c.get_occupant(), Plant):
                c.kill_trigger()
        if c.ucolor_triggered():
            self.update_color(c)
        if c.reproducing_triggered():
            self.draw_dot(self.world.add(c.reproduce(), c.get_centerx(), c.get_centery()))
        if c.kill_triggered():
            self.remove_dot(c)

    def update_collisions(self, c):
        """Handles collision between dots
            Args:
                c: the dot which is being checked for collisions"""
        overlaps = self.canvas.find_overlapping(c.getx(), c.gety(), c.getx2(), c.gety2())
        doverlaps = []
        for o in overlaps:
            if o != c.get_reference():
                doverlaps.append(self.dot_parrallels[o])
        self.world.handle_collisions(c, doverlaps)

    def update_visions(self, c):
        """Updates each dots vision of nearby dots
            Args:
                c: the dot whose vision is being updated"""
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


class Simulation2(Simulation):
    """A run configuration that sets all parameters and initializations for the simulation"""

    CANVAS_HEIGHT = 4000
    CANVAS_WIDTH = 1800

    def __init__(self, speed):
        """initialization logic
            Args:
                speed: the inverse of targeted fps.  FPStarget = (60/speed)"""
        Simulation.__init__(self, speed)

    def init_additional_gui_elements(self):
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
        Button(action_bar, text="Apply", command=self.apply_cs_changes).pack(fill=NONE, side=LEFT)
        action_bar.pack(side=LEFT)

    def configure_hotkeys(self):
        """Initialize all baseline hotkeys that apply to the whole simulation"""
        self.root.bind("<Tab>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)
        self.root.bind("<space>", self.pause)
        self.root.bind("<Up>", self.scroll_up)
        self.root.bind("<Down>", self.scroll_down)
        self.root.bind("<Right>", self.scroll_right)
        self.root.bind("<Left>", self.scroll_left)
        self.root.bind("<i>", self.print_info)
        self.root.bind("<c>", self.print_current_selection)


    def print_info(self, event=None):
        num_plants = 0
        for o in self.world.occupants:
            if o.special != -1:
                num_plants += 1
        print("****************************")
        print("Total Number of Occupants: ", len(self.world.occupants))
        print("Total Number of Plants: ", num_plants)
        print("****************************")

    def end_fullscreen(self, event=None):
        """forces the screen not to be fullscreen"""
        self.full_screen = False
        self.root.attributes("-fullscreen", False)
        return "break"

    def apply_cs_changes(self):
        """"Applies to the current selection the attributes typed into the text boxes"""
        self.current_selection.set_speed(int(self.csSpeedEntry.get()))
        self.current_selection.set_radius(int(self.csSizeEntry.get()))
        self.world.test_largest_radius(int(self.csSizeEntry.get()))
        self.current_selection.set_color(self.csColorEntry.get())
        self.canvas.update()

    def canvas_on_click(self, event):
        """The method called when the canvas is clicked -- Adds a gray Squawker at the point of the event
            Args:
                event: the mouse click"""
        self.canvas.focus_set()
        self.draw_dot(self.world.add_plant(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y), 5000))

    def init_dots(self):
        """Initializes dots that will be present at the time the program begins"""
        # g = ["Species", vis, str, size, spe, bur, col, vmf, strmf, szmf, spmf, bmf, colmf, toughness]
        self.world.add_creature(1500, 3400, ["G", 150, 10, 3, 3, 4, tools.random_color(),
                                            .95, .95, .95, .95, .95, .95, 20], reference.d_versatile_scripts(),
                                 10000, None).get_occupant().set_base_energy(10000)
        self.world.add_creature(1500, 100, ["I", 150, 10, 3, 3, 4, tools.random_color(),
                                            .95, .95, .95, .95, .95, .95, 20], reference.d_versatile_scripts(),
                                 10000, None).get_occupant().set_base_energy(10000)

    def init_spawners(self):
        """Initializes spawners that will be present at the time the program begins"""
        ps1 = self.world.add_plant_spawner(4, self.CANVAS_HEIGHT, self.CANVAS_WIDTH/5, 0, 0)
        self.spawn_map[ps1.get_special_id()] = ps1
        ps2 = self.world.add_plant_spawner(4, self.CANVAS_HEIGHT, self.CANVAS_WIDTH/5, self.CANVAS_WIDTH*3/4, 0)
        self.spawn_map[ps2.get_special_id()] = ps2
        ps3 = self.world.add_plant_spawner(4, self.CANVAS_HEIGHT / 20, self.CANVAS_WIDTH / 4, self.CANVAS_WIDTH*(3/8), self.CANVAS_HEIGHT*(7/16))
        self.spawn_map[ps3.get_special_id()] = ps3
        ps4 = self.world.add_plant_spawner(4, self.CANVAS_HEIGHT / 20, self.CANVAS_WIDTH / 4,
                                           self.CANVAS_WIDTH * (3 / 8), self.CANVAS_HEIGHT * (15 / 16))
        self.spawn_map[ps4.get_special_id()] = ps4

    def set_current_selection(self, dot):
        """Sets the current selection to and updates the text boxes
            Args:
                dot: the dot to be set as current selection"""
        self.current_selection = dot
        if dot is not None:
            self.print_current_selection()

    def print_current_selection(self, event=None):
        if self.current_selection is not None:
            print("----------------------------")
            print(self.current_selection.get_occupant())
            print(self.current_selection.to_string())
            print("----------------------------")

    def _add_callback(self):
        """The method called when 'ADD' is clicked -- Adds a convenient at the point of the event"""
        self.draw_dot(self.world.add_convenient(int(self.xEntry.get()), self.yEntry.get(),
                                                ["B", 250, 10, 15, 2, 1, tools.random_color(),
                                                 .99, .99, .99, .99, .99, .5, 2], reference.d_versatile_scripts(),
                                                10000))

    def _pause_callback(self, event=None):
        """The method called when 'PAUSE' is clicked -- pauses the program"""
        self.pause()

    def _kill_callback(self):
        """Sets the kill trigger the current selection"""
        self.current_selection.kill_trigger()

    def _slowdown_callback(self):
        """The method called when 'SLOW DOWN' is clicked -- Slows down the main loop"""
        self.speed += 1

    def _speedup_callback(self):
        """The method called when 'ADD' is clicked -- Speeds up the main loop"""
        if self.speed > 1:
            self.speed -= 1


Simulation2(1)
