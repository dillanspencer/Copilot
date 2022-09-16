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
        return None
    bestMove = None
    for move in mySnake.getMoves():
        mySnakeCopy = copy.deepcopy(mySnake)
        mySnakeCopy.move(move)
        if mySnakeCopy.head in food:
            mySnakeCopy.eat()
        if mySnakeCopy.head in [snake.head for snake in enemySnakes]:
            return move
        value = minN(mySnakeCopy, enemySnakes, food, depth - 1, alpha, beta)
        if value > alpha:
            alpha = value
            bestMove = move
        if alpha >= beta:
            break
    return bestMove

# minN algorithm with alpha beta pruning
def minN(mySnake, enemySnakes, food, depth, alpha, beta):
    if depth == 0:
        return None
    bestMove = None
    for move in mySnake.getMoves():
        mySnakeCopy = copy.deepcopy(mySnake)
        mySnakeCopy.move(move)
        if mySnakeCopy.head in food:
            mySnakeCopy.eat()
        if mySnakeCopy.head in [snake.head for snake in enemySnakes]:
            return move
        value = maxN(mySnakeCopy, enemySnakes, food, depth - 1, alpha, beta)
        if value < beta:
            beta = value
            bestMove = move
        if alpha >= beta:
            break
    return bestMove
