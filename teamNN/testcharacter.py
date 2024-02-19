# This is necessary to find the main code
import sys
from enum import Enum

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity

sys.path.insert(1, '../teamNN')
from utility import *
from project1.minimax import *

#Organizing all states
class State(Enum):
    START = 1
    PLACE_BOMB = 2
    WAIT_FOR_BOMB = 4
    FAR_FROM_MONSTER = 5
    CLOSE_TO_MONSTER = 6
    EXPLORATION = 7;


class TestCharacter(CharacterEntity):
    waitCount = 0
    bombCoolDown = 0
    stateMachine = State.START
    ai = AI()
    #Function starts here
    def do(self, wrld):
        monsterNum = len(wrld.monsters.values())
        print("Current State: ", self.stateMachine)
        self.bombCoolDown -= 1
        #State Machines starts here
        match self.stateMachine:

            #Start state -> When game begins, character will jump into this state
            case State.START:
                self.move(0, 1)
                # #If at corner
                # if self.x == 0 and self.y == 2:
                self.stateMachine = State.PLACE_BOMB

            #Place bomb, dodge and move onto WaitForBomb state
            case State.PLACE_BOMB:
                self.place_bomb()
                self.dodge_bomb_away_from_monster(wrld)
                self.waitCount = 0
                self.stateMachine = State.WAIT_FOR_BOMB

            #Wait till the bomb explodes (stay still) then move on the FarFromMonster state
            case State.WAIT_FOR_BOMB:
                self.move(0, 0)
                self.waitCount += 1
                if self.waitCount > 1:
                    self.bombCoolDown = 7
                    self.stateMachine = State.FAR_FROM_MONSTER
            #State where the monster is >= 8 distance from the character
            case State.EXPLORATION:
                # print("Exploring")
                # w = wrld.width
                # h = wrld.height
                # print(w)
                # print(h)
                #
                # for x in range(7):
                #     for y in range(17):
                #
                #         if wrld.wall_at(x, y):
                #             print(x, y)
                #             path = a_star(wrld, (x, y), character_location(wrld))
                #             if path.pop(len(path) - 1) != wrld.exitcell:
                #                 goal = (x, y)
                #                 break
                if a_star_distance_to_monster(wrld, (self.x, self.y + 1)) < 8 and len(wrld.monsters) > 0:
                    self.stateMachine = State.CLOSE_TO_MONSTER

                if is_cell_walkable(wrld, self.x, self.y + 1):
                    print("cell walkable")
                    self.move(self.x, self.y + 1)
                else:
                    self.stateMachine = State.PLACE_BOMB

            case State.FAR_FROM_MONSTER:
                #Running minimax, depth = 2
                self.ai.reccursionDepth = 2
                self.ai.isExpectimax = False

                print("a_star distance", a_star_distance_to_exit(wrld, character_location(wrld)))

                if a_star_distance_to_exit(wrld, character_location(wrld)) < 0:
                    print("No path to exit")
                    self.stateMachine = State.EXPLORATION

                #Generate AI move
                nextCell = self.ai.get_next_move(wrld)
                #Perform the move
                self.move(nextCell[0] - self.x, nextCell[1] - self.y)
                print("Score of current world", evaluate_state(wrld, character_location(wrld), monster_location(wrld)))
                print("Selected Move: ", nextCell)

                # #If can place bomb -> placebomb
                if self.can_place_bomb(nextCell):
                    self.stateMachine = State.PLACE_BOMB
                #If distance to monster < 8 -> close to monster
                if a_star_distance_to_monster(wrld, (nextCell[0], nextCell[1])) < 8 and len(wrld.monsters) > 0:
                    self.stateMachine = State.CLOSE_TO_MONSTER

            case State.CLOSE_TO_MONSTER:
                #Using expectimax
                self.ai.reccursionDepth = 3
                self.ai.isExpectimax = False
                print("a_star distance", a_star_distance_to_exit(wrld, character_location(wrld)))

                if a_star_distance_to_exit(wrld, character_location(wrld)) < 0:
                    print("No path to exit")
                    self.stateMachine = State.PLACE_BOMB
                nextCell = self.ai.get_next_move(wrld)
                self.move(nextCell[0] - self.x, nextCell[1] - self.y)

                print("Score of current world", evaluate_state(wrld, character_location(wrld), monster_location(wrld)))
                print("Selected Move: ", nextCell)

                # Evaluating states and current position to place bomb if possible
                if evaluate_state(wrld, character_location(wrld), monster_location(wrld)) < -20:
                    self.stateMachine = State.PLACE_BOMB
                if self.can_place_bomb(nextCell):
                    self.stateMachine = State.PLACE_BOMB
                if a_star_distance_to_monster(wrld, (nextCell[0], nextCell[1])) > 8:
                    self.stateMachine = State.FAR_FROM_MONSTER


    def can_place_bomb(self, location, ):
        """
        Checking if the prev bomb has exploded yet to place a new bomb in an empty location
        """
        if not self.bombCoolDown <= 0:
            return False
        return ((location[0] == 6) and (location[1] == 6 or location[1] == 14)) or (
                (location[0] == 1) and (location[1] == 2 or location[1] == 10))


    def dodge_bomb_away_from_monster(self, wrld):
        """
        Move away the position where bomb can explode or meet the monster
        """
        #Score that the bomb can reach -> hit wall or hit monster
        left_up_score = None
        right_up_score = None
        left_down_score = None
        right_down_score = None

        #Calculating each direction score
        if is_cell_in_range(wrld, self.x + 1, self.y - 1) and is_cell_walkable(wrld, self.x + 1, self.y - 1):
            right_up_score = len(a_star(wrld, (self.x + 1, self.y - 1), monster_location(wrld)))
        if is_cell_in_range(wrld, self.x - 1, self.y - 1) and is_cell_walkable(wrld, self.x - 1, self.y - 1):
            left_up_score = len(a_star(wrld, (self.x - 1, self.y - 1), monster_location(wrld)))
        if is_cell_in_range(wrld, self.x + 1, self.y + 1) and is_cell_walkable(wrld, self.x + 1, self.y + 1):
            right_down_score = len(a_star(wrld, (self.x + 1, self.y + 1), monster_location(wrld)))
        if is_cell_in_range(wrld, self.x - 1, self.y + 1) and is_cell_walkable(wrld, self.x - 1, self.y + 1):
            left_down_score = len(a_star(wrld, (self.x - 1, self.y + 1), monster_location(wrld)))

        #Summarizing up the dodge options to choose the best one
        dodge_options = [left_up_score, right_up_score, left_down_score, right_down_score]
        dodge_options = [x for x in dodge_options if x is not None]
        print(dodge_options)
        #Return the move based on the best dodge option (which option that brings the most score)
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
