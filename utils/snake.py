# Dillan Spencer
# Snake for battle snake
from .utils import Move
import json

class Snake():
    
    def __init__(self, body):
        self.body = [json.loads(point) for point in body]
        self.head = json.loads(body[0])
        self.neck = json.loads(body[1])
        self.tail = json.loads(body[len(body) - 1])
        self.alive = True
        self.score = 0

    def getMoves(self):
        moves = []
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
        self.neck = json.loads(self.body[1])
        self.tail = json.loads(self.body[len(self.body) - 1])

    def eat(self):
        self.body.append(self.tail)
        self.score += 1

    def die(self):
        self.alive = False
        return self.body    

    

    


