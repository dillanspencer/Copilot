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

    def getPoint(self) -> tuple:
        return (self.x, self.y)

class Food(Point):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)


class Tile(Enum):
    EMPTY = 0
    FOOD = 1
    SNAKE = 2
    WALL = 3
    HEAD = 4
    ME = 5