import random
import copy
import math
from utils.snake import Snake
from utils.utils import Move

# iterative deepening algorithm using maxN algorithm with alpha beta pruning
def iterativeDeepening(mySnake, enemySnakes, food, depth):
    bestMove = None
    for i in range(1, depth):
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
            print(enemySnake.getMoves())
            enemySnake.move(random.choice(enemySnake.getMoves()))
        value = minN(newMySnake, newEnemySnakes, food, depth - 1, alpha, beta)
        if value > bestValue:
            bestValue = value
            bestMove = move
        alpha = max(alpha, bestValue)
        if alpha >= beta:
            break
    if depth == 10:
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
         

# heuristic function that takes into account the distance to the closest food, the distance to the closest enemy, and the length of the snake
def heuristic(mySnake, enemySnakes, food):
    closestFood = min([mySnake.head.distance(foodPoint) for foodPoint in food])
    closestEnemy = min([mySnake.head.distance(enemySnake.head) for enemySnake in enemySnakes])
    return 1 / closestFood + 1 / closestEnemy + 1 + mySnake.length
