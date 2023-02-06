# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from PriorityQueue import PriorityQueue

sys.path.insert(1, '../teamNN')
from utility import *
from minimax import getNextMove_MiniMax
from minimaxnode import *


class TestCharacter(CharacterEntity):
    firstTime = True
    a_star_path = []      
    

    def do(self, wrld):

        
        print("on do function")
        print(getNextMove_MiniMax2(wrld))
        nextCell = getNextMove_MiniMax2(wrld)
        print("Selected Move: ", nextCell)
        self.move(nextCell[0] - self.x, nextCell[1] - self.y)

        """
        if self.firstTime:
            print("Character at", self.x, self.y)
            print("Exit at", wrld.exitcell)
            print("Explosions:", wrld.explosions)
            print("Monsters:", wrld.monsters)
            print("Monster Location", monster_location(wrld))
            print("Euclidean distance to exit:", euclidean_distance_to_exit(wrld))
            print("Manhattan distance to exit:", manhattan_distance_to_exit(wrld))
            print("Euclidean distance to monster:", euclidean_distance_to_monster(wrld))
            print("Manhattan distance to monster:", manhattan_distance_to_monster(wrld))
            self.a_star_path = a_star(wrld)
            print("A* path to goal:", self.a_star_path)
        
            for point in self.a_star_path:
                #Mark path on world
                self.set_cell_color(point[0], point[1], Fore.RED + Back.GREEN)
            self.firstTime = False
        else:
            nextCell = self.a_star_path.pop(0)
            print("nextcell")
            print(nextCell)
            self.move(nextCell[0] - self.x, nextCell[1] - self.y)
        
        """