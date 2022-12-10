from scipy.spatial import Voronoi
import copy
import math
import time
from utils.snake import Snake
from utils.utils import Move
import numpy as np


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


def calculate_voronoi(snakes):
  # Create an empty list to store the regions
  regions = []
  
  # Create a list of the positions of all snakes
  points_array = np.concatenate([np.array([p.getPoint3D() for p in snake.body]) for snake in snakes])
  
  # Create the Voronoi diagram using the scipy.spatial.Voronoi class
  voronoi = Voronoi(points_array)
  
  # Iterate through the regions in the Voronoi diagram
  for region in voronoi.regions:
    # Skip empty regions
    if region == []:
      continue
      
    # Calculate the size of the region
    size = calculate_region_size(region, voronoi.vertices)
    
    # Find the snake associated with the region by finding the closest snake to the centroid of the region
    snake = find_closest_snake(region, voronoi.points, snakes)
    
    # Create a Region object for the region and append it to the list of regions
    regions.append(Region(snake, size))
  
  # Return the list of regions
  return regions


def calculate_region_size(region, vertices):
  # Initialize the size to 0
  size = 0
  
  # Iterate through the vertices in the region
  for i in range(len(region) - 1):
    # Get the coordinates of the current vertex and the next vertex
    x1, y1 = vertices[region[i]]
    x2, y2 = vertices[region[i + 1]]
    
    # Add the distance between the vertices to the size
    size += ((x1 - x2)**2 + (y1 - y2)**2)**0.5
  
  # Return the size
  return size

def find_closest_snake(region, points, snakes):
  # Initialize the minimum distance to infinity
  min_distance = float("inf")
  
  # Initialize the closest snake to None
  closest_snake = None
  
  # Calculate the centroid of the region
  centroid = calculate_centroid(region, points)
  
  # Iterate through the snakes
  for snake in snakes:
    snake_points = np.array([p.getPoint() for p in snake.body])
    # Calculate the distance between the snake and the centroid
    distance = np.sqrt(np.sum((snake_points - centroid)**2, axis=1))
    
    # Update the minimum distance and closest snake if the current snake is closer
    if distance.any() < min_distance:
      min_distance = distance.any()
      closest_snake = snake
  
  # Return the closest snake
  return closest_snake


def calculate_centroid(region, points):
  # Initialize the x and y coordinates to 0
  x = 0
  y = 0
  
  # Iterate through the vertices in the region
  for vertex in region:
    # Add the x and y coordinates of the vertex to the x and y coordinates
    x += points[vertex][0]
    y += points[vertex][1]
  
  # Calculate the average x and y coordinates
  x /= len(region)
  y /= len(region)
  
  # Return the centroid as a tuple (x, y)
  return (x, y)


class Region:
  def __init__(self, snake, size):
    self.snake = snake
    self.size = size