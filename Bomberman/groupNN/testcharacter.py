# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back


class TestCharacter(CharacterEntity):

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
        if x1 or y1 == -1:
            pass
        return x1, y1

    def do(self, wrld):
        # Your code here
        x, y = self.get_exit(wrld)
        print(self.get_exit(wrld))
        pass
