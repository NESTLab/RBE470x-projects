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

        # Find the exit to move towards
        exit = [0, 0]

        #check every gridcell for the exit. Uses the last exit found as the "goal"
        for i in range(wrld.width()):

            for j in range(wrld.height()):

                if wrld.exit_at(i, j):
                    exit = [i, j]


        # A list of objects within the perimeter of 2 spaces
        closeObjects = self.checkPerimeter2(wrld)
        # True if there is an impassable wall within 1 space,
        # False otherwise
        isThereWall = self.impassableWall(wrld)
        # True if there is at least 1 bomb within 2 steps
        isThereBomb = isThereBomb(closeObjects)
        # True if there is at least 1 monster within 2 steps
        isThereMonster = isThereMonster(closeObjects)
        # True if there is at least 1 explosion within 2 steps
        isThereExplosion = isThereExplosion(closeObjects)

        if not closeObjects and not isThereWall:
            # Character is alone and able to push forward unimpeded by wall
            self.greedy(wrld, exit)
        elif not closeObjects and isThereWall:
            # Character is alone but there is a wall impeding movement
            self.greedy(wlrd, exit)
        elif isThereBomb and isThereMonster and isThereExplosion:
            # There at least 1 bomb, 1 monster, and 1 explosion within 2 steps
            self.greedy(wrld, exit)
        elif isThereBomb and isThereMonster:
            # There is both at least 1 bomb and 1 monster within 2 steps
            self.greedy(wrld, exit)
        elif isThereBomb and isThereExplosion:
            # There is both at least 1 bomb and 1 explosion within 2 steps
            self.greedy(wrld, exit)
        elif isThereExplosion and isThereMonster:
            # There is both at least 1 explosion and 1 monster within 2 steps
            self.greedy(wrld, exit)
        elif isThereMonster:
            # There is at least 1 monster within 2 steps
            self.greedy(wrld, exit)
        elif isThereBomb:
            # There is at least 1 bomb within 2 steps
            self.greedy(wrld, exit)
        elif isThereExplosion:
            # There is at least 1 explosion within 2 steps
            self.greedy(wrld, exit)
        else:
            # there should be nothing left, if anything gets to this point,
            # fix it
            self.greedy(wrld, exit)

    def checkPerimeter2(self, wrld):
        # Check the perimeter around the character at a depth of 2 for any other
        # objects, return a list of tuples [typeNum, x, y] that represents anything
        # found

        # TypeNum represents each type of object as follows:
        # 0 = wall
        # 1 = bomb
        # 2 = monster
        # 3 = explosion

        # Does not currently detect other characters or exit, but can be made to

        # The list to be returned
        closeObjects = {}

        # Get the position of the character
        meX = wrld.me(self).x
        meY = wrld.me(self).y

        # Go through each space in the box around the character
        for i in range -2 to 2:
            for j in range -2 to 2:
                # if this is not the space the character is in
                if i != 0 and j != 0:
                    # if the postition is in world bounds
                    if not meX + i >= width or meX + i <= 0 or meY + j >= height or meY + j <= 0:
                        # check if there is a wall there and append if so
                        if wrld.wall_at(meX + i, meY + j):
                            closeObjects.append([0, meX + i, meY + j])
                        # check if there is a bomb there and append if so
                        elif wrld.bomb_at(meX + i, meY + j):
                            closeObjects.append([1, meX + i, meY + j])
                        # check if there is a monster(s) there and append if so
                        elif wrld.monsters_at(meX + i, meY + j):
                            closeObjects.append([2, meX + i, meY + j])
                        # check if there is an explosion there and append if so
                        elif wrld.explosion_at(meX + i, meY + j):
                            closeObjects.append([3, meX + i, meY + j])

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

    def isThereExplosion(closeObjects):
        # Use the established list of objects within the perimeter to see if
        # there is an explosion nearby
        isThereExplosion = False

        return isThereExplosion

    def greedy(self, wrld, exit):
        # Complete the greedy algorithm
