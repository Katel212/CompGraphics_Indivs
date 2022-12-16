import numpy as np


def raytracing(canv, width, height):
    camera = np.array([0, 0, -20])
    for x in range(width):
        for y in range(height):
            r = vector_ray(x, y, width, height)
            col = ray(camera, r, canv.storage.figs, canv.light)
            canv.put_pixel(x, y, col)


def vector_ray(x, y, width, height):
    return normalize(np.array([100*x/width - 50, -1 * (100*y/ height - 50), 100]))


def normalize(vector):
    return vector / np.linalg.norm(vector)


def ray(camera, direction, storage, light):
    nearest_object, min_distance = nearest_intersected_object(storage, camera, direction)
    if nearest_object is None:
        return (255, 255, 255)
    intersection = camera + min_distance * direction

    normal_to_surface = nearest_object.get_normal(intersection)
    shifted_point = intersection + 1e-5 * normal_to_surface
    intersection_to_light = normalize(light.center - shifted_point)

    _, min_distance = nearest_intersected_object(storage, shifted_point, intersection_to_light)

    intersection_to_light_distance = np.linalg.norm(light.center - intersection)
    is_shadowed = min_distance < intersection_to_light_distance

    illumination = np.zeros((3))

    # ambiant
    illumination += nearest_object.ambient * light.intense
    if is_shadowed:
        color = np.clip(illumination.astype(int), 0, 255)
        return (color[0], color[1], color[2])
    illumination += nearest_object.diffuse * light.intense * np.dot(intersection_to_light, normal_to_surface)
    intersection_to_camera = normalize(camera - intersection)
    H = normalize(intersection_to_light + intersection_to_camera)
    illumination += nearest_object.specular * light.intense * np.dot(normal_to_surface, H) ** (
                100/ 4)

    color = np.clip(illumination.astype(int),0,255)
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
