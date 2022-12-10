import math


# нахождение уравнения прямой (её коээфициентов)
def equation(p1, p2):
    a = p2[1] - p1[1]
    b = p1[0] - p2[0]
    c = -p1[0] * a - p1[1] * b
    if b < 0:
        return -1 * a, -1 * b, -1 * c
    return a, b, c


# нахождение расстояния между точкой и прямой
def distance(p1, p2, p):
    a, b, c = equation(p1, p2)
    return abs(a * p[0] + b * p[1] + c) / math.sqrt(a ** 2 + b ** 2)


# создание множеств точек над и под прямой
def create_sets(p1, p2, arr):
    above = []
    below = []
    if p1[0] == p2[0] == 0:
        return above, below
    a, b, c = equation(p1, p2)
    for p in arr:
        if a * p[0] + b * p[1] + c > 0:
            above.append(p)
        elif a * p[0] + b * p[1] + c < 0:
            below.append(p)
    return above, below


def quickhull(p1, p2, segment, flag):
    if segment == [] or p1 is None or p2 is None:
        return []
    convex_hull = []
    farthest_distance = -1
    farthest_point = None
    for point in segment:  # находим самую удаленную точку
        dist = distance(p1, p2, point)
        if dist > farthest_distance:
            farthest_distance = dist
            farthest_point = point
    convex_hull = convex_hull + [farthest_point]
    segment.remove(farthest_point)
    p1a, p1b = create_sets(p1, farthest_point, segment)
    p2a, p2b = create_sets(farthest_point, p2, segment)
    if flag == 'above':  # если точки над начальной прямой, то и все следующие будут над новой прямой
        convex_hull += quickhull(p1, farthest_point, p1a, 'above')
        convex_hull += quickhull(farthest_point, p2, p2a, 'above')
    else:
        convex_hull += quickhull(p1, farthest_point, p1b, 'below')
        convex_hull += quickhull(farthest_point, p2, p2b, 'below')
    return convex_hull


def draw_hull(canvas):
    if len(canvas.points) <= 2:
        return
    QuickHull(canvas)
    previous = canvas.hull[0]
    for i in range(1, len(canvas.hull)):  # отрисовываем оболочку
        canvas.create_line(previous[0], previous[1], canvas.hull[i][0], canvas.hull[i][1])
        previous = canvas.hull[i]
    canvas.create_line(previous[0], previous[1], canvas.hull[0][0], canvas.hull[0][1])
    print('hull is done')


def QuickHull(canvas):
    sort = sorted(canvas.points, key=lambda x: x[0])
    p1 = sort[0]
    p2 = sort[len(sort) - 1]
    sort.pop(0)
    sort.pop(len(sort) - 1)

    convex_hull = [p1]  # стартовая точка (самая левая)
    above, below = create_sets(p1, p2, sort)  # находим множества точек под и над начальной прямой
    convex_hull += sorted(quickhull(p1, p2, above, 'above'),
                          key=lambda x: x[0])  # запускаем нахождение оболочки для всех точек над прямой
    convex_hull += [p2]  # самая правая точка
    convex_hull += sorted(quickhull(p1, p2, below, 'below'), key=lambda x: x[0],
                          reverse=True)  # запускаем нахождение оболочки для всех точек под прямой
    canvas.hull = convex_hull