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
        # передняя
        self.canv.storage.add_figure(
            Wall(Point(25, 25, 70), Point(-25, -25, 70), [255, 255, 255], [230, 230, 230], [0, 0, -1]))
        # нижняя
        self.canv.storage.add_figure(
            Wall(Point(-25, -25, -70), Point(25, -25, 70), [255, 255, 255], [230, 230, 230], [0, 1, 0]))
        # верхняя
        self.canv.storage.add_figure(
            Wall(Point(-25, 25, 70), Point(25, 25, -70), [255, 255, 255], [230, 230, 230], [0, -1, 0]))
        # левая
        self.canv.storage.add_figure(
            Wall(Point(-25, -25, -70), Point(-25, 25, 70), [255, 0, 0], [200, 0, 0], [1, 0, 0]))
        # правая
        self.canv.storage.add_figure(
            Wall(Point(25, -25, -70), Point(25, 25, 70), [0, 0, 255], [0, 0, 200], [-1, 0, 0]))
        # передняя
        self.canv.storage.add_figure(
             Wall(Point(25, 25, -30), Point(-25, -25, -30), [255, 255, 0], [200, 200, 0], [0, 0, 1]))
        # sphere
        self.canv.storage.add_figure(Sphere([255, 0, 255], [230, 0, 230], (-14, -14, 50), 10))
        self.canv.light = LightSource([5, 20, 40], np.array([0.5, 0.5, 0.5]))
        raytracing(self.canv, self.win_width, self.win_height)

    def run(self):
        self.mainloop()
