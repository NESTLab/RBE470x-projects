# This is necessary to find the main code
import sys
from utility import *

sys.path.insert(0, '../bomberman')
from sys import maxsize

reccursionDepth = 2


def getNextMove_MiniMax(wrld):
    # Get the next move using minimax
    possibleMoves = eight_neighbors(wrld, character_location(wrld)[0], character_location(wrld)[1])
    possibleMoves.append(character_location(wrld))
    # Get the value of each possible move
    values = list(map(lambda move: getValue_of_State(wrld, move, 0), possibleMoves))
    # Get the max value
    maxValue = max(values)
    # Get the index of the max value
    maxIndex = values.index(maxValue)
    # Return the location to move to
    return possibleMoves[maxIndex]


def getValue_of_State(wrld, pos, depth):
    # Base case, depth has reached limit
    if depth == reccursionDepth:
        return evaluateState(wrld, pos)
    # If depth is even, then it is a min node
    possibleMoves = eight_neighbors(wrld, pos[0], pos[1])
    possibleMoves.append(pos)
    return max(map(lambda move: getValue_of_State(wrld, move, depth + 1), possibleMoves))
    # if depth % 2 == 0:
    #     # Find the smallest value of the possible moves using map reduce
    #     return min(map(lambda move: getValue_of_State(wrld, move, depth + 1), possibleMoves))
    # else:
    #     # Find the largest value of the possible moves using map reduce
    #     return max(map(lambda move: getValue_of_State(wrld, move, depth + 1), possibleMoves))


def evaluateState(wrld, pos):
    # Calculate the value of the state based on the distance to the exit and proximity to monsters
    # The closer to the exit, the better, the closer to monsters, the worse
    exitDist = a_star_distance_to_exit(wrld, start=pos)
    mosnterDist = euclidean_distance_to_monster(wrld, start=pos)
    print("Pos: " + str(pos))
    print("Exit Dist: " + str(exitDist))
    print("Monster Dist: " + str(mosnterDist))
    print("Value: " + str((mosnterDist * 0.7) - exitDist))
    if exitDist is 0:
        return maxsize
    return (mosnterDist * 0.7) - exitDist
