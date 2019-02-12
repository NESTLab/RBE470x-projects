# This is necessary to find the main code
import sys
import pathfinding as greedyBFS

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
        exit = [0, 0]
        meX = wrld.me(self).x
        meY = wrld.me(self).y

        for i in range(wrld.width()):

            for j in range(wrld.height()):

                if wrld.exit_at(i, j):
                    exit = [i, j]

        goTo = greedyBFS.getNextStep([meX, meY], exit, wrld)


        self.move(-meX + goTo[0], -meY + goTo[1])

