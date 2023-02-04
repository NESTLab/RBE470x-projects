# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
from sys import maxsize

sys.path.insert(1, '../')
from utility import *

reccursionDepth = 2


def getNextMove_MiniMax(wrld):
    # Get the next move using minimax
    possibleMoves = eight_neighbors(wrld, character_location(wrld)[0], character_location(wrld)[1])
    possibleMoves.append(character_location(wrld))
    print("get next move called! self move options: ", possibleMoves)
    values = list(map(lambda move: getValue_of_State(wrld, move, monster_location(wrld), 0), possibleMoves))
    print("Options Evaluated: ", possibleMoves)
    print("Option Scores: ", values)
    return possibleMoves[values.index(max(values))]


def getValue_of_State(wrld, self_pos, monster_pos, depth):
    # Base case, depth has reached limit
    if depth == reccursionDepth:
        sys.stdout.write("\t" * depth)
        print("base case! (Rec-depth) self pos: ", self_pos, "monster pos: ", monster_pos, "depth: ", depth, "score: ",
              evaluate_state(wrld, self_pos, monster_pos))
        return evaluate_state(wrld, self_pos, monster_pos)

    if self_pos in eight_neighbors(wrld, monster_pos[0], monster_pos[1]):
        sys.stdout.write("\t" * depth)
        print("base case! (Monster) self pos: ", self_pos, "monster pos: ", monster_pos, "depth: ", depth, "score: ",
              -maxsize / 2)
        return -maxsize / 2

    if self_pos == wrld.exitcell:
        sys.stdout.write("\t" * depth)
        print("base case! (Exit) self pos: ", self_pos, "monster pos: ", monster_pos, "depth: ", depth, "score: ",
              maxsize / 2)
        return maxsize / 2
    # If depth is even, then it is a min node
    if depth % 2 == 1:  # Max Node (self)
        possible_moves = eight_neighbors(wrld, self_pos[0], self_pos[1])
        possible_moves.append(self_pos)
        sys.stdout.write("\t" * depth)
        print("max node called! self pos: ", self_pos, "monster pos: ", monster_pos, "depth: ", depth)
        sys.stdout.write("\t" * depth)
        print("max node called! self move options: ", possible_moves)
        return max(map(lambda self_move: getValue_of_State(wrld, self_move, monster_pos, depth + 1), possible_moves))
    else:  # Min Node (monster)
        possible_moves = eight_neighbors(wrld, monster_pos[0], monster_pos[1])
        possible_moves.append(monster_pos)
        sys.stdout.write("\t" * depth)
        print("min node called! self pos: ", self_pos, "monster pos: ", monster_pos, "depth: ", depth)
        sys.stdout.write("\t" * depth)
        print("min node called! monster move options: ", possible_moves)
        return min(map(lambda monster_move: getValue_of_State(wrld, self_pos, monster_move, depth + 1), possible_moves))
