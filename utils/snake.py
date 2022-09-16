# Dillan Spencer
# Snake for battle snake
from .utils import Move, Point
import json

class Snake():
    
    def __init__(self, body):
        self.body = [Point(point["x"], point["y"]) for point in body]
        self.head = Point(body[0]["x"], body[0]["y"])
        self.neck = Point(body[1]["x"], body[1]["y"])
        self.tail = Point(body[len(body) - 1]["x"], body[len(body) - 1]["y"])
        self.alive = True
        self.score = 0

    def getMoves(self):
        moves = []
        print("HEAD: ", self.head.x, self.head.y)
        print("NECK: ", self.neck.x, self.neck.y)
        if self.head.x > self.neck.x:
            moves.append(Move.LEFT)
        if self.head.x < self.neck.x:
            moves.append(Move.RIGHT)
        if self.head.y > self.neck.y:
            moves.append(Move.UP)
        if self.head.y < self.neck.y:
            moves.append(Move.DOWN)
        return moves

    def move(self, move):
        if move == Move.LEFT:
            self.head.x -= 1
        if move == Move.RIGHT:
            self.head.x += 1
        if move == Move.UP:
            self.head.y -= 1
        if move == Move.DOWN:
            self.head.y += 1
        self.body.insert(0, self.head)
        self.body.pop()
        self.neck = self.body[1]
        self.tail = self.body[len(self.body) - 1]

    def eat(self):
        self.body.append(self.tail)
        self.score += 1

    def die(self):
        self.alive = False
        return self.body    

    

    


