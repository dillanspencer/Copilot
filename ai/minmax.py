import random
import copy
import math
import time
from utils.snake import Snake
from utils.utils import Move

# iterative deepening algorithm using maxN algorithm with alpha beta pruning
def iterativeDeepening(mySnake, enemySnakes, food, depth):
    bestMove = Move.UP
    startTime = time.time()
    for i in range(1, depth):
        if time.time() - startTime > 0.350:
            return bestMove
        bestMove = maxN(mySnake, enemySnakes, food, i, -math.inf, math.inf)
    return bestMove

# maxN algorithm with alpha beta pruning
def maxN(mySnake, enemySnakes, food, depth, alpha, beta):
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
        value = minN(newMySnake, newEnemySnakes, food, depth - 1, alpha, beta)
        if value > bestValue:
            bestValue = value
            bestMove = move
        alpha = max(alpha, bestValue)
        if alpha >= beta:
            break
    if depth == 4:
        return bestMove
    return bestValue

# minN algorithm with alpha beta pruning
def minN(mySnake, enemySnakes, food, depth, alpha, beta):
    if depth == 0:
        return heuristic(mySnake, enemySnakes, food)
    bestValue = math.inf
    for enemySnake in enemySnakes:
        for move in enemySnake.getMoves():
            newMySnake = copy.deepcopy(mySnake)
            newEnemySnakes = copy.deepcopy(enemySnakes)
            for enemySnake in newEnemySnakes:
                enemySnake.move(move)
            value = maxN(newMySnake, newEnemySnakes, food, depth - 1, alpha, beta)
            bestValue = min(bestValue, value)
            beta = min(beta, bestValue)
            if alpha >= beta:
                break
    return bestValue
         

# heuristic function that takes into account control of the board, distance to enemy snakes and being closer to food than enemy snakes
def heuristic(mySnake, enemySnakes, food):
    mySnakeDistance = 0
    enemySnakeDistance = 0
    for enemySnake in enemySnakes:
        mySnakeDistance += mySnake.head.distance(enemySnake.head)
    foodDistance = 0
    for foodPoint in food:
        foodDistance += mySnake.head.distance(foodPoint)
        enemySnakeDistance += enemySnake.head.distance(foodPoint)
    return mySnakeDistance - enemySnakeDistance + foodDistance
