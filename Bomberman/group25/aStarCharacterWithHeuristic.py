# This is necessary to find the main code
import sys
import heapq

from monsters.selfpreserving_monster import SelfPreservingMonster
from monsters.stupid_monster import StupidMonster

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity, MonsterEntity
from colorama import Fore, Back
import math


# this version of monster is used to determine the type of monster when it is supposed to be hidden (see readme)
class Monster():
    def __init__(self, x, y):
        self.prevX = x
        self.prevY = y
        self.x = 0
        self.y = 0
        self.velocityX = None
        self.velocityY = None

        self.timesIActedSmart = 0
        self.type = None

    def checkVelocity(self, wrld):
        currVelocityX = self.x - self.prevX
        currVelocityY = self.y - self.prevY
        if self.velocityX is None or self.must_change_direction(wrld):
            self.velocityX = currVelocityX
            self.velocityY = currVelocityY
            self.prevX = self.x
            self.prevY = self.y

        elif self.velocityX == currVelocityX and self.velocityY == currVelocityY:
            self.timesIActedSmart += 1
            self.prevX = self.x
            self.prevY = self.y

            # if moved in a manner consistent to self-preserving monster, then it's smart
            if self.timesIActedSmart > 2:
                self.type = "smart"
        else:
            self.type = "stupid"
        return

    # stolen from Self Preserving Monster
    def must_change_direction(self, wrld):
        # Get next desired position
        (nx, ny) = (self.prevX + self.velocityX, self.prevY + self.velocityY)
        # If next pos is out of bounds, must change direction
        if ((nx < 0) or (nx >= wrld.width()) or
                (ny < 0) or (ny >= wrld.height())):
            return True
        # If these cells are an explosion, a wall, or a monster, go away
        # return (wrld.explosion_at(self.x, self.y) or
        return (wrld.wall_at(nx, ny) or
                wrld.exit_at(nx, ny))


class Node():
    def __init__(self, x, y, hval=0, gval=0, parent=None):
        self.x = x
        self.y = y
        self.hval = hval
        self.gval = gval
        self.fval = hval + gval
        self.parent = parent

    # def __eq__(self, other):
    #    return self.position == other.position


class TestCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        super().__init__(name, avatar, x, y)
        self.monsters = []
        self.monsterVelocities = []
        self.path = []
        self.pathIterator = -1

    def do(self, wrld):

        if not self.monsters:
            for key, monsterlist in wrld.monsters.items():
                for monster in monsterlist:
                    self.monsters.append(Monster(monster.x, monster.y))
        else:
            i = 0
            for key, monsterlist in wrld.monsters.items():
                for monster in monsterlist:
                    self.monsters[i].x = monster.x
                    self.monsters[i].y = monster.y
                i += 1

            for monster in self.monsters:
                if monster.type is None or (monster.type == 'smart' and monster.timesIActedSmart < 10):
                    monster.checkVelocity(wrld)

        # TODO get the maximum detection maxDistance of a monster
        if self.checkIfNearMonster(self, 4, wrld):
            selfIsCloserToExitThanMonster = True
            for key, monsterlist in wrld.monsters.items():
                for monster in monsterlist:
                    if len(self.aStarPath(self, Node(7, 18), wrld, False)) >= len(
                            self.aStarPath(monster, Node(7, 18), wrld, False)):
                        selfIsCloserToExitThanMonster = False
                        break

            if not selfIsCloserToExitThanMonster:
                # pick the spot out of the 8 cardinal directions that is least near to a monster.
                self.path = self.runAway(6, wrld)
                self.pathIterator = 0
            elif not self.path or self.checkIfNearMonster(self, 6, wrld) or self.pathIterator == len(self.path) - 1:
                self.path = self.aStarPath(self, Node(7, 18), wrld, True)
                self.pathIterator = 0

        # if no path or within distance 6 of a monster
        # elif not self.path or self.checkIfNearMonster(self, 6, wrld) or self.pathIterator == len(self.path) - 1:
        else:
            self.path = self.aStarPath(self, Node(7, 18), wrld, True)
            self.pathIterator = 0
        # if within distance 3 of a monster
        self.pathIterator += 1
        self.move(self.path[self.pathIterator].x - self.x, self.path[self.pathIterator].y - self.y)
        return

    def checkIfNearMonster(self, node, maxDistance, wrld):
        for monster in self.monsters:
            # if SelfPreservingMonster (smart) monster is within <maxDistance> steps, return true
            distance = self.aStarPath(node, monster, wrld, False)

            if monster.type is not None and monster.type == "smart" and len(distance) - 1 < maxDistance:
                return True

            elif len(distance) - 1 < 2:
                return True

        return False

    # TODO calculate distance function
    # def distanceBetweenPoints():

    # Implement alpha beta search to try to run away faster
    def runAway(self, maxDistance, wrld):
        # put current position into the path
        path = [Node(self.x, self.y)]
        possibleNodes = []

        # start by setting the lowest sum to infinity
        highestSum = 0
        # iterate over the available spots of the eight cardinal directions
        for node in self.getNeighbors(self, Node(7, 18), wrld):
            # put the node farthest from the available locations
            currSum = 0
            for key, monsterlist in wrld.monsters.items():
                for monster in monsterlist:
                    distance = len(self.aStarPath(node, monster, wrld, False))
                    # check if the monster is within distance 6, we don't care about distance from monster after that
                    if distance < maxDistance:
                        currSum += distance
            if currSum == highestSum:
                possibleNodes.append(node)
            elif currSum > highestSum:
                highestSum = currSum
                possibleNodes = [node]
        pathToStart = self.aStarPath(self, Node(0, 0), wrld, False)
        pathToEnd = self.aStarPath(self, Node(7, 18), wrld, False)
        lowestNode = possibleNodes[0]
        for node in possibleNodes:
            if len(pathToEnd) > 1 and pathToEnd[1].x == node.x and pathToEnd[1].y == node.y:
                path.append(node)
                break

            if len(pathToStart) > 1 and pathToStart[1].x == node.x and pathToStart[1].y == node.y:
                path.append(node)
                break
        # if no node was added before
        if len(path) == 1:
            path.append(lowestNode)
        return path

    def aStarPath(self, startNode, endNode, wrld, shouldPathAroundMonsters):
        openNodes = []
        closedNodes = []
        # End node is position 7, 18
        startNode = Node(startNode.x, startNode.y)

        openNodes.append(startNode)

        while len(openNodes) > 0:

            minNode = openNodes[0]
            currIndex = 0

            # find the smallest node fval and append it
            for index, currNode in enumerate(openNodes):
                if currNode.fval < minNode.fval:
                    minNode = currNode
                    currIndex = index

            openNodes.pop(currIndex)
            closedNodes.append(minNode)

            if minNode.x == endNode.x and minNode.y == endNode.y:
                path = []
                currNode = minNode
                while currNode is not None:
                    path.append(currNode)
                    currNode = currNode.parent
                return path[::-1]

            for neighbor in self.getNeighbors(minNode, endNode, wrld):
                isClosed = False
                isOpen = False

                sameNode = None
                nodeIndex = None
                for closedNode in closedNodes:
                    if neighbor.x == closedNode.x and neighbor.y == closedNode.y:
                        isClosed = True
                        break

                for index, openNode in enumerate(openNodes):
                    if neighbor.x == openNode.x and neighbor.y == openNode.y:
                        isOpen = True
                        sameNode = openNode
                        nodeIndex = index
                        break

                if not isClosed:
                    neighbor.gval = minNode.gval + 1
                    neighbor.hval = self.distanceBetweenNodes(neighbor, endNode, wrld, shouldPathAroundMonsters)
                    neighbor.fval = neighbor.gval + neighbor.hval

                    if isOpen and neighbor.fval < sameNode.fval:
                        openNodes[nodeIndex] = neighbor

                    elif not isOpen:
                        openNodes.append(neighbor)
        print("this is the end")

        # for node in self.getNeighbors(currNode, wrld):
        #     currCost = self.distanceBetweenNodes(node, startNode) + self.distanceBetweenNodes(node, endNode)
        #     #if the cost isn't here or
        #     if currCost not in costs or currCost < costs[node]:
        #         costs[node] = currCost
        #         heapVal = currCost
        #         path[node] = currNode

    # code taken from selfpreserving_monster.py
    def getNeighbors(self, node, endNode, wrld):
        listOfNeighbors = []
        # Go through neighboring cells
        for dx in [-1, 0, 1]:
            # Avoid out-of-bounds access
            if (node.x + dx >= 0) and (node.x + dx < wrld.width()):
                for dy in [-1, 0, 1]:
                    # Avoid out-of-bounds access
                    if (node.y + dy >= 0) and (node.y + dy < wrld.height()):
                        # add node if it's the end node, useful if calculating distance to monster
                        if endNode.x == node.x + dx and endNode.y == node.y + dy:
                            listOfNeighbors.append(Node(node.x + dx, node.y + dy, parent=node))
                        # Is this cell safe?
                        elif (wrld.exit_at(node.x + dx, node.y + dy) or
                              wrld.empty_at(node.x + dx, node.y + dy)):
                            if not (dx == 0 and dy == 0):
                                listOfNeighbors.append(Node(node.x + dx, node.y + dy, parent=node))
        # All done
        return listOfNeighbors

    # absolute distance between two nodes
    def distanceBetweenNodes(self, currNode, endNode, wrld, shouldPathAroundMonsters):
        xDistance = abs(endNode.x - currNode.x)
        yDistance = abs(endNode.y - currNode.y)

        # if the node is close to any monster and the endnode is not a monster, try to avoid it

        if shouldPathAroundMonsters:
            for i in range(1, 3):
                for key, monsterlist in wrld.monsters.items():
                    for monster in monsterlist:
                        if (monster.x - i <= currNode.x <= monster.x + i) \
                                and (monster.y - i <= currNode.y <= monster.y + i):
                            return max(xDistance, yDistance) + 400 - i * 100

        # moving diagonally is one move so can combine x and y distance
        return max(xDistance, yDistance)
