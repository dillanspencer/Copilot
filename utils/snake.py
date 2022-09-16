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

    def getMoves(self):
        moves = []
        if self.head.x >= self.neck.x:
            moves.append(Move.RIGHT)
        if self.head.x <= self.neck.x:
            moves.append(Move.LEFT)
        if self.head.y >= self.neck.y:
            moves.append(Move.UP)
        if self.head.y <= self.neck.y:
            moves.append(Move.DOWN)
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


    

    


