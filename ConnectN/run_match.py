#!/usr/bin/env python3

import sys
from pathlib import Path

import game
from players import PLAYERS

#
# Parse arguments
#
if not len(sys.argv) in [8,9]:
    print("Usage:\n  {} <datadir> <board width> <board height> <tokens to win> <time limit> <player1> <player2> [replay]".format(sys.argv))
    sys.exit(1)

DATADIR      = sys.argv[1]
BOARD_WIDTH  = int(sys.argv[2])
BOARD_HEIGHT = int(sys.argv[3])
TOKENS       = int(sys.argv[4])
TIME_LIMIT   = int(sys.argv[5])
PLAYER1      = sys.argv[6]
PLAYER2      = sys.argv[7]
REPLAY       = (len(sys.argv) == 9 and sys.argv[8] == "replay")

#
# Make file name and check if it exists
#
FILE_PATH = "{}/{}_{}_{}_{}_{}.dat".format(DATADIR, BOARD_WIDTH, BOARD_HEIGHT, TOKENS, PLAYER1, PLAYER2)
if(Path(FILE_PATH).exists() and (not REPLAY)):
    print(FILE_PATH, "skipped")
    sys.exit(0)
print(FILE_PATH, "started")

#
# Time to play!
#
g = game.Game(BOARD_WIDTH,      # width
              BOARD_HEIGHT,     # height
              TOKENS,           # tokens in a row to win
              PLAYERS[PLAYER1], # player 1
              PLAYERS[PLAYER2]) # player 2
g.logged_go(FILE_PATH, TIME_LIMIT)
print(FILE_PATH, "done")
