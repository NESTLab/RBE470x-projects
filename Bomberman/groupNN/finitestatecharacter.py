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

        # A list of objects within the perimeter of 2 spaces
        closeObjects = self.checkPerimeter2(wrld)
        # True if there is an impassable wall within 1 space,
        # False otherwise
        isThereWall = self.impassableWall(wrld)
        # True if there is at least 1 bomb within 2 steps
        isThereBomb = isThereBomb(closeObjects)
        # True if there is at least 1 monster within 2 steps
        isThereMonster = isThereMonster(closeObjects)

        if not closeObjects and not isThereWall:
            # Character is alone and able to push forward unimpeded by wall
            self.greedy(wrld)
        elif not closeObjects and isThereWall:
            # Character is alone but there is a wall impeding movement
            self.greedy(wlrd)
        elif isThereBomb and isThereMonster:
            # There is both at least 1 bomb and 1 monster within 2 steps
            self.greedy(wrld)
        elif isThereMonster:
            # There is at least 1 monster within 2 steps
            self.greedy(wrld)
        elif isThereBomb:
            # There is at least 1 bomb within 2 steps
            self.greedy(wrld)
        else:
            # there should be nothing left, if anything gets to this point,
            # fix it
            self.greedy(wrld)

    def checkPerimeter2(self, wrld):
        # Check the perimeter around the character at a depth of 2 for any other
        # objects, return a list of the objects within the perimeter

        # Note: we could also have it return a list of tuples [object, type, position]
        # if we think the if elses will operate better that way
        closeObjects = {}
        return closeObjects

    def impassableWall(self, wrld):
        # Check to see if there is an impassable wall a step ahead of the
        # character
        isThereWall = False

        # Note: can be changed to be closer or farther away from wall
        return isThereWall

    def isThereBomb(closeObjects):
        # Use the established list of objects within the perimeter to see if
        # there is a bomb nearby
        isThereBomb = False

        return isThereBomb

    def isThereWall(closeObjects):
        # Use the established list of objects within the perimeter to see if
        # there is a wall nearby
        isThereWall = False

        return isThereWall

    def greedy(self, wrld):
        # Complete the greedy algorithm
