# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here

        self.move(1, 0)

        # Prints the current position of the character after the character moves
        print(self.x, self.y)
        pass
