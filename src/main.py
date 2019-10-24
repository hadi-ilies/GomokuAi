import sys
from game import Game
from debug import Debugger

def main():
    game = Game()
    while True:
        try:
            game.run(input().replace("\r", "").replace("\n", "").split(" "))
        except Exception as error:
            Debugger.error(str(error))


if __name__ == "__main__":
    main()