# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from testcharacter import CharacterEntity
from colorama import Fore, Back
from PriorityQueue import PriorityQueue
from sys import maxsize


class Node(object):
    firstTime = True

    def __init__(self, depth, player, distance, value, x, y, wrld):
        self.depth = depth
        self.player = player
        self.distance = distance
        self.value = value
        self.x = x
        self.y = y
        self.wrld = wrld
        self.children = []
        self.makechildren()

    def makechildren(self):
        if self.depth >= 0:
            neighbordlist = self.eight_neighbors(self.x, self.y)
            for neighbord in neighbordlist:
                if self.is_cell_walkable(neighbord):
                    if self.look_for_monster(self.wrld):
                        self.value = -100000000
                    else:
                        self.value = 10000 - self.euclidean_dist(self.wrld.exitcell, neighbord) - self.depth
                        self.distance = self.euclidean_dist(self.wrld.exitcell, neighbord)
                else:
                    self.value = 0
            self.children.append(
                Node(self.depth - 1, -self.player, self.distance, self.value, neighbord.x, neighbord.y, self.wrld))

    def minimax(node, depth, player):
        if (depth == 0) or (node.value == -100000000):  # or game wine, game lose
            return node.value
        bestvalue = maxsize * -player

        for child in node.children:
            child = node.children[child]
            value = minimax(child, depth - 1, -player)
            if (abs(maxsize * player - value) < abs(maxsize * player - bestvalue)):
                bestvalue = value
        return bestvalue

   

        



