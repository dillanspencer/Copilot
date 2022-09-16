import typing
from models.board import Board
from utils.utils import Move, Point
from utils.snake import Snake
from ai.minmax import *

def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Dillan Spencer",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }

def start(game_state: typing.Dict):
    print("Starting game...")

def end(game_state: typing.Dict):
    print("Ending game...")

def move(game_state: typing.Dict):
    mySnake = Snake(game_state["you"]["id"], game_state["you"]["body"])
    enemySnakes = [Snake(snake["id"], snake["body"]) for snake in game_state["board"]["snakes"] if snake["id"] != game_state["you"]["id"]]
    food = [Point(game_state["board"]["food"][i]["x"], game_state["board"]["food"][i]["y"]) for i in range(len(game_state["board"]["food"]))]

    # board = Board(11, 11, enemySnakes, food, mySnake)
    move = iterativeDeepening(mySnake, enemySnakes=enemySnakes, food=food, depth=6)

    return {"move": move.value}


if __name__ == '__main__':
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})