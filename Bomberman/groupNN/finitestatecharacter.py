# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class FiniteStateCharacter(CharacterEntity):

    def do(self, wrld):
        # TODO: Code this.  Concept:
        # Figure out where you are and who is around you.
        # Create an if statement different states, such as 'alone', 'with bomb', etc.
        # Call different other algorithms based on which state it is.
        pass
