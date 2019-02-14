# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back


class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
        self.move(0,1)
        # jose attacks

        pass

    @staticmethod
    def get_exit(wrld):
        x1 = 0
        y1 = 0
        # Find the exit to use for heuristic A*
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.exit_at(x, y):
                    x1 = x
                    y1 = y
        return x1, y1
