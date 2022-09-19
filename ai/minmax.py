import random
import copy
import math
import time
from utils.snake import Snake
from utils.utils import Move, Point, Entry


# iterative deepening algorithm using maxN algorithm with alpha beta pruning
def iterativeDeepening(board, mySnake, enemySnakes, food, depth) -> Move:
    bestMove = Move.RIGHT
    startTime = time.time()
    transpositionTable = {}
    for i in range(1, depth):
        if time.time() - startTime > 0.150:
            return bestMove
        bestMove = maxN(board, mySnake, enemySnakes, food, i, i,-math.inf, math.inf, transpositionTable, startTime)
    return bestMove

# maxN algorithm with alpha beta pruning
def maxN(board, mySnake, enemySnakes, food, depth, maxDepth, alpha, beta, transpositionTable, returnTime) -> Move:
    if depth == 0 or time.time() - returnTime > 0.150:
        heuristicValue = heuristic(mySnake, enemySnakes, food)
        return heuristicValue

    alphaOrig = alpha
    boardHash = hash(board)
    ttEntry = transpositionLookup(transpositionTable, boardHash)
    if ttEntry is not None:
        if ttEntry["flag"] == Entry.EXACT:
            return ttEntry["value"]
        if ttEntry["flag"] == Entry.LOWERBOUND:
            alpha = max(alpha, ttEntry.value)
        if ttEntry["flag"] == Entry.UPPERBOUND:
            beta = min(beta, ttEntry.value)
        if alpha >= beta:
            return ttEntry["value"]

    bestValue = -math.inf
    bestMove = None
    for move in mySnake.getMoves(enemySnakes):
        newMySnake = copy.deepcopy(mySnake)
        newMySnake.move(move)
        newEnemySnakes = copy.deepcopy(enemySnakes)
        newBoard = copy.deepcopy(board)
        newBoard.updateBoard(mySnake, enemySnakes, food)
        value = minN(newBoard, newMySnake, newEnemySnakes, food, depth - 1, maxDepth, alpha, beta, transpositionTable, returnTime)
        if value > bestValue:
            bestValue = value
            bestMove = move
        alpha = max(alpha, bestValue)
        if alpha >= beta:
            break

        # transposition
        ttEntry = {}
        ttEntry["value"] = bestValue
        if bestValue <= alphaOrig:
            ttEntry["flag"] = Entry.UPPERBOUND
        if bestValue >= beta:
            ttEntry["flag"] = Entry.LOWERBOUND
        else:
            ttEntry["flag"] = Entry.EXACT

        transpositionTable[boardHash] = ttEntry

    if depth == maxDepth:
        return bestMove
    return bestValue

# minN algorithm with alpha beta pruning
def minN(board, mySnake, enemySnakes, food, depth, maxDepth, alpha, beta, transpositionTable, returnTime):
    if depth == 0:
        return heuristic(mySnake, enemySnakes, food)
    bestValue = math.inf
    for enemySnake in enemySnakes:
        for move in enemySnake.getMoves():
            newMySnake = copy.deepcopy(mySnake)
            newEnemySnakes = copy.deepcopy(enemySnakes)
            for enemySnake in newEnemySnakes:
                enemySnake.move(move)
            newBoard = copy.deepcopy(board)
            newBoard.updateBoard(mySnake, enemySnakes, food)
            value = maxN(board, newMySnake, newEnemySnakes, food, depth - 1, maxDepth, alpha, beta, transpositionTable, returnTime)
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



def transpositionLookup(transpositionTable, key):
    try:
        val = transpositionTable[key]
        return val
    except:
        return None
    
