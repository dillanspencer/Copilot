# Dillan Spencer
# Snake for battle snake
from .utils import Move, Point
import json

class Snake():
    
    def __init__(self, id, body):
        self.id = id
        self.body = [Point(point["x"], point["y"]) for point in body]
        self.head = Point(body[0]["x"], body[0]["y"])
        self.neck = Point(body[1]["x"], body[1]["y"])
        self.tail = Point(body[len(body) - 1]["x"], body[len(body) - 1]["y"])  
        self.length = len(body)

    def getMoves(self, enemySnakes=[]):
        moves = []
        if self.head.x >= self.neck.x and Point(self.head.x + 1, self.head.y) not in self.body and self.head.x < 11:          
            moves.append(Move.RIGHT)
        if self.head.x <= self.neck.x and Point(self.head.x - 1, self.head.y) not in self.body and self.head.x > 0:
            moves.append(Move.LEFT)
        if self.head.y >= self.neck.y and Point(self.head.x, self.head.y + 1) not in self.body and self.head.y < 11:
            moves.append(Move.UP)
        if self.head.y <= self.neck.y and Point(self.head.x, self.head.y - 1) not in self.body and self.head.y > 0:
            moves.append(Move.DOWN)

        if enemySnakes:
            for enemySnake in enemySnakes:
                if Point(self.head.x + 1, self.head.y) in enemySnake.body[1:]:
                    if Move.RIGHT in moves:
                        moves.remove(Move.RIGHT)
                if Point(self.head.x - 1, self.head.y) in enemySnake.body[1:]:
                    if Move.LEFT in moves:
                        moves.remove(Move.LEFT)
                if Point(self.head.x, self.head.y + 1) in enemySnake.body[1:]:
                    if Move.UP in moves:
                        moves.remove(Move.UP)
                if  Point(self.head.x, self.head.y - 1) in enemySnake.body[1:]:
                    if Move.DOWN in moves:
                        moves.remove(Move.DOWN)
            print(moves)
        return moves

    
    def move(self, move):
        if move == Move.LEFT:
            self.head.x -= 1
        if move == Move.RIGHT:
            self.head.x += 1
        if move == Move.UP:
            self.head.y += 1
        if move == Move.DOWN:
            self.head.y -= 1
        self.body.insert(0, self.head)
        self.body.pop()
        self.neck = Point(self.body[1].x, self.body[1].y)
        self.tail = Point(self.body[len(self.body) - 1].x, self.body[len(self.body) - 1].y)


    

    


