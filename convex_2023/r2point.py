from math import sqrt


class R2Point:
    """ Точка (Point) на плоскости (R2) """

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))
        if y is None:
            y = float(input("y -> "))
        self.x, self.y = x, y

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x))

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (((a.x <= self.x and self.x <= b.x) or
                 (a.x >= self.x and self.x >= b.x)) and
                ((a.y <= self.y and self.y <= b.y) or
                 (a.y >= self.y and self.y >= b.y)))

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = R2Point.area(a, b, self)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))

    # Совпадает ли точка с другой?
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False

    @staticmethod
    def dist_bw_seg(a, b, c, d):
        distance1 = R2Point.distance_point_to_segment(a.x, a.y, c, d)
        distance2 = R2Point.distance_point_to_segment(b.x, b.y, c, d)
        distance3 = R2Point.distance_point_to_segment(c.x, c.y, a, b)
        distance4 = R2Point.distance_point_to_segment(d.x, d.y, a, b)
        return min(distance1, distance2, distance3, distance4)

    @staticmethod
    def distance_point_to_segment(x, y, a, b):
        vector1_x = x - a.x
        vector1_y = y - a.y
        vector2_x = b.x - a.x
        vector2_y = b.y - a.y
        projection = (vector1_x * vector2_x + vector1_y * vector2_y) / \
                     (vector2_x ** 2 + vector2_y ** 2)
        if projection <= 0:
            # Точка ближе к началу отрезка
            return sqrt((x - a.x) ** 2 + (y - a.y) ** 2)
        elif projection >= 1:
            # Точка ближе к концу отрезка
            return sqrt((x - b.x) ** 2 + (y - b.y) ** 2)
        else:
            # Точка ближе к промежуточной точке на отрезке
            projection_point = (a.x + projection * vector2_x,
                                a.y + projection * vector2_y)
            return sqrt((x - projection_point[0]) ** 2 +
                        (y - projection_point[1]) ** 2)


if __name__ == "__main__":
    x = R2Point(1.0, 1.0)
    print(type(x), x.__dict__)
    print(x.dist(R2Point(1.0, 0.0)))
    a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
    print(R2Point.area(a, c, b))
