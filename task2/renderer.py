import numpy as np
from point import Point
from math import pi, tan, cos, sin, asin, acos


class Renderer:
    def __init__(self, canvas):
        self.gridX = True
        self.gridY = False
        self.gridZ = False
        self.camera = None
        self.canvas = canvas
        self.projection = [[1, 0,0,0],
            [0, 1,0,0],
            [0, 0,1,0.005],
            [0, 0,0,1]] #перспективная
        self.center = Point(self.canvas.width / 2, self.canvas.height / 2)
        self.axis_bound = 200

    def render_scene(self, scene):
        self.canvas.clear()
        for figure in scene.storage:
            figure.draw(self)

    def draw_line(self, points, color=(0, 0, 0), thickness=2):
        points = [self.translate3D_point(p) for p in points]
        self.canvas.draw_line((points[0].x, points[0].y), (points[1].x, points[1].y), color, thickness=thickness)

    def translate3D_point(self, point):
        p0 = np.array([[point.x, point.y, point.z, 1]])
        p0 = np.dot(p0, self.projection)
        p = p0[0]
        return self.center + Point(p[0] / p[3], -(p[1] / p[3]), point.z)


