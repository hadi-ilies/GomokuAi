import sys
from ai import Ai

def start(args: list, player: Ai):
    if int(args[0]) <= 0:
        raise ValueError("Invalid size")
    player.setBoard(int(args[0]))
    player.send("OK")

def info(args: list, player: Ai):
    return

def begin(args: list, player: Ai):
    player.play()

def turn(args: list, player: Ai):
    return

def board(args: list, player: Ai):
    return

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