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
        x1, y1 = top_left.latitude, top_left.longitude
        x2, y2 = bottom_right.latitude, bottom_right.longitude

        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        self.bottom_left = Point(x1, y1)
        self.top_right = Point(x2, y2)

        self.x_scale = self.width / (x2 - x1)
        self.y_scale = self.height / (y2 - y1)

    def to_cartesian(self, longitude: float, latitude: float):
        dx = latitude - self.bottom_left.x
        dy = longitude - self.bottom_left.y

        i, j = np.round(dx * self.x_scale), np.round(dy * self.y_scale)

        # for points that out of bounds
        i = int(np.clip(i, 0, self.width - 1))
        j = int(np.clip(j, 0, self.height - 1))

        return Point(i, j)