import numpy as np

from point import Point
from task2.raytracing import normalize


class Figure:
    def __init__(self, a, d):
        self.ambient = np.array(a)
        self.diffuse = np.array(d)
        self.specular = np.array([255, 255, 255])

    def intersect(self):
        pass

    def get_normal(self, intersection):
        pass


class Wall(Figure):
    def __init__(self, p1, p2, ambient, diffuse, normal=None):
        super().__init__(ambient, diffuse)
        self.p1 = np.array([p1.x, p1.y, p1.z])
        self.p2 = np.array([p2.x, p2.y, p2.z])
        self.p3 = np.array([p1.x, p2.y, p1.z])
        self.p4 = np.array([p2.x, p1.y, p2.z])
        if (self.p3 == self.p1).all() or (self.p3 == self.p2).all():
            self.p3 = np.array([ p1.x, p1.y, p2.z])
            self.p4 = np.array([p2.x, p1.y, p1.z])
        self.center = np.array([(p2.x - p1.x) / 2, (p2.y - p1.y) / 2, (p2.z - p1.z) / 2])
        if normal is None:
            self.normal = self.update_normal()
        else:
            self.normal = np.array(normal)

    def update_normal(self):
        v1 = self.p2 - self.p1
        v2 = self.p3 - self.p1
        return normalize(np.cross(v1, v2))

    def intersect(self, origin, direction):
        if np.equal(normalize(origin), self.normal).all():
            return None
        a = self.intersect_triangle(self.p1, self.p2, self.p3, origin, direction)
        b = self.intersect_triangle(self.p1, self.p2, self.p4, origin, direction)
        return a or b

    def intersect_triangle(self, p1, p2, p3, origin, direction):
        e1 = p2 - p1
        e2 = p3 - p1
        pvec = np.cross(direction, e2)
        det = np.dot(e1, pvec)
        if det < 1e-8 and det > -1e-8:
            return None
        inv_det = 1 / det
        tvec = origin - self.p1
        u = np.dot(tvec, pvec) * inv_det
        if u < 0 or u > 1:
            return 0
        qvec = np.cross(tvec, e1)
        v = np.dot(direction, qvec) * inv_det
        if v < 0 or u + v > 1:
            return 0
        return np.dot(e2, qvec) * inv_det

    def get_normal(self, intersection):
        return self.normal


class Sphere(Figure):
    def __init__(self, ambient, diffuse, center, radius):
        super().__init__(ambient, diffuse)
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

    def get_normal(self, intersection):
        return normalize(intersection - self.center)


class LightSource:
    def __init__(self, center, intense):
        self.center = np.array(center)
        self.radius = 2
        self.intense = intense
