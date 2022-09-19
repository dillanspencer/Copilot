import random
import copy
import math
import time
from utils.snake import Snake
from utils.utils import Move, Point
from threading import Thread

class MinMaxThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

# iterative deepening algorithm using maxN algorithm with alpha beta pruning
def iterativeDeepening(mySnake, enemySnakes, food, depth) -> Move:
    bestMove = Move.RIGHT
    startTime = time.time()
    alpha = -math.inf
    beta = math.inf
    threads = [None] * depth - 1
    for i in range(1, depth):
        threads[i] = MinMaxThread(target=maxN, args=(mySnake, enemySnakes, food, i, alpha, beta, startTime))
        threads[i].start()
        

    for i in range(len(threads) - 1):
        val = threads[i].join
        print("BEST MOVE: ", i, val)
    return bestMove

# maxN algorithm with alpha beta pruning
def maxN(mySnake, enemySnakes, food, depth, alpha, beta, returnDepth) -> Move:
    if depth == 0 or time.time() - returnDepth > 0.135:
        heuristicValue = heuristic(mySnake, enemySnakes, food)
        return heuristicValue
    bestValue = -math.inf
    bestMove = None
    for move in mySnake.getMoves(enemySnakes):
        newMySnake = copy.deepcopy(mySnake)
        newMySnake.move(move)
        newEnemySnakes = copy.deepcopy(enemySnakes)
        for enemySnake in newEnemySnakes:
            enemySnake.move(random.choice(enemySnake.getMoves()))
        value = minN(newMySnake, newEnemySnakes, food, depth - 1, alpha, beta, returnDepth)
        if value > bestValue:
            bestValue = value
            bestMove = move
        alpha = max(alpha, bestValue)
        if alpha >= beta:
            break
    if depth == 6 :
        return bestMove
    return bestValue

# minN algorithm with alpha beta pruning
def minN(mySnake, enemySnakes, food, depth, alpha, beta, returnDepth):
    if depth == 0:
        return heuristic(mySnake, enemySnakes, food)
    bestValue = math.inf
    for enemySnake in enemySnakes:
        for move in enemySnake.getMoves():
            newMySnake = copy.deepcopy(mySnake)
            newEnemySnakes = copy.deepcopy(enemySnakes)
            for enemySnake in newEnemySnakes:
                enemySnake.move(move)
            value = maxN(newMySnake, newEnemySnakes, food, depth - 1, alpha, beta, returnDepth)
            bestValue = min(bestValue, value)
            beta = min(beta, bestValue)
            if alpha >= beta:
                break
    return bestValue
         

# heuristic function for the minmax algorithm that takes account being close to the center and not moving out of bounds
def heuristic(mySnake, enemySnakes, food):
    myHead = mySnake.head
    myDistance = 0
    foodPoint = 0
    
    for enemySnake in enemySnakes:
        # check if snake hit enemy body
        if mySnake.head.distance(enemySnake.head) == 0:
            print("RUN into enemy head")
            return -math.inf

    foodDist = myHead.distance(food[0])
    for point in food:
        foodDist = min(foodDist, mySnake.head.distance(point))
        
    return -foodDist
    
