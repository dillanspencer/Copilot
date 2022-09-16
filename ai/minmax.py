import random
import copy
import math
import time
from utils.snake import Snake
from utils.utils import Move

# iterative deepening algorithm using maxN algorithm with alpha beta pruning
def iterativeDeepening(mySnake, enemySnakes, food, depth) -> Move:
    bestMove = Move.UP
    startTime = time.time()
    for i in range(1, depth):
        if time.time() - startTime > 0.350:
            print("time exceeded", i)
            return bestMove
        bestMove = maxN(mySnake, enemySnakes, food, i, -math.inf, math.inf, i)
    return bestMove

# maxN algorithm with alpha beta pruning
def maxN(mySnake, enemySnakes, food, depth, alpha, beta, returnDepth) -> Move:
    if depth == 0:
        return heuristic(mySnake, enemySnakes, food)
    bestValue = -math.inf
    bestMove = Move.UP
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
    mySnakeHead = mySnake.head
    mySnakeBody = mySnake.body
    mySnakeLength = len(mySnakeBody)
    mySnakeMoves = mySnake.getMoves()
    mySnakeMovesLength = len(mySnakeMoves)
    mySnakeMovesLength = 1 if mySnakeMovesLength == 0 else mySnakeMovesLength
    enemySnakeLength = 0
    enemySnakeMovesLength = 0
    for enemySnake in enemySnakes:
        enemySnakeLength += len(enemySnake.body)
        enemySnakeMovesLength += len(enemySnake.getMoves())
    enemySnakeMovesLength = 1 if enemySnakeMovesLength == 0 else enemySnakeMovesLength
    foodLength = len(food)
    foodLength = 1 if foodLength == 0 else foodLength
    return (mySnakeLength - enemySnakeLength) / (mySnakeMovesLength - enemySnakeMovesLength) + (mySnakeLength - foodLength) / (mySnakeMovesLength - foodLength) + (mySnakeHead.x - 5) ** 2 + (mySnakeHead.y - 5) ** 2
    
