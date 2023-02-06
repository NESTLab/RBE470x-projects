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
    WAIT_FOR_BOMB = 4
    FAR_FROM_MONSTER = 5
    CLOSE_TO_MONSTER = 6


class TestCharacter(CharacterEntity):
    waitCount = 0
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
                self.dodge_bomb_away_from_monster(wrld)
                self.waitCount = 0
                self.stateMachine = State.WAIT_FOR_BOMB
            case State.WAIT_FOR_BOMB:
                self.move(0, 0)
                self.waitCount += 1
                if self.waitCount > 1:
                    self.bombCoolDown = 7
                    self.stateMachine = State.FAR_FROM_MONSTER
            case State.FAR_FROM_MONSTER:
                self.ai.reccursionDepth = 2
                self.ai.isExpectimax = False
                nextCell = self.ai.get_next_move(wrld)
                self.move(nextCell[0] - self.x, nextCell[1] - self.y)
                print("Score of current world", evaluate_state(wrld, character_location(wrld), monster_location(wrld)))
                print("Selected Move: ", nextCell)
                if self.can_place_bomb(nextCell):
                    self.stateMachine = State.PLACE_BOMB
                if self.can_place_bomb(nextCell):
                    self.stateMachine = State.PLACE_BOMB
                if a_star_distance_to_monster(wrld, (nextCell[0], nextCell[1])) < 8:
                    self.stateMachine = State.CLOSE_TO_MONSTER
            case State.CLOSE_TO_MONSTER:
                self.ai.reccursionDepth = 3
                self.ai.isExpectimax = True  # True
                if len(wrld.monsters.values()) > 1:
                    self.ai.isExpectimax = False
                nextCell = self.ai.get_next_move(wrld)
                self.move(nextCell[0] - self.x, nextCell[1] - self.y)
                print("Score of current world", evaluate_state(wrld, character_location(wrld), monster_location(wrld)))
                print("Selected Move: ", nextCell)
                # The monster is one tile away, so we need to place a bomb to try to escape
                # if len(a_star(wrld, (self.x, self.y), monster_location(wrld))) <= 3:
                #     self.stateMachine = State.PLACE_BOMB
                if evaluate_state(wrld, character_location(wrld), monster_location(wrld)) < -20:
                    self.stateMachine = State.PLACE_BOMB
                if self.can_place_bomb(nextCell):
                    self.stateMachine = State.PLACE_BOMB
                if self.can_place_bomb(nextCell):
                    self.stateMachine = State.PLACE_BOMB
                if a_star_distance_to_monster(wrld, (nextCell[0], nextCell[1])) > 8:
                    self.stateMachine = State.FAR_FROM_MONSTER

    def can_place_bomb(self, location, ):
        if not self.bombCoolDown <= 0:
            return False
        return ((location[0] == 6) and (location[1] == 6 or location[1] == 14)) or (
                (location[0] == 1) and (location[1] == 2 or location[1] == 10))

    def dodge_bomb_away_from_monster(self, wrld):
        left_up_score = None
        right_up_score = None
        left_down_score = None
        right_down_score = None
        if is_cell_in_range(wrld, self.x + 1, self.y - 1) and is_cell_walkable(wrld, self.x + 1, self.y - 1):
            right_up_score = len(a_star(wrld, (self.x + 1, self.y - 1), monster_location(wrld)))
        if is_cell_in_range(wrld, self.x - 1, self.y - 1) and is_cell_walkable(wrld, self.x - 1, self.y - 1):
            left_up_score = len(a_star(wrld, (self.x - 1, self.y - 1), monster_location(wrld)))
        if is_cell_in_range(wrld, self.x + 1, self.y + 1) and is_cell_walkable(wrld, self.x + 1, self.y + 1):
            right_down_score = len(a_star(wrld, (self.x + 1, self.y + 1), monster_location(wrld)))
        if is_cell_in_range(wrld, self.x - 1, self.y + 1) and is_cell_walkable(wrld, self.x - 1, self.y + 1):
            left_down_score = len(a_star(wrld, (self.x - 1, self.y + 1), monster_location(wrld)))
        dodge_options = [left_up_score, right_up_score, left_down_score, right_down_score]
        dodge_options = [x for x in dodge_options if x is not None]
        print(dodge_options)
        if len(dodge_options) > 0:
            best_move = max(dodge_options)
            if best_move == left_up_score:
                self.move(-1, -1)
            elif best_move == right_up_score:
                self.move(1, -1)
            elif best_move == left_down_score:
                self.move(-1, 1)
            elif best_move == right_down_score:
                self.move(1, 1)
