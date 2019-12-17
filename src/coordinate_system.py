import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Coordinate:
    def __init__(self, longitude, latitude):
        self.latitude = latitude
        self.longitude = longitude


class CoordinateSystem:
    def __init__(self, shape: tuple, top_left: Coordinate, bottom_right: Coordinate):
        self.width, self.height = shape
        y1, x1 = top_left.latitude, top_left.longitude
        y2, x2 = bottom_right.latitude, bottom_right.longitude

        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        self.bottom_left = Point(x1, y1)
        self.top_right = Point(x2, y2)

        self.x_scale = self.width / (x2 - x1)
        self.y_scale = self.height / (y2 - y1)

    def to_cartesian_int(self, longitude: float, latitude: float):
        dx = longitude - self.bottom_left.x
        dy = latitude - self.bottom_left.y

        i, j = np.round(dx * self.x_scale), np.round(dy * self.y_scale)

        if i < 0 or i >= self.width:
            return None

        if j < 0 or j >= self.height:
            return None

        # for points that out of bounds
        # i = int(np.clip(i, 0, self.width - 1))
        # j = int(np.clip(j, 0, self.height - 1))

        return Point(i, j)

    def to_cartesian_float(self, longitude: float, latitude: float):
        dx = longitude - self.bottom_left.x
        dy = latitude - self.bottom_left.y

        i, j = dx * self.x_scale, dy * self.y_scale

        if i > self.width:
            i = self.width

        if j > self.height:
            j = self.height

        return Point(i, j)
