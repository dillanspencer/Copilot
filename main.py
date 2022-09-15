import typing
from utils.utils import Move

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
    print(game_state)

def end(game_state: typing.Dict):
    print("Ending game...")
    print(game_state)

def move(game_state: typing.Dict):
    
    
    return Move.UP




if __name__ == '__main__':
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})