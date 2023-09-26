from deq import Deq
from r2point import R2Point
from math import sqrt


class Figure:
    """ Абстрактная фигура """

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)

    def count(self):
        return 0


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)

    def count(self):
        return 0


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r)
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return self

    def count(self):
        return 0


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c):
        self.points = Deq()
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            self.points.push_first(t)

            return self

    def count(self):
        c = 0
        for i in range(self.points.size() - 1):
            for k in range(i + 1, self.points.size()):
                if k + 1 > self.points.size() - 1:
                    l = 0
                else:
                    l = k + 1
                if self.dist_bw_seg(self.points.array[i],
                                    self.points.array[i + 1],
                                    self.points.array[k],
                                    self.points.array[l]) <= 1:
                    c += 1
        return c

    def dist_bw_seg(self, a, b, c, d):
        distance1 = self.distance_point_to_segment(a.x, a.y, c, d)
        distance2 = self.distance_point_to_segment(b.x, b.y, c, d)
        distance3 = self.distance_point_to_segment(c.x, c.y, a, b)
        distance4 = self.distance_point_to_segment(d.x, d.y, a, b)
        return min(distance1, distance2, distance3, distance4)

    def distance_point_to_segment(self, x, y, a, b):
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
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
