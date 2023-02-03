# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from testcharacter import CharacterEntity
from colorama import Fore, Back
from PriorityQueue import PriorityQueue
from sys import maxsize
from teamNN.utility import *


class Node(object):

    def __init__(self, depth, player,wrld,position=None,value=0):
        self.depth = depth
        self.player = player
        self.value = value
        self.wrld = wrld
        self.distancetogoal = a_star_distance_to_exit(wrld,position)
        self.children = []
        self.makechildren()

    def makechildren(self,wrld):
        if self.depth >= 0:
            neighbordlist = self.eight_neighbors(wrld, character_location(wrld)[0], character_location(wrld)[1])
            for neighbord in neighbordlist:
                newdistance = self.distancetogoal - a_star_distance_to_exit(wrld,neighbord)
                newpostion = (neighbord.x, neighbord.y)
                self.children.append( Node(self.depth - 1, - self.player, wrld,newpostion, self.evaluateState(wrld,newdistance,newpostion)))

    def evaluateState(wrld, distance,pos):
        if distance is 0:
            return maxsize
        return - maxsize


    def minimax(self,node, depth, player):
        if (depth == 0) or (abs(node.value == maxsize)):  # or game wine, game lose
            return node.value
        bestvalue = maxsize * -player

        for child in node.children:
            child = node.children[child]
            value = self.minimax(child, depth - 1, -player)
            if (abs(maxsize * player - value) < abs(maxsize * player - bestvalue)):
                bestvalue = value
        return bestvalue

depthserach = 4
currentplayer = 1 #monster

def getNextMove_MiniMax2(wrld):
        if character_location != monster_location:
            currentplayer *= -1
            node = Node(depthserach,currentplayer,wrld,character_location)  
            bestmove = -100
            bestvalue = - currentplayer * maxsize
            for i in range(len(node.children)):
                child = node.children[i]
                value = node.minimax(child,depthserach,-currentplayer)
                if ( abs(currentplayer * maxsize - value)<= abs(currentplayer*maxsize-bestvalue)):
                    bestvalue = value
                    bestmove = i
            return bestmove
