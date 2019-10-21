import sys
from game import Game

def main():
    game = Game()
    while True:
        try:
            game.run(sys.stdin.readline().replace("\r", "").replace("\n", "").split(" "))
        except Exception as error:
            game.getDebugger().error(str(error))


if __name__ == "__main__":
    main()