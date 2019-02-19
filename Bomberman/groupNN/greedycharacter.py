# This is necessary to find the main code
import sys
import pathfinding as greedyBFS

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class GreedyCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
        exit = [0, 0]
        #get current position
        meX = wrld.me(self).x
        meY = wrld.me(self).y

        #check every gridcell for the exit. Uses the last exit found as the "goal"
        for i in range(wrld.width()):

            for j in range(wrld.height()):

                if wrld.exit_at(i, j):
                    exit = [i, j]

        #get the [x,y] coords of the next cell to go to
        goTo = greedyBFS.getNextStep([meX, meY], exit, wrld,1)

        #move in direction to get to x,y found in prev step
        self.move(-meX + goTo[0], -meY + goTo[1])

        self.place_bomb()
