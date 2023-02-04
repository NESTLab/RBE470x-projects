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
from project1.minimax import *


class State(Enum):
    START = 1
    PLACE_BOMB = 2
    PLACE_BOMB_R = 3
    WAIT_FOR_BOMB = 4
    FAR_FROM_MONSTER = 5
    CLOSE_TO_MONSTER = 6


class TestCharacter(CharacterEntity):
    waitCount = 0
    bombCount = 0
    bombLimit = 5
    bombCoolDown = 0
    stateMachine = State.START
    ai = AI()

    def do(self, wrld):
        print("Current State: ", self.stateMachine)
        self.bombCoolDown -= 1
        match self.stateMachine:
            case State.START:
                self.move(0, 1)
                if self.x == 0 and self.y == 2:
                    self.stateMachine = State.PLACE_BOMB
            case State.PLACE_BOMB:
                self.place_bomb()
                self.move(1, -1)
                self.waitCount = 0
                self.stateMachine = State.WAIT_FOR_BOMB
            case State.PLACE_BOMB_R:
                self.place_bomb()
                self.move(-1, -1)
                self.waitCount = 0
                self.stateMachine = State.WAIT_FOR_BOMB
            case State.WAIT_FOR_BOMB:
                self.move(0, 0)
                self.waitCount += 1
                if self.waitCount > 2:
                    self.bombCount += 1
                    self.bombCoolDown = 7
                    self.stateMachine = State.FAR_FROM_MONSTER
            case State.FAR_FROM_MONSTER:
                self.ai.reccursionDepth = 2
                self.ai.isExpectimax = False
                nextCell = self.ai.get_next_move(wrld)
                self.move(nextCell[0] - self.x, nextCell[1] - self.y)
                print("Score of current world", evaluate_state(wrld, character_location(wrld), monster_location(wrld)))
                print("Selected Move: ", nextCell)
                if self.bombCount < self.bombLimit and self.bombCoolDown <= 0 and self.valid_bomb_location(
                        (nextCell[0], nextCell[1]), True):
                    self.stateMachine = State.PLACE_BOMB_R
                if self.bombCount < self.bombLimit and self.bombCoolDown <= 0 and self.valid_bomb_location(
                        (nextCell[0], nextCell[1]), False):
                    self.stateMachine = State.PLACE_BOMB
                if euclidean_distance_to_monster(wrld, (nextCell[0], nextCell[1])) < 7:
                    self.stateMachine = State.CLOSE_TO_MONSTER
            case State.CLOSE_TO_MONSTER:
                self.ai.reccursionDepth = 3
                self.ai.isExpectimax = True
                if len(wrld.monsters.values()) > 1:
                    self.ai.isExpectimax = False
                nextCell = self.ai.get_next_move(wrld)
                self.move(nextCell[0] - self.x, nextCell[1] - self.y)
                print("Score of current world", evaluate_state(wrld, character_location(wrld), monster_location(wrld)))
                print("Selected Move: ", nextCell)
                if self.bombCount < self.bombLimit and self.bombCoolDown <= 0 and self.valid_bomb_location(
                        (nextCell[0], nextCell[1]), True):
                    self.stateMachine = State.PLACE_BOMB_R
                if self.bombCount < self.bombLimit and self.bombCoolDown <= 0 and self.valid_bomb_location(
                        (nextCell[0], nextCell[1]), False):
                    self.stateMachine = State.PLACE_BOMB
                if euclidean_distance_to_monster(wrld, (nextCell[0], nextCell[1])) > 10:
                    self.stateMachine = State.FAR_FROM_MONSTER

    def valid_bomb_location(self, location, isRight):
        if isRight:
            return (location[0] == 7 or location[0] == 6) and (location[1] == 6 or location[1] == 14)
        else:
            return (location[0] == 0 or location[0] == 1) and (location[1] == 2 or location[1] == 10)
