import numpy as np

from point import Point


class Figure:
    def __init__(self, color):
        self.initial_color = np.array(color)

    def intersect(self):
        pass


class Wall(Figure):
    def __init__(self, p1, p2, normal, color=[255, 255, 255]):
        super().__init__(color)
        self.p1 = p1
        self.p2 = np.array([p2.x, p2.y, p2.z])
        self.center = np.array([(p2.x-p1.x)/2,(p2.y-p1.y)/2,(p2.z-p1.z)/2])
        self.normal = normal

    def intersect(self, origin, direction):
        diff = origin - self.p2
        prod1 = np.dot(diff, self.normal)
        prod2 = np.dot(direction, self.normal)
        if prod2 <= 0:
            return None
        prod3 = -prod1 / prod2

        if prod3 < 0.000001:
            return None
        interPoint = Point(origin[0] + prod3 * direction[0], origin[1] + prod3 * direction[1],
                           origin[2] + prod3 * direction[2])
        if self.pointInPlane(interPoint):
            return prod3
        else:
            return None

    def pointInPlane(self, point):
        xval = point.x - max(self.p2[0], self.p1.x) <= 0.00001 and point.x - min(self.p2[1], self.p1.x) >= -0.00001
        yval = (point.y - max(self.p2[1], self.p1.y) <= 0.00001) and (
                point.y - min(self.p2[1], self.p1.y) >= -0.00001)
        zval = (point.z - max(self.p2[2], self.p1.z) <= 0.00001) and (
                point.z - min(self.p2[2], self.p1.z) >= -0.00001)

        return xval and yval and zval


class Sphere(Figure):
    def __init__(self, color, center, radius):
        super().__init__(color)
        self.center = center
        self.radius = radius

    def intersect(self, origin, direction):
        b = 2 * np.dot(direction, origin - self.center)
        c = np.linalg.norm(origin - self.center) ** 2 - self.radius ** 2
        delta = b ** 2 - 4 * c
        if delta > 0:
            t1 = (-b + np.sqrt(delta)) / 2
            t2 = (-b - np.sqrt(delta)) / 2
            if t1 > 0 and t2 > 0:
                return min(t1, t2)
        return None


class LightSource:
    def __init__(self, center, intense):
        self.center = center
        self.radius = 2
        self.intense = intense
