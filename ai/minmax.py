import random
import copy
import math
import time
from utils.snake import Snake
from utils.utils import Move, Point, Entry


# iterative deepening algorithm using maxN algorithm with alpha beta pruning
def iterativeDeepening(board, mySnake, enemySnakes, food, depth) -> Move:
    bestMove = None
    startTime = time.time()
    transpositionTable = {}
    for i in range(1, depth):
        if time.time() - startTime > 0.275:
            break
        bestMove = maxN(board, mySnake, enemySnakes, food, i, -math.inf, math.inf, transpositionTable, startTime)
    return bestMove

# maxN algorithm with alpha beta pruning
def maxN(board, mySnake, enemySnakes, food, depth, alpha, beta, transpositionTable, returnTime) -> Move:
    alphaOrig = alpha
    boardHash = hash(board)
    ttEntry = transpositionLookup(transpositionTable, boardHash)
    if ttEntry is not None and ttEntry["depth"] >= depth:
        if ttEntry["flag"] == Entry.EXACT:
            return ttEntry["move"]
        if ttEntry["flag"] == Entry.LOWERBOUND:
            alpha = max(alpha, ttEntry.value)
        if ttEntry["flag"] == Entry.UPPERBOUND:
            beta = min(beta, ttEntry.value)
        if alpha >= beta:
            return ttEntry["move"]

    if depth == 0 or time.time() - returnTime > 0.350:
        return mySnake.getMoves(enemySnakes)[0]

    bestMove = None
    for move in mySnake.getMoves(enemySnakes):
        newMySnake = copy.deepcopy(mySnake)
        newMySnake.move(move)
        newEnemySnakes = copy.deepcopy(enemySnakes)
        newBoard = copy.deepcopy(board)
        newBoard.updateBoard(mySnake, enemySnakes, food)
        value = minN(newBoard, newMySnake, newEnemySnakes, food, depth - 1, alpha, beta, transpositionTable, returnTime)
        if value > bestMove:
            bestMove = value
        alpha = max(alpha, bestMove)
        if alpha >= beta:
            break

        # transposition
        ttEntry = {}
        ttEntry["value"] = bestMove
        ttEntry["move"] = bestMove
        if bestMove <= alphaOrig:
            ttEntry["flag"] = Entry.UPPERBOUND
        if bestMove >= beta:
            ttEntry["flag"] = Entry.LOWERBOUND
        else:
            ttEntry["flag"] = Entry.EXACT
            ttEntry["depth"] = depth
            transpositionTable[boardHash] = ttEntry

    return bestMove

# minN algorithm with alpha beta pruning
def minN(board, mySnake, enemySnakes, food, depth, alpha, beta, transpositionTable, returnTime) -> Move:
    betaOrig = beta
    boardHash = hash(board)
    ttEntry = transpositionLookup(transpositionTable, boardHash)
    if ttEntry is not None and ttEntry["depth"] >= depth:
        if ttEntry["flag"] == Entry.EXACT:
            return ttEntry["value"]
        if ttEntry["flag"] == Entry.LOWERBOUND:
            alpha = max(alpha, ttEntry.value)
        if ttEntry["flag"] == Entry.UPPERBOUND:
            beta = min(beta, ttEntry.value)
        if alpha >= beta:
            return ttEntry["value"]
    if depth == 0 or time.time() - returnTime > 0.350:
        return mySnake.getMoves(enemySnakes)[0]

    bestMove = None
    for enemySnake in enemySnakes:
        for move in enemySnake.getMoves():
            newMySnake = copy.deepcopy(mySnake)
            newMySnake.move(move)
            newEnemySnakes = copy.deepcopy(enemySnakes)
            newBoard = copy.deepcopy(board)
            newBoard.updateBoard(mySnake, enemySnakes, food)
            value = maxN(newBoard, newMySnake, newEnemySnakes, food, depth - 1, alpha, beta, transpositionTable, returnTime)
            if value < bestMove:
                bestMove = value
            beta = min(beta, bestMove)
            if alpha >= beta:
                break

    # transposition
    ttEntry = {}
    ttEntry["value"] = bestMove
    if bestMove <= alpha:
        ttEntry["flag"] = Entry.UPPERBOUND
    if bestMove >= betaOrig:
        ttEntry["flag"] = Entry.LOWERBOUND
    else:
        ttEntry["flag"] = Entry.EXACT
        ttEntry["depth"] = depth
        transpositionTable[boardHash] = ttEntry

    return bestMove

         

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



def transpositionLookup(transpositionTable, key):
    try:
        val = transpositionTable[key]
        return val
    except:
        return None
    
