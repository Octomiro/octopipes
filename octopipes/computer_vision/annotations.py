from dataclasses import dataclass

@dataclass
class Bbox:
    x0: int
    y0: int
    x1: int
    y1: int

    def to_list(self):
        return [self.x0, self.y0, self.x1, self.y1]

@dataclass
class Point:
    x: int
    y: int
    z: int

    def to_list(self):
        return [self.x, self.y, self.z]

@dataclass
class Circle:
    x: int
    y: int
    r: int | float

    def to_list(self):
        return [self.x, self.y, self.r]
