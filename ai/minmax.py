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
    bestMove = maxN(mySnake, enemySnakes, food, depth, alpha, beta, startTime)
    return bestMove

# maxN algorithm with alpha beta pruning
def maxN(mySnake, enemySnakes, food, depth, alpha, beta, returnTime) -> Move:
    if depth == 0 or time.time() - returnTime > 0.135:
        heuristicValue = heuristic(mySnake, enemySnakes, food)
        return heuristicValue
    bestValue = -math.inf
    bestMove = None
    for move in mySnake.getMoves(enemySnakes):
        newMySnake = copy.deepcopy(mySnake)
        newMySnake.move(move)
        newEnemySnakes = copy.deepcopy(enemySnakes)
        value = minN(newMySnake, newEnemySnakes, food, depth - 1, alpha, beta, returnTime)
        if value > bestValue:
            bestValue = value
            bestMove = move
        alpha = max(alpha, bestValue)
        if alpha >= beta:
            break
    if depth == 8:
        return bestMove
    return bestValue

# minN algorithm with alpha beta pruning
def minN(mySnake, enemySnakes, food, depth, alpha, beta, returnTime):
    if depth == 0:
        return heuristic(mySnake, enemySnakes, food)
    bestValue = math.inf
    for enemySnake in enemySnakes:
        for move in enemySnake.getMoves():
            newMySnake = copy.deepcopy(mySnake)
            newEnemySnakes = copy.deepcopy(enemySnakes)
            for enemySnake in newEnemySnakes:
                enemySnake.move(move)
            value = maxN(newMySnake, newEnemySnakes, food, depth - 1, alpha, beta, returnTime)
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
            if len(mySnake.body) > len(enemySnake.body):
                return math.inf
            else:
                return -math.inf

    foodDist = myHead.distance(food[0])
    for point in food:
        foodDist = min(foodDist, mySnake.head.distance(point))
        
    return -foodDist
    
