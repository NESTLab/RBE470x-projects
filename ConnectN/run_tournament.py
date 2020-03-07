#!/usr/bin/env python3

import multiprocessing
import os
import sys
from subprocess import call
from players import PLAYERS

def run_match(params):
    datadir = params[0]
    width   = params[1]
    height  = params[2]
    tokens  = params[3]
    limit   = params[4]
    p1      = params[5]
    p2      = params[6]
    call(["python3", "run_match.py", datadir, str(width), str(height), str(tokens), str(limit), p1, p2])

#
# Parse arguments
#
if not len(sys.argv) == 6:
    print("Usage:\n  {} <datadir> <board width> <board height> <tokens to win> <time limit>".format(sys.argv))
    sys.exit(1)

DATADIR      = sys.argv[1]
BOARD_WIDTH  = int(sys.argv[2])
BOARD_HEIGHT = int(sys.argv[3])
TOKENS       = int(sys.argv[4])
TIME_LIMIT   = int(sys.argv[5])

pool = multiprocessing.Pool()
matches = []
for p1 in PLAYERS.keys():
    for p2 in PLAYERS.keys():
        if p1 != p2:
            matches.append((p1,p2))

procs = pool.map(run_match, [(DATADIR, BOARD_WIDTH, BOARD_HEIGHT, TOKENS, TIME_LIMIT, m[0], m[1]) for m in matches])
