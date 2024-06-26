import dataclasses


@dataclasses.dataclass
class Point:
    x: int
    y: int

    @staticmethod
    def create(x, y):
        return Point(x=x, y=y)
