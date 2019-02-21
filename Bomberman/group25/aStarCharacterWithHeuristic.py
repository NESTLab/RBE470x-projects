# This is necessary to find the main code
import sys
import heapq

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back


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
        self.path = []
        self.pathIterator = -1

    def do(self, wrld):
        # if no path
        if not self.path or self.checkIfNearMonster(self, 5, wrld):
            self.path = self.aStarPath(wrld)
            self.pathIterator = 0
        # if within distance 3 of a monster
        self.pathIterator += 1
        self.move(self.path[self.pathIterator].x - self.x, self.path[self.pathIterator].y - self.y)
        return

    def checkIfNearMonster(self, node, range, wrld):
        # TODO account for walls and bombs
        for key, monsterlist in wrld.monsters.items():
            for monster in monsterlist:
                if (monster.x - range < node.x < monster.x + range) \
                        and (monster.y - range < node.y < monster.y + range):
                    return True
        return False

    def aStarPath(self, wrld):
        openNodes = []
        closedNodes = []
        # End node is position 7, 18
        endNode = Node(7, 18)
        startNode = Node(self.x, self.y)

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

            for neighbor in self.getNeighbors(minNode, wrld):
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
                    neighbor.hval = self.distanceBetweenNodes(neighbor, endNode, wrld)
                    neighbor.fval = neighbor.gval + neighbor.hval

                    if isOpen and neighbor.fval < sameNode.fval:
                        openNodes[nodeIndex] = neighbor

                    elif not isOpen:
                        openNodes.append(neighbor)

            # for node in self.getNeighbors(currNode, wrld):
            #     currCost = self.distanceBetweenNodes(node, startNode) + self.distanceBetweenNodes(node, endNode)
            #     #if the cost isn't here or
            #     if currCost not in costs or currCost < costs[node]:
            #         costs[node] = currCost
            #         heapVal = currCost
            #         path[node] = currNode

    # code taken from selfpreserving_monster.py
    def getNeighbors(self, node, wrld):
        listOfNeighbors = []
        # Go through neighboring cells
        for dx in [-1, 0, 1]:
            # Avoid out-of-bounds access
            if (node.x + dx >= 0) and (node.x + dx < wrld.width()):
                for dy in [-1, 0, 1]:
                    # Avoid out-of-bounds access
                    if (node.y + dy >= 0) and (node.y + dy < wrld.height()):
                        # Is this cell safe?
                        if (wrld.exit_at(node.x + dx, node.y + dy) or
                                wrld.empty_at(node.x + dx, node.y + dy)):
                            if not (dx == 0 and dy == 0):
                                listOfNeighbors.append(Node(node.x + dx, node.y + dy, parent=node))
        # All done
        return listOfNeighbors

    # absolute distance between two nodes
    def distanceBetweenNodes(self, currNode, endNode, wrld):
        xDistance = abs(endNode.x - currNode.x)
        yDistance = abs(endNode.y - currNode.y)

        # if the node is close to any monster, try to avoid it
        for i in range(1, 5):
            if self.checkIfNearMonster(currNode, i, wrld):
                return max(xDistance, yDistance) + 500 - i * 100

        # moving diagonally is one move so can combine x and y distance
        return max(xDistance, yDistance)
