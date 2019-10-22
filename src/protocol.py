import sys
from ai import Ai

def start(args: list, player: Ai):
    if int(args[0]) <= 0:
        raise ValueError("Invalid size")
    player.setBoard(int(args[0]))
    player.send("OK")

def info(args: list, player: Ai):
    #print(args)
    return None

def begin(args: list, player: Ai):
    player.firstPlay()

def turn(args: list, player: Ai):
    #print(args)
    coord = args[0].split(",")
    x = int(coord[0])
    y = int(coord[1])
    player.getBoard().set(x, y, 2) ## enemy's stone
    player.play(x, y)

def board(args: list, player: Ai):
    #print(args)
    command = player.recv()
    while command[0] is not "DONE":
        infos = command[0].split(",")
        if len(infos) >= 3:
            player.getBoard().set(int(infos[0]), int(infos[1]), int(infos[2])) ## check args
        command = player.recv()
    player.play(-1, -1)

def end(args: list, player: Ai):
    sys.exit(0)

def about(args: list, player: Ai):
    player.send("name=\"Hadi Bereksi\", version=\"0.8\", author=\"Hadi Bereksi\", country=\"DZ/FR\"")

protocolDir = {
    "START": start,
    "TURN": turn,
    "BEGIN": begin,
    "BOARD": board,
    "INFO": info,
    "END": end,
    "ABOUT": about
}