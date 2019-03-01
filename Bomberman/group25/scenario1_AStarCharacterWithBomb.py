# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
import math
import customEntities
import astar

class TestCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y, shouldPanic, distanceStupid, distanceSmart):
        super().__init__(name, avatar, x, y)
        self.monsters = []
        # TODO keep track of all bombs, unnecessary rn because we have our own
        self.path = []
        self.bombTimer = 0
        self.explosionTimer = 0
        self.placeBombAtEnd = True
        self.pathIterator = -1
        self.distanceFromExit = 0
        self.shouldPanic = shouldPanic
        self.distanceStupid = distanceStupid
        self.distanceSmart = distanceSmart
        self.panicCounter = 0
        self.numberOfBombsPlaced = -1
        self.bombPosition = None

    def do(self, wrld):
        ispanicking = False
        # recalculate the AStar path and distance from exit every time
        self.distanceFromExit = astar.distanceBetweenNodes(customEntities.Node(self.x, self.y), customEntities.Node(7, 18), self.monsters, False)
        self.calculateCharacterPath(customEntities.Node(7, 18), wrld, True)
        self.pathIterator = 0

        if self.bombTimer == 0 and self.explosionTimer > 0:
            self.explosionTimer -= 1
            if self.explosionTimer == 0:
                self.bombPosition = None

        if self.bombTimer > 0:
            self.bombTimer -= 1
            if self.bombTimer == 0:
                self.numberOfBombsPlaced += 1
                self.explosionTimer = wrld.expl_duration + 2

        for bomb in wrld.bombs.items():
            if self.bombTimer <= 2:
                self.runAway(wrld)

        if len(self.path) == 1:
            self.runAway(wrld)

        if not self.monsters or len(self.monsters) != len(wrld.monsters.items()):
            self.monsters = []
            for key, monsterlist in wrld.monsters.items():
                for monster in monsterlist:
                    self.monsters.append(customEntities.Monster(monster.x, monster.y))
        else:
            i = 0
            for key, monsterlist in wrld.monsters.items():
                for monster in monsterlist:
                    self.monsters[i].x = monster.x
                    self.monsters[i].y = monster.y
                i += 1
            for monster in self.monsters:
                monster.checkVelocity(wrld)

        if self.checkIfNearMonster(self, wrld):
            self.panicCounter += 1
            ispanicking = True

            # if my path ends at the exit
            selfIsCloserToExitThanMonster = True
            myPathToExit = astar.calculateAStarPath(self, customEntities.Node(7, 18), wrld, self.monsters, False)

            # if there isn't currently a path to the exit
            if not myPathToExit[0]:
                selfIsCloserToExitThanMonster = False

            else:
                for key, monsterlist in wrld.monsters.items():
                    for monster in monsterlist:
                        if len(myPathToExit[1]) >= len(astar.calculateAStarPath(monster, customEntities.Node(7, 18), wrld, self.monsters, False)[1]):
                            selfIsCloserToExitThanMonster = False
                            break

            if self.shouldPanic and len(wrld.bombs.items()) == 0:
                self.placeBombAtEnd = True
                self.panicCounter = 0

            elif not selfIsCloserToExitThanMonster:
                # pick the spot out of the 8 cardinal directions that is least near to a monster.
                self.runAway(wrld)

            else:
                self.calculateCharacterPath(customEntities.Node(7, 18), wrld, False)

        if self.placeBombAtEnd:
            self.bombPosition = customEntities.Node(self.x, self.y)
            self.place_bomb()
            self.bombTimer = wrld.bomb_time
            self.runAway(wrld)
            self.placeBombAtEnd = False

        if not ispanicking and self.panicCounter > 0:
            self.panicCounter -= 1
        self.pathIterator += 1
        self.move(self.path[self.pathIterator].x - self.x, self.path[self.pathIterator].y - self.y)
        return

    def checkIfNearMonster(self, node, wrld):
        for monster in self.monsters:
            # if SelfPreservingMonster (smart) monster is within <maxDistance> steps, return true
            pathBetweenSelfAndMonster = astar.calculateAStarPath(node, monster, wrld, self.monsters, False)

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

    # TODO Implement alpha beta search to try to run away faster
    def runAway(self, wrld):
        # put current position into the path
        path = [customEntities.Node(self.x, self.y)]
        possibleNodes = []
        shouldRun = False

        # start by setting the lowest sum to infinity
        highestSum = -math.inf

        # get the set of neighbors, including ourself
        neighbors = astar.getNeighbors(self, customEntities.Node(7, 18), wrld)
        neighbors.append(customEntities.Node(self.x, self.y))

        # iterate over the available spots of the eight cardinal directions
        for node in neighbors:
            currSum = 0

            # if there's an explosion, don't add
            if wrld.explosion_at(node.x, node.y):
                continue

            shouldContinue = False

            # TODO account for other players bombs
            # do not include the nodes that would be in bomb's path of explosion
            if self.bombTimer <= 2 and self.bombPosition is not None:
                bombRange = wrld.expl_range
                for x in range(-bombRange - 1, bombRange + 1):
                    if node.x == self.bombPosition.x + x and node.y == self.bombPosition.y:
                        shouldContinue = True
                        break

                for y in range(-bombRange - 1, bombRange + 1):
                    if node.x == self.bombPosition.x and node.y == self.bombPosition.y + y:
                        shouldContinue = True
                        break
            if shouldContinue:
                continue

            node.hval = math.inf
            # for monster in monsterlist:
            for monster in self.monsters:
                pathBetweenSelfAndMonster = astar.calculateAStarPath(node, monster, wrld, self.monsters, False)
                myDistance = len(astar.calculateAStarPath(self, monster, wrld, self.monsters, False)[1])


                # if there is a path between myself and the monster
                if pathBetweenSelfAndMonster[0]:
                    distance = len(pathBetweenSelfAndMonster[1])
                    # distance = self.distanceBetweenNodes(node, monster, False)
                    if myDistance < self.distanceSmart and monster.type == "smart":
                        if distance < (self.distanceSmart - 1):
                            # try very hard not to get into detection range
                            currSum -= 5

                        elif distance < (self.distanceSmart - 2):
                            currSum -= 10
                            shouldRun = True

                        currSum += distance
                        node.hval = astar.absoluteDistanceBetweenNodes(node, monster)

                    elif myDistance < self.distanceStupid + 1:
                        currSum += distance
                        if distance < self.distanceStupid:
                            shouldRun = True

            if currSum == highestSum:
                possibleNodes.append(node)

            elif currSum > highestSum:
                highestSum = currSum
                possibleNodes = [node]

        pathToStart = (astar.calculateAStarPath(self, customEntities.Node(4, 8), wrld, self.monsters, True))[1]
        self.calculateCharacterPath(customEntities.Node(7, 18), wrld, True)
        if not possibleNodes:
            # accept death.
            self.path = [customEntities.Node(self.x, self.y), customEntities.Node(self.x, self.y)]
            return

        bestNode = None
        highestSum = -math.inf

        if shouldRun:
            for node in possibleNodes:
                if node.hval > highestSum:
                    bestNode = node
                    highestSum = node.hval

        if bestNode is None:
            # append possible nodes
            for node in possibleNodes:
                # if node is in the path to the end
                if len(self.path) > 1 and self.path[1].x == node.x and self.path[1].y == node.y:
                    bestNode = node
                    break

        if bestNode is None:
            for node in possibleNodes:
                # if node is in the path to the start
                if len(pathToStart) > 1 and pathToStart[1].x == node.x and pathToStart[1].y == node.y:
                    bestNode = node
                    break

        # if no node was added before, just add the first node
        if bestNode is not None:
            path.append(bestNode)
        else:
            path.append(possibleNodes[0])
        self.path = path

    # return the character's path to the end
    def calculateCharacterPath(self, endNode, wrld, shouldPathAroundMonsters):
        startNode = customEntities.Node(self.x, self.y)
        path = astar.calculateAStarPath(startNode, endNode, wrld, self.monsters, shouldPathAroundMonsters)

        if path[0]:
            self.path = path[1]
        else:
            # if I can't find the exit after searching all possible nodes, I should find the node closest to the exit.
            #   > Also, flag that spot for bombing
            minNode = startNode
            minNode.hval = math.inf
            for node in path[1]:
                node.hval = astar.absoluteDistanceBetweenNodes(node, endNode)
                if node.hval < minNode.hval:
                    minNode = node

            if astar.absoluteDistanceBetweenNodes(minNode, endNode) == astar.absoluteDistanceBetweenNodes(self, endNode) \
                and self.bombTimer == 0 and len(wrld.explosions.items()) == 0:
                self.placeBombAtEnd = True

            else:
                self.calculateCharacterPath(minNode, wrld, True)
