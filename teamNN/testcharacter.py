# This is necessary to find the main code
import sys
from enum import Enum

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from PriorityQueue import PriorityQueue

sys.path.insert(1, '../teamNN')
from utility import *
from project1.minimax import getNextMove_MiniMax


class State(Enum):
    START = 1
    MOVE_TO_EXIT = 2
    RUN_FROM_MONSTER = 3
    MOVE_TO_WALL = 4
    PLACE_BOMB = 5
    RUN_FROM_BOMB = 6
    DONE = 7


class TestCharacter(CharacterEntity):
    stateMachine = State.START

    def do(self, wrld):
        # match self.stateMachine:
        #     case State.START:
        #         self.stateMachine = State.MOVE_TO_EXIT
        #     case State.MOVE_TO_EXIT:
        #         self.move_to_exit(wrld)
        #     case State.RUN_FROM_MONSTER:
        #         self.run_from_monster(wrld)
        #     case State.MOVE_TO_WALL:
        #         self.move_to_wall(wrld)
        #     case State.PLACE_BOMB:
        #         self.place_bomb(wrld)
        #     case State.RUN_FROM_BOMB:
        #         self.run_from_bomb(wrld)
        #     case State.DONE:
        #         return

        # print(getNextMove_MiniMax(wrld))
        print("Score of current world", evaluate_state(wrld, character_location(wrld), monster_location(wrld)))
        nextCell = getNextMove_MiniMax(wrld)
        print("Selected Move: ", nextCell)

        self.move(nextCell[0] - self.x, nextCell[1] - self.y)

        # if self.firstTime:
