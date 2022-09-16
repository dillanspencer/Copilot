import random
import copy
import math
from utils.snake import Snake
from utils.utils import Move

# iterative deepening algorithm using monte carlo tree search
def iterativeDeepening(snake: Snake, enemySnakes, food, depth):
    bestMove = None
    for i in range(1, depth):
        bestMove = monteCarloTreeSearch(snake, enemySnakes, food, i)
    return bestMove

# monte carlo tree search algorithm
def monteCarloTreeSearch(snake: Snake, enemySnakes, food, depth):
    root = Node(snake, enemySnakes, food, None)
    for i in range(0, depth):
        node = treePolicy(root)
        reward = defaultPolicy(node.snake, node.enemySnakes, node.food)
        backup(node, reward)
    return bestChild(root, 0).move

# tree policy algorithm
def treePolicy(node):
    while node.untriedMoves == [] and node.children != []:
        node = bestChild(node, 2)
    if node.untriedMoves != []:
        m = random.choice(node.untriedMoves)
        node = node.addChild(m, node.snake, node.enemySnakes, node.food)
    return node

# default policy algorithm
def defaultPolicy(snake: Snake, enemySnakes, food):
    reward = 0
    while snake.alive:
        moves = snake.getMoves()
        move = random.choice(moves)
        snake.move(move)
        for enemy in enemySnakes:
            if snake.head == enemy.head:
                snake.die()
                break
        if snake.head in food:
            snake.eat()
            reward += 1
    return reward
        

# backup algorithm
def backup(node, reward):
    while node != None:
        node.visits += 1
        node.reward += reward
        node = node.parent

# best child algorithm
def bestChild(node, explorationValue):
    bestScore = 0
    bestNodes = []
    for child in node.children:
        exploit = child.reward / child.visits
        explore = math.sqrt((2 * math.log(node.visits)) / child.visits)
        score = exploit + explorationValue * explore
        if score == bestScore:
            bestNodes.append(child)
        if score > bestScore:
            bestScore = score
            bestNodes = [child]
    return random.choice(bestNodes)

# node class
class Node():
    def __init__(self, snake: Snake, enemySnakes, food, parent):
        self.parent = parent
        self.children = []
        self.untriedMoves = snake.getMoves()
        self.move = None
        self.snake = snake
        self.enemySnakes = enemySnakes
        self.food = food
        self.visits = 0
        self.reward = 0

    def addChild(self, move, snake, enemySnakes, food):
        newSnake = copy.deepcopy(snake)
        newSnake.move(move)
        newEnemySnakes = copy.deepcopy(enemySnakes)
        for enemy in newEnemySnakes:
            enemy.move(enemy.die())
        newNode = Node(newSnake, newEnemySnakes, food, self)
        newNode.move = move
        self.untriedMoves.remove(move)
        self.children.append(newNode)
        return newNode





