# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
from sys import maxsize

sys.path.insert(1, '../')
from utility import *

reccursionDepth = 3


def getNextMove_MiniMax(wrld, alpha=-float("inf"), beta=float("inf")):
    # Get the next move using minimax with alpha-beta pruning
    possibleMoves = eight_neighbors(wrld, character_location(wrld)[0], character_location(wrld)[1])
    possibleMoves.append(character_location(wrld))
    values = []
    for move in possibleMoves:
        value = getValue_of_State(wrld, move, monster_location(wrld), 0, alpha, beta)
        values.append(value)
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return possibleMoves[values.index(max(values))]


def getValue_of_State(wrld, self_pos, monster_pos, depth, alpha, beta):
    if self_pos == wrld.exitcell:
        return 1000 - depth

    if self_pos in eight_neighbors(wrld, monster_pos[0], monster_pos[1]) or self_pos == monster_pos:
        return -1000 - depth

    if depth == reccursionDepth:
        return evaluate_state(wrld, self_pos, monster_pos) - depth

    if depth % 2 == 1:  # Max Node (self)
        value = -float("inf")
        possible_moves = eight_neighbors(wrld, self_pos[0], self_pos[1])
        possible_moves.append(self_pos)
        for self_move in possible_moves:
            value = max(value, getValue_of_State(wrld, self_move, monster_pos, depth + 1, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:  # Min Node (monster)
        value = float("inf")
        possible_moves = eight_neighbors(wrld, monster_pos[0], monster_pos[1])
        possible_moves.append(monster_pos)
        for monster_move in possible_moves:
            value = min(value, getValue_of_State(wrld, self_pos, monster_move, depth + 1, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value
