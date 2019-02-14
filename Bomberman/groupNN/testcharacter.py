# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import PriorityQueue


class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
        self.move(0,1)
        # shreeja was here something
        # jose attacks

        pass

    @staticmethod
    def get_exit(wrld):
        x1 = -1
        y1 = -1
        # Find the exit to use for heuristic A*
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.exit_at(x, y):
                    x1 = x
                    y1 = y
        if x1 == -1:
            return -1
        return x1, y1

    # Determining the heuristic value, being Euclidean Distance
    @staticmethod
    def heuristic(start, goal):
        (x1, y1) = start
        (x2, y2) = goal

        # Euclidean distance is the hypotenuse
        # We add the squared values, and finding the sqrt is
        # not necessary as it will never effect the outcome
        value = (x1 + x2)**2 + (y1 + y2)**2
        return value

    @staticmethod
    def a_star(wrld, start, goal):
        frontier = PriorityQueue()
