# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
import math


# this version of monster is used to determine the type of monster when it is supposed to be hidden (see readme)
class Monster:
    def __init__(self, x, y):
        self.prevX = x
        self.prevY = y
        self.x = x
        self.y = y
        self.velocityX = None
        self.velocityY = None

        self.timesIActedSmart = 0
        self.type = None
        self.path = []

    def getPath(self, wrld):
        self.checkVelocity(wrld)
        path = [Node(self.x, self.y)]
        isOutOfBounds = False
        i = 1
        while not isOutOfBounds:
            (nx, ny) = (self.prevX + self.velocityX*i, self.prevY + self.velocityY*i)
            # If next pos is out of bounds, must change direction
            if ((nx < 0) or (nx >= wrld.width()) or
                    (ny < 0) or (ny >= wrld.height())):
                isOutOfBounds = True
            else:
                path.append(Node(self.x + self.velocityX*i, self.y + self.velocityY*i))
                i += 1
        return path

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
        elif self.timesIActedSmart < 5:
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
    def __init__(self, name, avatar, x, y, shouldPanic, distanceStupid, distanceSmart):
        super().__init__(name, avatar, x, y)
        self.monsters = []
        # TODO keep track of all bombs, unnecessary rn because we have our own
        self.path = []
        self.bombTimer = 0
        self.explosionTimer = 0
        self.placeBombAtEnd = False
        self.pathIterator = -1
        self.distanceFromExit = 0
        self.shoudPanic = shouldPanic
        self.distanceStupid = distanceStupid
        self.distanceSmart = distanceSmart
        self.panicCounter = 0

    def do(self, wrld):
        ispanicking = False
        # recalculate the AStar path and distance from exit every time
        self.distanceFromExit = self.distanceBetweenNodes(Node(self.x, self.y), Node(7,18), False)
        self.calculateCharacterPath(Node(7, 18), wrld, True)
        self.pathIterator = 0

        if self.shoudPanic and self.panicCounter > 3 and len(wrld.bombs.items()) == 0:
            self.placeBombAtEnd = True
            self.panicCounter = 0

        if self.explosionTimer > 0:
            self.explosionTimer -= 1

        if self.bombTimer > 0:
            self.bombTimer -= 1
            if self.bombTimer == 0:
                self.explosionTimer = wrld.expl_duration

        for bomb in wrld.bombs.items():
            if self.explosionTimer < 8:
                self.runAway(6, wrld)

        if len(self.path) == 1:
            self.runAway(6, wrld)

        if not self.monsters or len(self.monsters) != len(wrld.monsters.items()):
            self.monsters = []
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
                monster.checkVelocity(wrld)

        if self.placeBombAtEnd:
            self.place_bomb()
            self.bombTimer = wrld.bomb_time
            self.runAway(6, wrld)
            self.placeBombAtEnd = False

        if self.checkIfNearMonster(self, wrld):
            self.panicCounter += 1
            ispanicking = True

            # if my path ends at the exit
            selfIsCloserToExitThanMonster = True
            myPathToExit = self.calculateAStarPath(self, Node(7, 18), wrld, False)

            # if there isn't currently a path to the exit
            if not myPathToExit[0]:
                selfIsCloserToExitThanMonster = False

            else:
                for key, monsterlist in wrld.monsters.items():
                    for monster in monsterlist:
                        if len(myPathToExit[1]) >= len(self.calculateAStarPath(monster, Node(7, 18), wrld, False)[1]):
                            selfIsCloserToExitThanMonster = False
                            break

            if not selfIsCloserToExitThanMonster:
                # pick the spot out of the 8 cardinal directions that is least near to a monster.
                self.runAway(6, wrld)
            else:
                self.calculateCharacterPath(Node(7, 18), wrld, False)

        if not ispanicking and self.panicCounter > 0:
            self.panicCounter -= 1
        self.pathIterator += 1
        self.move(self.path[self.pathIterator].x - self.x, self.path[self.pathIterator].y - self.y)
        return

    def checkIfNearMonster(self, node, wrld):
        for monster in self.monsters:
            # if SelfPreservingMonster (smart) monster is within <maxDistance> steps, return true
            pathBetweenSelfAndMonster = self.calculateAStarPath(node, monster, wrld, False)

            # if there is path between myself and the monster
            if pathBetweenSelfAndMonster[0]:
                distance = len(pathBetweenSelfAndMonster[1])
                if monster.type is not None and monster.type == "smart" and distance - 1 < self.distanceSmart:
                    return True

                elif distance - 1 < self.distanceStupid:
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
        highestSum = -math.inf

        neighbors = self.getNeighbors(self, Node(7, 18), wrld)
        neighbors.append(Node(self.x, self.y))
        # iterate over the available spots of the eight cardinal directions
        for node in neighbors:
            # put the node farthest from the available locations
            currSum = 0

            # if there's an explosion, don't add
            if wrld.explosion_at(node.x, node.y):
                continue

            shouldContinue = False

            # TODO account for other players bombs
            # only bomb is ours:
            for k, bomb in wrld.bombs.items():
                if self.bombTimer <= 2:
                    # avoid the tiles in the x and y direction
                    bombRange = wrld.expl_range
                    for x in range(-bombRange, bombRange):
                        if node.x == bomb.x + x and node.y == bomb.y:
                            shouldContinue = True
                            break

                    for y in range(-bombRange, bombRange):
                        if node.x == bomb.x and node.y == bomb.y + y:
                            shouldContinue = True
                            break

            if shouldContinue:
                continue

            # for monster in monsterlist:
            for monster in self.monsters:
                pathBetweenSelfAndMonster = self.calculateAStarPath(node, monster, wrld, False)
                myDistance = len(self.calculateAStarPath(self, monster, wrld, False)[1])
                # if there is a path between myself and the monster
                if pathBetweenSelfAndMonster[0]:
                    distance = len(pathBetweenSelfAndMonster[1])
                    if myDistance < self.distanceSmart and monster.type == "smart":
                        if distance < (self.distanceSmart - 1):
                            # try very hard not to get into detection range
                            currSum -= 5
                        elif distance < (self.distanceSmart - 2):
                            currSum -= 10

                        # monsterPath = monster.getPath(wrld)
                        # for monsterNode in monsterPath:
                        #     if monsterNode.x == node.x and monsterNode.y == node.y:
                        #         currSum -= 3
                        #     break

                        currSum += distance
                    elif myDistance < self.distanceStupid:
                        currSum += distance

            if highestSum + 2 <= currSum <= highestSum - 2:
                possibleNodes.append(node)
            elif currSum > highestSum:
                highestSum = currSum
                possibleNodes = [node]

        pathToStart = (self.calculateAStarPath(self, Node(0, 0), wrld, True))[1]
        self.calculateCharacterPath(Node(7, 18), wrld, True)
        if not possibleNodes:
            # accept death.
            self.path = [Node(self.x, self.y), Node(self.x, self.y)]
            return

        firstNode = possibleNodes[0]
        # append possible nodes
        for node in possibleNodes:
            # if node is in the path to the end
            if len(self.path) > 1 and self.path[1].x == node.x and self.path[1].y == node.y:
                path.append(node)
                break

            # if node is in the path to the start
            if len(pathToStart) > 1 and pathToStart[1].x == node.x and pathToStart[1].y == node.y:
                path.append(node)
                break

        # if no node was added before, just add the first node
        if len(path) == 1:
            path.append(firstNode)
        self.path = path

    # return the character's path to the end
    def calculateCharacterPath(self, endNode, wrld, shouldPathAroundMonsters):
        startNode = Node(self.x, self.y)
        path = self.calculateAStarPath(startNode, endNode, wrld, shouldPathAroundMonsters)

        if path[0]:
            self.path = path[1]
        else:
            # if I can't find the exit after searching all possible nodes, I should find the node closest to the exit.
            #   > Also, flag that spot for bombing
            minNode = startNode
            minNode.hval = math.inf
            for node in path[1]:
                node.hval = self.absoluteDistanceBetweenNodes(node, endNode)
                if node.hval < minNode.hval:
                    minNode = node

            if self.absoluteDistanceBetweenNodes(minNode, endNode) == self.absoluteDistanceBetweenNodes(self, endNode) and self.bombTimer == 0:
                self.placeBombAtEnd = True

            else:
                self.calculateCharacterPath(minNode, wrld, True)


    # take into account walls; if there is a wall in the way, move to it and bomb the heck out of it
    # Returns
    # > Boolean, <Nodes> tuple where Boolean says whether there is a clear path to the end and Nodes returns
    # either the path or the set of closed nodes
    def calculateAStarPath(self, startNode, endNode, wrld, shouldPathAroundMonsters):
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
                return True, path[::-1]
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
                    neighbor.hval = self.distanceBetweenNodes(neighbor, endNode, shouldPathAroundMonsters)
                    neighbor.fval = neighbor.gval + neighbor.hval

                    if isOpen and neighbor.fval < sameNode.fval:
                        openNodes[nodeIndex] = neighbor

                    elif not isOpen:
                        openNodes.append(neighbor)
        return False, closedNodes

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
                        # Is this cell an exit, empty or a monster?
                        elif (wrld.exit_at(node.x + dx, node.y + dy) or
                              wrld.empty_at(node.x + dx, node.y + dy) or
                              wrld.monsters_at(node.x + dx, node.y + dy)):
                            if not (dx == 0 and dy == 0):
                                listOfNeighbors.append(Node(node.x + dx, node.y + dy, parent=node))
        # All done
        return listOfNeighbors

    # absolute distance between nodes
    def absoluteDistanceBetweenNodes(self, currNode, endNode):
        xDistance = abs(endNode.x - currNode.x)
        yDistance = abs(endNode.y - currNode.y)

        return xDistance + yDistance


    # distance between two nodes
    def distanceBetweenNodes(self, currNode, endNode, shouldPathAroundMonsters):
        xDistance = abs(endNode.x - currNode.x)
        yDistance = abs(endNode.y - currNode.y)

        # if the node is close to any monster and the endnode is not a monster, try to avoid it

        if shouldPathAroundMonsters:
            for i in range(0, 4):
                for monster in self.monsters:
                    if monster.type == 'stupid' and i < 3:
                        if (monster.x - i <= currNode.x <= monster.x + i) \
                                and (monster.y - i <= currNode.y <= monster.y + i):
                            return max(xDistance, yDistance) + 300 - i * 100

                    else:
                        if (monster.x - i <= currNode.x <= monster.x + i) \
                                and (monster.y - i <= currNode.y <= monster.y + i):
                            return max(xDistance, yDistance) + 300 - i * 100

        # moving diagonally is one move so can combine x and y distance
        return max(xDistance, yDistance)
