# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from testcharacter import CharacterEntity
from colorama import Fore, Back
from PriorityQueue import PriorityQueue
from sys import maxsize
from utility import *


class Node(object):

    def __init__(self, depth, player,wrld,position,value=0):
        self.depth = depth
        self.player = player
        self.value = value
        self.wrld = wrld
        self.position = position
        self.distancetogoal = a_star_distance_to_exit(wrld,position)
        #print("checkone " + str(position))  
        #print("checktwo: " + str(player))  
        self.children = []
        self.makechildren(self.wrld)

    def makechildren(self,wrld):
        if self.depth >= 0:
            neighbordlist = eight_neighbors(wrld, character_location(wrld)[0], character_location(wrld)[1])
            #print("check3 " + str(character_location(wrld)[0]))  
            #print("check3 " + str(character_location(wrld)[1]))  
            for neighbord in neighbordlist:
                
                newdistance = self.distancetogoal - a_star_distance_to_exit(wrld,neighbord)
                #print(neighbord)
                #print(newdistance)
                newpostion = (neighbord[0], neighbord[1])
                self.children.append(Node(self.depth - 1, - self.player, wrld,newpostion, evaluateState(wrld,newpostion)))

    

def evaluateState(wrld, pos):
        exitDist = a_star_distance_to_exit(wrld, pos)
        mosnterDist = euclidean_distance_to_monster(wrld,pos)
        print("Pos: " + str(pos))
        print("Exit Dist: " + str(exitDist))
        print("Monster Dist: " + str(mosnterDist))
        print("Value: " + str((mosnterDist * 0.7) - exitDist))
        if exitDist == 0:
            
            return maxsize
        return (mosnterDist * 0.7) - exitDist

def minimax(node, depth, player):
        
        #print(node)
        if (depth == 0) or (abs(node.value == maxsize)):  # or game wine, game lose
            return node.value
        bestvalue = maxsize * -player

        for i in range(len(node.children)):
            child = node.children[i]
            value = minimax(child, depth - 1, -player)
            if (abs(maxsize * player - value) < abs(maxsize * player - bestvalue)):
                bestvalue = value
        
        return bestvalue

def getNextMove_MiniMax2(wrld):
        depthserach = 2
        currentplayer = -1 #monster
        location = character_location(wrld)
        #print("movemove")
        
        #print(character_location(wrld))
        #print(monster_location(wrld))

        if character_location(wrld) != monster_location(wrld):
        
            currentplayer *= -1
            node = Node(depthserach,currentplayer,wrld,location)  
            bestmove = node.position
            bestvalue = - currentplayer * maxsize
            for i in range(len(node.children)):
                child = node.children[i]
                value = minimax(child,depthserach,-currentplayer)
                if ( abs(currentplayer * maxsize - value)<= abs(currentplayer*maxsize-bestvalue)):
                    bestvalue = value
                    bestmove = child.position
            print("what is returning: " + str(bestmove))        
            return bestmove
