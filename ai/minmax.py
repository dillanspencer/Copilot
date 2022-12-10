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
    for i in range(1, depth):
        if time.time() - startTime > 0.275:
            return bestMove
        bestMove = maxN(board, mySnake, enemySnakes, food, i, i,-math.inf, math.inf, startTime)
    return bestMove

# maxN algorithm with alpha beta pruning
def maxN(board, mySnake, enemySnakes, food, depth, maxDepth, alpha, beta, returnTime) -> Move:

    if depth == 0 or time.perf_counter() - returnTime > 0.175:
        heuristicValue = heuristic(mySnake, enemySnakes)
        return heuristicValue

    bestValue = -math.inf
    bestMove = None
    for move in mySnake.getMoves(enemySnakes):
        newMySnake = copy.deepcopy(mySnake)
        newMySnake.move(move)
        newEnemySnakes = copy.deepcopy(enemySnakes)
        newBoard = copy.deepcopy(board)
        newBoard.updateBoard(mySnake, enemySnakes, food)
        value = minN(newBoard, newMySnake, newEnemySnakes, food, depth - 1, maxDepth, alpha, beta, returnTime)
        if value > bestValue:
            bestValue = value
            bestMove = move
        alpha = max(alpha, bestValue)
        if alpha >= beta:
            break

    if depth == maxDepth:
        return bestMove
    return bestValue

# minN algorithm with alpha beta pruning
def minN(board, mySnake, enemySnakes, food, depth, maxDepth, alpha, beta, returnTime):
    if depth == 0 or time.perf_counter() - returnTime > 0.175:
        return heuristic(mySnake, enemySnakes)
    bestValue = math.inf
    for enemySnake in enemySnakes:
        for move in enemySnake.getMoves():
            newMySnake = copy.deepcopy(mySnake)
            newEnemySnakes = copy.deepcopy(enemySnakes)
            for enemySnake in newEnemySnakes:
                enemySnake.move(move)
            newBoard = copy.deepcopy(board)
            newBoard.updateBoard(mySnake, enemySnakes, food)
            value = maxN(newBoard, newMySnake, newEnemySnakes, food, depth - 1, maxDepth, alpha, beta, returnTime)
            bestValue = min(bestValue, value)
            beta = min(beta, bestValue)
            if alpha >= beta:
                break

    return bestValue
         

# heuristic function for the minmax algorithm that takes account being close to the center and not moving out of bounds
def heuristic(mySnake, enemySnakes):
  # Create a list of all snakes, including the current player's snake and the enemy snakes
  snakes = [mySnake] + enemySnakes
  
  # Calculate the Voronoi diagram for the list of snakes
  voronoi = calculate_voronoi(snakes)
  
  # Initialize the value to 0
  value = 0
  
  # Iterate through the regions in the Voronoi diagram
  for region in voronoi:
    # If the region is associated with the current player's snake, add the size of the region to the value
    if region.snake == mySnake:
      value += region.size
    # If the region is associated with an enemy snake, subtract the size of the region from the value
    else:
      value -= region.size
  
  # Return the value
  return value


    