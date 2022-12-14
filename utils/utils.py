from enum import Enum

class Move(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"

class Point():
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self. y = y

    def __eq__(self, point) -> bool:
        return self.x == point.x and self.y == point.y

    def distance(self, point) -> int:
        return abs(self.x - point.x) + abs(self.y - point.y)

    def getPoint(self) -> tuple:
        return (self.x, self.y)

    def getPoint3D(self) -> tuple:
        return (self.x, self.y, 0)

class Food(Point):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)


class Tile(Enum):
    EMPTY = 'e'
    FOOD = 'f'
    SNAKE = 's'
    WALL = 'w'
    HEAD = 'h'
    ME = 'm'

class Entry(Enum):
    EXACT = 0
    LOWERBOUND = 1
    UPPERBOUND = 2