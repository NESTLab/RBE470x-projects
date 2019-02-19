# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class FiniteStateCharacter(CharacterEntity):

    def do(self, wrld):
        # This method calls different algorithms to find the next position to
        # move based on the finite state the character is in.
        if()
        # Character is alone and able to push forward unimpeded by wall
        elif()
        # Character is alone but there is a wall impeding movement
        elif()
        # There is at least 1 bomb within 2 steps
        elif()
        # There is at least 1 monster within 2 steps
        elif()
        # There are 2 monsters within 2 steps
        elif()
        # There is both at least 1 bomb and 1 monster within 2 steps
        else()
        # there should be nothing left, if anything gets to this point, fix it
        pass
