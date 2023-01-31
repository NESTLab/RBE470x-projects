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

    def __init__(self,depth,player,distance,value,x,y,wrld):
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
            neighbordlist = self.eight_neighbors(self.x,self.y)
            for neighbord in neighbordlist :
                if  self.is_cell_walkable(neighbord):
                    if self.look_for_monster(self.wrld):
                        self.value = -100000000
                    else:    
                        self.value = 10000 - self.euclidean_dist(self.wrld.exitcell,neighbord) - self.depth 
                        self.distance = self.euclidean_dist(self.wrld.exitcell,neighbord) 
                else:
                    self.value = 0
            self.children.append(Node (self.depth-1,-self.player,self.distance,self.value,neighbord.x,neighbord.y,self.wrld))
  

    def look_for_monster(self, wrld):
        for dx in range(-self.rnge, self.rnge+1):
            # Avoid out-of-bounds access
            if ((self.x + dx >= 0) and (self.x + dx < wrld.width())):
                for dy in range(-self.rnge, self.rnge+1):
                    # Avoid out-of-bounds access
                    if ((self.y + dy >= 0) and (self.y + dy < wrld.height())):
                        # Is a character at this position?
                        if (wrld.characters_at(self.x + dx, self.y + dy)):
                            return (True)
        # Nothing found
        return (False)        

    def euclidean_dist(point_one, point_two):
        return ((point_one[0] - point_two[0]) ** 2 + (point_one[1] - point_two[1]) ** 2) ** 0.5

    def eight_neighbors(self, wrld, x, y):
        """
        Returns the walkable 8-neighbors cells of (x,y) in wrld
        """
        return_list = []

        if x != 0 and self.is_cell_walkable(wrld, x - 1, y):
            return_list.append((x - 1, y))
        if x != wrld.width() - 1 and self.is_cell_walkable(wrld, x + 1, y):
            return_list.append((x + 1, y))
        if y != 0 and self.is_cell_walkable(wrld, x, y - 1):
            return_list.append((x, y - 1))
        if y != wrld.height() - 1 and self.is_cell_walkable(wrld, x, y + 1):
            return_list.append((x, y + 1))
        if x != 0 and y != 0 and self.is_cell_walkable(wrld, x - 1, y - 1):
            return_list.append((x - 1, y - 1))
        if x != wrld.width() - 1 and y != 0 and self.is_cell_walkable(wrld, x + 1, y - 1):
            return_list.append((x + 1, y - 1))
        if y != wrld.height() - 1 and x != 0 and self.is_cell_walkable(wrld, x - 1, y + 1):
            return_list.append((x - 1, y + 1))
        if x != wrld.width() - 1 and y != wrld.height() - 1 and self.is_cell_walkable(wrld, x + 1, y + 1):
            return_list.append((x + 1, y + 1))

        return return_list

    def is_cell_walkable(self, wrld, x, y):
        return wrld.exit_at(x, y) or wrld.empty_at(x, y)   

                  

    def minimax(node,depth,player):
        if (depth == 0) or (node.value == -100000000): #or game wine, game lose
            return node.value
        bestvalue = maxsize * -player

        for child in node.children:
            child = node.children[child]
            value = minimax(child,depth -1, -player)
            if(abs(maxsize * player - value)< abs(maxsize*player - bestvalue)):
                bestvalue = value
        return bestvalue

   

        



