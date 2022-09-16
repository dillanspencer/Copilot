import random
import copy
import math
import time
from utils.snake import Snake
from utils.utils import Move, Point

# iterative deepening algorithm using maxN algorithm with alpha beta pruning
def iterativeDeepening(mySnake, enemySnakes, food, depth) -> Move:
    bestMove = Move.RIGHT
    startTime = time.time()
    alpha = -math.inf
    beta = math.inf
    for i in range(1, depth):
        if time.time() - startTime > 0.135:
            print("time exceeded", i)
            break
        bestMove = maxN(mySnake, enemySnakes, food, i, alpha, beta, i)
    print(time.time() - startTime)
    return bestMove

# maxN algorithm with alpha beta pruning
def maxN(mySnake, enemySnakes, food, depth, alpha, beta, returnDepth) -> Move:
    if depth == 0:
        return heuristic(mySnake, enemySnakes, food)
    bestValue = -math.inf
    bestMove = None
    for move in mySnake.getMoves():
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
    if depth == returnDepth:
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
    if mySnake.head.x < 0 or mySnake.head.x == 11 or mySnake.head.y < 0 or mySnake.head.y == 11:
        return -math.inf
    myHead = mySnake.head
    myDistance = 0
    
    for enemySnake in enemySnakes:
        # check if snake hit enemy body
        if mySnake.head in enemySnake.body:
            return -math.inf
        myDistance -= myHead.distance(enemySnake.head)
    
    return myDistance
    
