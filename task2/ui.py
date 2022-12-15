from tkinter import Tk

import numpy as np

from task1.functions import rgb2hex
from task2.canvas import Scene, StorageCanvas
from task2.figure import Sphere, Wall, LightSource
from task2.point import Point
from task2.raytracing import raytracing
from task2.renderer import Renderer


class UI(Tk):
    def __init__(self, title="Корнуэльская комната", width=300, height=300):
        super().__init__()
        self.variables = []
        if width == 0:
            self.win_width = self.winfo_screenwidth()
        else:
            self.win_width = width
        if height == 0:
            self.win_height = self.winfo_screenheight()
        else:
            self.win_height = height

        self.title(title)
        self.create_canvas()
        self.create_renderer()
        self.scene = Scene()

    def create_canvas(self):
        self.canv = StorageCanvas(self, width=self.win_width, height=self.win_height, bg="white")
        self.canv.grid(row=1, column=2)

    def create_renderer(self):
        self.renderer = Renderer(self.canv)

    def setup_room(self):
        # room
        self.canv.storage.add_figure(Wall(Point(-25, -25, 70), Point(25, 25, 70), [0, 0, -1]))
        self.canv.storage.add_figure(Wall(Point(-25, -25, -70), Point(25, -25, 70), [0, 1, 0]))
        self.canv.storage.add_figure(Wall(Point(-25, 25, 70), Point(25, 25, 70), [0, -1, 0]))
        self.canv.storage.add_figure(Wall(Point(-25, -25, -70), Point(-25, 25, 70), [1, 0, 0]))
        self.canv.storage.add_figure(Wall(Point(25, -25, -70), Point(25, 25, 70), [-1, 0, 0]))
        self.canv.storage.add_figure(Wall(Point(-25, -25, -70), Point(25, 25, -70), [0, 0, 1]))
        # sphere
        self.canv.storage.add_figure(Sphere([255, 0, 255], (-18, -20, 55), 15))
        self.canv.light = LightSource((30,100,0), np.array([0.3, 0.3, 0.3]))
        p = self.renderer.translate3D_point(Point(self.canv.light.center[0],self.canv.light.center[1],self.canv.light.center[2]))
        raytracing(self.canv, self.win_width, self.win_height)
        self.canv.create_oval(p.x - self.canv.light.radius, p.y - self.canv.light.radius, p.x + self.canv.light.radius, p.y + self.canv.light.radius, fill=rgb2hex((0,255,0)), outline=rgb2hex((0,255,0)))


    def run(self):
        self.mainloop()
