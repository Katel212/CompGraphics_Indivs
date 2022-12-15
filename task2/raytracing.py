import numpy as np

from task2.point import Point


def raytracing(canv, width, height):
    lookup = np.array([0, 0, -20])
    for i in range(width):
        for j in range(height):
            r = vector_ray(i, j, width, height)
            col = ray(lookup, r, canv.storage.figs, canv.light)
            canv.put_pixel(i, j, col)


def vector_ray(i, j, width, height):
    return normalize(np.array([(i - width / 2) * (100.0 / width), (j - height / 2) * (-1) * (100.0 / height), 100]))


def normalize(vector):
    return vector / np.linalg.norm(vector)


def ray(lookup, direction, storage, light):
    nearest_object, min_distance = nearest_intersected_object(storage, lookup, direction)
    if nearest_object is None:
        return (255, 255, 255)
    intersection = lookup + min_distance * direction
    normal_to_surface = normalize(intersection - nearest_object.center)
    shifted_point = intersection + 1e-5 * normal_to_surface
    intersection_to_light = normalize(light.center - shifted_point)

    _, min_distance = nearest_intersected_object(storage, shifted_point, intersection_to_light)

    intersection_to_light_distance = np.linalg.norm(light.center - intersection)
    is_shadowed = min_distance < intersection_to_light_distance

    if is_shadowed:
        return (0,0,0)

    illumination = np.zeros((3))

    # ambiant
    illumination += nearest_object.initial_color * light.intense
    illumination += nearest_object.initial_color * light.intense * np.dot(intersection_to_light, normal_to_surface)
    color = illumination.astype(int)
    return (color[0], color[1], color[2])


def nearest_intersected_object(storage, cam, direction):
    distances = [obj.intersect(cam, direction) for obj in storage]
    nearest_object = None
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = storage[index]
    return nearest_object, min_distance
