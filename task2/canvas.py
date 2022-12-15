from tkinter import Canvas, PhotoImage

from task1.functions import draw_pix, rgb2hex
from task2.point import Point


class MyCanvas(Canvas):
    def __init__(self, tk, width, height, bg="white"):
        super().__init__(tk, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.camera = (0,0,300)
        self.light = None
        self.create_image()

    def set_center(self, x, y, z=0):
        self.center = Point(x, y, z)

    def create_image(self, state="normal"):
        self.image = PhotoImage(width=self.width, height=self.height)
        super().create_image((self.width / 2, self.height / 2), image=self.image, state=state)

    def clear(self):
        self.delete('all')
        self.create_image()

    def put_pixel(self, x, y, color=(0, 0, 0)):
        draw_pix(self.image, (x, y), color)

    def draw_line(self, p0, p1, color=(0, 0, 0), thickness=2):
        rp0 = round(p0[0]), round(p0[1])
        rp1 = round(p1[0]), round(p1[1])
        self.create_line(rp0[0], rp0[1], rp1[0], rp1[1], fill=rgb2hex(color), width=thickness)


class StorageCanvas(MyCanvas):
    def __init__(self, tk, width, height, bg="white"):
        super().__init__(tk, width=width, height=height, bg=bg)
        self.storage = Storage([], self)

    def redraw(self):
        self.clear()
        self.storage.draw(self)

    def delete_content(self):
        self.storage.delete_all()
        self.clear()

    def delete_selected(self):
        self.storage.delete_selected()
        self.redraw()


class Storage:
    def __init__(self, figs, canvas):
        self.canvas = canvas
        self.figs = figs

    def add_figure(self, fig):
        self.figs.append(fig)
        # fig.draw(self.canvas)

    def draw(self, canvas):
        for fig in self.figs:
            fig.draw(canvas)

    def delete_all(self):
        self.figs = []

    def delete_selected(self):
        self.figs = [fig for fig in self.figs if not fig.selected]

    def call(self, func):
        res = []
        for fig in self.figs:
            res += func(fig)
        return res


class Scene:
    def __init__(self):
        self.storage = []
        self.camera = None
        self.light = None

    def add_figure(self, figure):
        self.storage.append(figure)

    def clear(self):
        self.storage = []
