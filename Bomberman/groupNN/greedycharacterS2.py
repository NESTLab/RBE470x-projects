# This is necessary to find the main code
import sys
import pathfinding as greedyBFS
import pathfinding4conn as greedyBFSNoWall

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back


class GreedyCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.state = 'm'
        self.bomb_at = []


    def do(self, wrld):

        NotSetThisTime = True
        # Your code here
        if self.state is 'm' and NotSetThisTime:
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
            goTo = greedyBFS.getNextStep([meX, meY], exit, wrld)
            if goTo is None:
                goTo = greedyBFSNoWall.getNextStep([meX, meY], exit, wrld)
                if wrld.wall_at(goTo[0],goTo[1]):
                    NotSetThisTime = False
                    self.state='b'
                    self.place_bomb()
                    self.bomb_at = [meX,meY]
                else:
                    self.move(-meX + goTo[0], -meY + goTo[1])

            else:
                self.move(-meX + goTo[0], -meY + goTo[1])
            #move in direction to get to x,y found in prev step

        if self.state is 'b' and NotSetThisTime:
            if (wrld.bomb_at(self.bomb_at[0],self.bomb_at[1]) is not None) or (wrld.explosion_at(self.bomb_at[0],self.bomb_at[1]) is not None):
                self.move(-1,-1)
            else:
                self.state = 'm'

