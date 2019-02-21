# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity, AIEntity, MovableEntity
from colorama import Fore, Back
import random
from sensed_world import SensedWorld
import math

class Scen2Var2Character(CharacterEntity):

    BOMB = 0

    def __init__(self, name, avatar, x, y, depth):
        AIEntity.__init__(self, name, avatar)
        MovableEntity.__init__(self, x, y)
        # Whether this character wants to place a bomb
        self.maybe_place_bomb = False
        # Debugging elements
        self.tiles = {}
        self.max_depth = depth
        # List of cells already visited
        self.visited = []
        self.foundexit = False
        self.exit = (0,0)
        # Location of bomb on board. (-1,-1) means there is no bomb.
        self.bomb = (-1,-1)

    def do(self, wrld):
        # Your code here
        #pass
        # Adds current position to cells already visited
        self.visited.append((self.x, self.y))

        # On the first move, searches through whole board to find exit
        # Would have to modify if we want to do last man standing, but I think we'd use a different map for that
        while not self.foundexit:
            for x in range(0,wrld.width()):
                for y in range(0,wrld.height()):
                    if wrld.exit_at(x,y):
                        self.foundexit = True
                        self.exit = (x,y)
        # Checks if a bomb is still at the last bomb position and resets self.bomb if it isn't
        if not self.bomb == (-1,-1) and not wrld.bomb_at(self.bomb[0],self.bomb[1]):
            self.bomb = (-1,-1)
        move = self.alpha_beta_search(wrld)[1]
        if move == self.BOMB:
            self.place_bomb()
            self.bomb = (self.x,self.y)
            # Stops moving after it places a bomb, so it doesn't walk into an explosion.
            # TODO: The character can place a bomb and move on the same turn. Probably best to use this to my advantage.
            self.move(0,0)
        else:
            self.move(move[0],move[1])

    def get_nextworlds(self, wrld):
        # Return accessible next worlds after character's movement in given world
        # Possible moves include moving to empty cells, moving to the exit cell, and placing a bomb
        # List of possible worlds
        nextworlds = []
        """
        for i in range (x-1,x+2):
            for j in range (y-1,y+2):
                if wrld.empty_at(i,j) and not (x,y) == (i,j):
                    cells.append((i,j))
        """
        # Adapted from example code on Github
        # Loop through delta x
        for dx in [-1,0,1]:
            # Avoid out-of-bound indexing
            if(self.x+dx >=0) and (self.x+dx < wrld.width()):
                # Loop through delta y
                for dy in [-1,0,1]:
                    # Originally wrapped below in a check that the position was not the character's current position
                    # But in some cases, not moving at all may be necessary
                    # Still can't stay still, however; move isn't counted as possible if a character is there
                    # Avoid out-of-bound indexing
                    if (self.y+dy >= 0) and (self.y+dy < wrld.height()) and (wrld.empty_at(self.x+dx,self.y+dy) or wrld.exit_at(self.x+dx,self.y+dy)):
                        # Add cell to list
                        # cells.append((self.x+dx,self.y+dy))

                        clonewrld = SensedWorld.from_world(wrld)
                        clonewrld.me(self).move(dx,dy)
                        (newwrld, events) = clonewrld.next()
                        nextworlds.append((newwrld,events,(dx,dy)))
        # Includes world in which character places bomb
        # The final value in the tuple, move, contains either the space the character moves to or self.BOMB if they
        # place a bomb
        clonewrld = SensedWorld.from_world(wrld)
        clonewrld.me(self).place_bomb()
        (newwrld, events) = clonewrld.next()
        nextworlds.append((newwrld,events,self.BOMB))
        return nextworlds

    def alpha_beta_search(self,wrld):
        # Alpha beta functio
        v = self.max_value(wrld,[],-99999,99999,self.max_depth)
        return v

    def max_value(self,wrld,events,alpha,beta,depth):
        # Max value helper function for alpha-beta pruning
        # Return 99999 if a win condition has been met (in this case, if the character has reached the exit)
        # Return -99999 if a lose condition has been met (if the character has been hit by a bomb or killed by a
        # monster)
        # For now, assumes there's only one character
        # TODO: Account for time running out
        for e in events:
            if e.tpe == e.CHARACTER_FOUND_EXIT:
                return (99999,(0,0))
            if e.tpe == e.BOMB_HIT_CHARACTER:
                return (-99999,(0,0))
            if e.tpe == e.CHARACTER_KILLED_BY_MONSTER:
                return (-99999,(0,0))
        if depth == 0:
            # Perform evaluation function
            return (self.distance_evaluation(wrld),(0,0))
        # Default move is no move at all
        v = (-99999, (0,0))
        #Iterate through possible new worlds
        for (newwrld, newevents, move) in self.get_nextworlds(wrld):
            # Adapted from example code, but I don't know if it will really move.
            #self.move(action[0],action[1])
            # Get new wrld
            # (newwrld, newevents) = wrld.next()

            # Associated move calculated as the difference between the clone character's position and
            # the current character's position
            # Or the difference between the exit's position and the current character's position if the character has
            # found the exit in this new board
            # TODO: Account for character death
            """
            charoffboard = False
            for e in newevents:
                if e.tpe == e.CHARACTER_FOUND_EXIT:
                    charoffboard = True
            if charoffboard:
                move = (self.exit[0] - self.x, self.exit[1] - self.y)       
            else:
                move = (newwrld.me(self).x-self.x,newwrld.me(self).y-self.y)
            # If there's a bomb at the character's location on this board, the move is BOMB, meaning placing a bomb
            # rather than moving
            if newwrld.bomb_at(newwrld.me(self).x,newwrld.me(self).y):
                move = self.BOMB
            """
            newValue = self.min_value(newwrld,newevents,alpha,beta,depth-1)[0]
            if v[0] < newValue:
                v = (newValue,move)
            if v[0] >= beta:
                return v
            alpha = max(alpha,v[0])
        return v


    def min_value(self,wrld,events,alpha,beta,depth):
        # Min value helper function for alpha-beta pruning
        # Return 99999 if a win condition has been met (in this case, if the character has reached the exit)
        # Return -99999 if a lose condition has been met (if the character has been hit by a bomb or killed by a
        # monster)
        # For now, assumes there's only one character
        # TODO: Account for time running out
        for e in events:
            if e.tpe == e.CHARACTER_FOUND_EXIT:
                return (99999,(0,0))
            if e.tpe == e.BOMB_HIT_CHARACTER:
                return (-99999,(0,0))
            if e.tpe == e.CHARACTER_KILLED_BY_MONSTER:
                return (-99999,(0,0))
        if depth == 0:
            # Perform evaluation function
            return (self.distance_evaluation(wrld),(0,0))
        # Default move is no move at all
        v = (99999, (0,0))
        for (newwrld, newevents, move) in self.get_nextworlds(wrld):
            # Adapted from example code, but I don't know if it will really move.
            #self.move(action[0], action[1])
            # Get new wrld
            # (newwrld, newevents) = wrld.next()

            # Associated move calculated as the difference between the clone character's position and
            # the current character's position
            # Or the difference between the exit's position and the current character's position if the character has
            # found the exit in this new board
            # TODO: Account for character death
            """
            charoffboard = False
            for e in newevents:
                if e.tpe == e.CHARACTER_FOUND_EXIT:
                    charoffboard = True
            if charoffboard:
                move = (self.exit[0] - self.x, self.exit[1] - self.y)
            else:
                move = (newwrld.me(self).x - self.x, newwrld.me(self).y - self.y)
            # If there's a bomb at the character's location on this board, the move is BOMB, meaning placing a bomb
            # rather than moving
            if newwrld.bomb_at(newwrld.me(self).x, newwrld.me(self).y):
                move = self.BOMB
            """
            newValue = self.max_value(newwrld, newevents, alpha, beta, depth - 1)[0]
            if v[0] > newValue:
                v = (newValue,move)
            if v[0] <= alpha:
                return v
            beta = min(beta, v[0])
        return v

    # Evaluation function
    # For now, calculates cost based on distance from exit cell, but I may have to change this
    # Update 3: After maxing the max and min methods account for an off-board character, it worked fine. However, the
    # path the character follows is still less than optimal; they jump all over the place.
    # TODO: (possibly) account for obstacles
    def distance_evaluation(self,wrld):
        position = (wrld.me(self).x,wrld.me(self).y)
        # Uses distance formula to calculate distance between position and exit
        distance = math.sqrt(math.pow(position[0]-self.exit[0],2) + math.pow(position[1]-self.exit[1],2))

        bombdistance = 99999
        xbombdistance = 99999
        ybombdistance = 99999
        xmonsterdistance = 99999
        ymonsterdistance = 99999
        withinmonsterrange = False
        dangercost = 0
        if not self.bomb == (-1,-1):
            # bombdistance = max(abs(self.bomb[0]-wrld.me(self).x),abs(self.bomb[1]-wrld.me(self).y)
            xbombdistance = abs(self.bomb[0]-wrld.me(self).x)
            ybombdistance = abs(self.bomb[1]-wrld.me(self).y)
        # If within range of a bomb, getting away from it should be top priority.
        if (xbombdistance <= wrld.expl_range and ybombdistance == 0) or (ybombdistance <= wrld.expl_range and xbombdistance == 0):
            bombdistance = max(xbombdistance,ybombdistance)
            fraction = wrld.expl_range + 1 - bombdistance
            dangercost = -9999*fraction
        # If any neighboring cell contains a monster, the character is considered within monster range
        # NOTE: Monsters can have a bigger detection range than 1. May need to account for this.
        for dx in [-1,0,1]:
            # Avoid out-of-bound indexing
            if (wrld.me(self).x + dx >= 0) and (wrld.me(self).x + dx < wrld.width()):
                for dy in [-1,0,1]:
                    # Avoid out-of-bound indexing
                    if (wrld.me(self).y+dy >= 0) and (wrld.me(self).y+dy < wrld.height()) and wrld.monsters_at(wrld.me(self).x+dx,wrld.me(self).y+dy):
                            withinmonsterrange = True
        # Escaping monsters should be equal priority to escaping explosions
        if withinmonsterrange:
            dangercost = dangercost - 9999

        # As should escaping explosions
        # if wrld.explosion_at(wrld.me(self).x,wrld.me(self).y):
        #    dangercost = dangercost -9999

        # Distance made negative for return value so shorter distances are of higher value
        # print(distance*-1+dangercost)
        return distance * -1 + dangercost