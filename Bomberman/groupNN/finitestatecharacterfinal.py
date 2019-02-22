# This is necessary to find the main code
import sys
import pathfinding as greedyBFS
import expectimaxV4 as EM

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

        #get current position
        meX = wrld.me(self).x
        meY = wrld.me(self).y

        # True if there is at least 1 monster within 5 steps
        isThereMonster = self.isThereMonster(self, wrld, meX, meY)

        # A list of bombs if there are bombs on the board, empty otherwise
        isThereBomb = self.isThereBomb(self, wrld, meX, meY)

        # A list of explosions if there is at least 1 explosion within 2 steps, empty otherwise
        isThereExplosion = self.isThereExplosion(self, wrld, meX, meY)

        if isThereBomb and isThereMonster and isThereExplosion:
            # There at least 1 bomb, 1 monster, and 1 explosion within the danger zone
            self.greedy(wrld, exit, meX, meY)
        elif isThereBomb and isThereMonster:
            # There is both at least 1 bomb and 1 monster within 2 steps
            self.greedy(wrld, exit, meX, meY)
        elif isThereBomb and isThereExplosion:
            # There is both at least 1 bomb and 1 explosion within 2 steps
            self.greedy(wrld, exit, meX, meY)
        elif isThereExplosion and isThereMonster:
            # There is both at least 1 explosion and 1 monster within 2 steps
            self.greedy(wrld, exit, meX, meY)
        elif isThereMonster:
            # There is at least 1 monster within 2 steps
            self.expectimax(wrld, exit, meX, meY)
        elif isThereBomb:
            # There is at least 1 bomb within 2 steps
            self.greedy(wrld, exit, meX, meY)
        elif isThereExplosion:
            # There is at least 1 explosion within 2 steps
            # TODO: eliminate this case, handle in greedy
            self.greedy(wrld, exit, meX, meY)
        else:
            # There is no danger nearby
            self.greedy(wrld, exit, meX, meY)



    def MoveDist(self, start, end):
        return max(abs(start[0] - end[0]), abs(start[1] - end[1]))

    def isThereBomb(self, wrld, meX, meY):
        # List of bombs across the entire board
        try:
            bombs = next(iter(wrld.bombs.values()))
            return bombs
        except IndexError:
            return None

    def isThereExplosion(self, wrld, meX, meY):
        try:
            # Returns all of the close explosions
            exps = []

            # All of the explosions
            e = next(iter(wrld.explosions.values()))

            # Filtering only close monsters
            for exp in e:
                if self.MoveDist([meX, meY], [exp.x, exp.y]) <= 1:
                    exps.append(exp)

            return exps
        except IndexError:
            return None


    def isThereMonster(self, wrld, meX, meY):
        try:
            # All of the monsters
            m = next(iter(wrld.monsters.values()))

            # Filtering only close monsters
            for monstr in m:
                if self.MoveDist([meX, meY], [monstr.x, monstr.y]) <= 5:
                    return True
            return False
        except IndexError:
            return False

    def expectimax(self, wrld, exit, meX, meY):
        # Complete the greedy algorithm
        # Get the [x,y] coords of the next cell to go to
        goTo = EM.expectiMax(wrld, 2)

        # move in direction to get to x,y found in prev step
        self.move(-meX + goTo[0], -meY + goTo[1])


    def greedy(self, wrld, exit, meX, meY):
        # Returns true if the character can be moved, false if not

        # Complete the greedy algorithm
        # Get the [x,y] coords of the next cell to go to
        goTo = greedyBFS.getNextStep([meX, meY], exit, wrld)

        #move in direction to get to x,y found in prev step
        self.move(-meX + goTo[0], -meY + goTo[1])

        if not greedy:
            # TODO: Improve bomb placement and pathfinding combinations
            goTo = greedyBFS.getNextStep([meX, meY], exit, wrld,0)
            if wrld.wall_at(goTo[0],goTo[1]):
                NotSetThisTime = False
                self.place_bomb()
            else:
                self.move(-meX + goTo[0], -meY + goTo[1])
