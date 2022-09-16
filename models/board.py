
from utils.utils import Tile


class Board():
    def __init__(self, width, height, snakes, food, you):
        self.width = width
        self.height = height
        self.snakes = snakes
        self.food = food
        self.you = you
        self.board = [[Tile.EMPTY for x in range(width)] for y in range(height)]
        self.loadBoard()
        
    def loadBoard(self):
        for snake in self.snakes:
            for point in snake.body:
                self.board[point.y][point.x] = Tile.SNAKE
            self.board[snake.head.y][snake.head.x] = Tile.HEAD
            if snake.id == self.you.id:
                self.board[snake.head.y][snake.head.x] = Tile.ME
        for food in self.food:
            self.board[food["x"]][food["y"]] = Tile.FOOD