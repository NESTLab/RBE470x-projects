# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
# Imports for code implementation
from queue import PriorityQueue
import math

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here

        # Prints the current position of the character after the character moves
        print(self.x, self.y)

        # Find the start (current position) and goal
        start = (self.x, self.y)
        goal = self.findGoal(wrld)

        # Get all possible directions fro agent
        allDirections = self.getAllDirections(wrld, start)

        # Find the current best move for the agent
        bestScoreMove = self.scoreMoves(wrld, start, goal, allDirections)
        self.move(bestScoreMove[0], bestScoreMove[1])

        # Go to the goal state if the path leads to a space next to it. ie Terminal Test
        self.goToGoal(start, goal)

        pass

    # Chooses the best direction to go in based on heuristics
    #
    # PARAM: [ world, [int, int], (int, int)]: wrld: the current state of the world
    #                                          [start.x, start.y]: the x and y coordinated the agent is located at
    #                                          [goal.x, goal.y]: the x and y coordinated of the goal / exit
    #                                          allDirections: a list of all the directions the agent can go
    #
    # RETRUNS: the best move for the agent
    #
    def scoreMoves(self, wrld, start, goal, allDirections):
        enemies = self.getEnemy(wrld)

        # Gets the move recommended by A*
        a_star_move = self.get_a_star_move(wrld, start, goal)

        bestMove = -1
        highestScore = -1
        for i in range(len(allDirections)):
            livingScore = abs(wrld.time)

            enemyScore = 0
            for enemyLoc in enemies:
                futureX = (self.x + allDirections[i][0])
                futureY = (self.y + allDirections[i][1])

                enemyDis = math.sqrt((enemyLoc[0] - futureX) ** 2 + (enemyLoc[1] - futureY) ** 2)
                if(enemyDis < 4):
                    enemyScore = enemyScore - ((4 - enemyDis) * 3)

            a_star_score = 0
            if(a_star_move == allDirections[i]):
                a_star_score = 5

            totalScore = livingScore + a_star_score + enemyScore
            print(totalScore)
            if(totalScore > highestScore):
                highestScore = totalScore
                bestMove = allDirections[i]

        return bestMove


    # Gets the locations of the enemies location
    #
    # PARAM: [world] wrld: the current state of the world
    #
    # RETURNS: [list [entities]] enemies: a list of enemies
    #
    def getEnemy(self, wrld):
        enemies = []

        x = 0
        y = 0
        for y in range(wrld.height()):
            for x in range(wrld.width()):
                if(wrld.monsters_at(x, y)):
                    enemies.append((x, y))

        return enemies


    # Goes to the goal / exit
    #
    # PARAM: [[int, int], [int, int]]: [start.x, start.y]: the x and y coordinated the agent is located at
    #                                  [goal.x, goal.y]: the x and y coordinated of the goal / exit
    # RETURNS: [int, int] x, y: the x and y coordinates of the direction the of the goal
    #
    def goToGoal(self, start, goal):
        # Move Vertical Down
        if start == (goal[0], goal[1] - 1):
            return self.move(0, 1)
        # Move Vertical Up
        elif start == (goal[0], goal[1] + 1):
            return self.move(0, -1)
        # Move Horizontal Right
        elif start == (goal[0] - 1, goal[1]):
            return self.move(1, 0)
        # Move Horizontal Left
        elif start == (goal[0] + 1, goal[1]):
            return self.move(-1, 0)
        # Move Diagonal Right-Down
        elif start == (goal[0] - 1, goal[1] - 1):
            return self.move(1, 1)
        # Move Diagonal Right-Up
        elif start == (goal[0] - 1, goal[1] + 1):
            return self.move(1, -1)
        # Move Diagonal Left-Down
        elif start == (goal[0] + 1, goal[1] - 1):
            return self.move(-1, 1)
        # Move Diagonal Left-Up
        elif start == (goal[0] - 1, goal[1] - 1):
            return self.move(-1, -1)

    # Finds the goal / exit to the world
    #
    # PARAM: [world] wrld: the current world configuration
    # RETURNS: [int, int] x, y: the x and y coordinates of the goal / exit
    #
    def findGoal(self, wrld):
        x = 0
        y = 0
        for y in range(wrld.height()):
            for x in range(wrld.width()):
                if(wrld.exit_at(x,y)):
                    print(x,y)
                    return (x,y)

        # Return impossible exit coordinate to signal no exit found
        print('No Exit Found')
        return (-1,-1)

    # Returns a world with the A* path marked
    #
    # PARAM: [world, [int, int], [int, int]] wrld: the current world configuration
    #                                       [start.x, start.y]: the x and y coordinated the agent is located at
    #                                       [goal.x, goal.y]: the x and y coordinated of the goal / exit
    # RETURNS: [world] newWrld: a grid world marking the A* path to the goal
    #
    def a_star_search(self, wrld, start, goal):

        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in self.getAllSpaces(wrld, current):
                new_cost = cost_so_far[current] + 1 # + graph.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.a_star_heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

        return came_from, cost_so_far


    # Returns a heuristic value to influence agent movement
    #
    # PARAM: [goal.x, goal.y] goal: the x and y location of the goal
    #        [start.x, start.y] current: the x and y coordinated the agent is located at
    # RETURNS: [int] distance: distance between the current agent location and the goal
    #
    def a_star_heuristic(self, goal, next):
        return abs(goal[0] - next[0]) + abs(goal[1] - next[1])

    # Returns list of all the possible moves for agent (up, down, left, right, diagonal)
    #
    # PARAM: [world, [int, int]] wrld: the current world configuration
    #        [start.x, start.y] currentLocation: the x and y coordinated the agent is located at
    # RETURNS: [list [int, int]] allMoves: a list of all the possible moves for agent
    #
    def getAllSpaces(self, wrld, currentLocation):
        movesList = []

        # Look right
        # Avoid out of bound look ups
        if((currentLocation[0] + 1) < wrld.width()):
            if(wrld.empty_at(currentLocation[0] + 1, currentLocation[1])):
                movesList.append((currentLocation[0] + 1, currentLocation[1]))
        # Look left
        # Avoid out of bound look ups
        if ((currentLocation[0] - 1) >= 0):
            if (wrld.empty_at(currentLocation[0] - 1, currentLocation[1])):
                movesList.append((currentLocation[0] - 1, currentLocation[1]))
        # Look down
        # Avoid out of bound look ups
        if ((currentLocation[1] - 1) >= 0):
            if (wrld.empty_at(currentLocation[0], currentLocation[1] - 1)):
                movesList.append((currentLocation[0], currentLocation[1] - 1))
        # Look up
        # Avoid out of bound look ups
        if ((currentLocation[1] + 1) < wrld.height()):
            if (wrld.empty_at(currentLocation[0], currentLocation[1] + 1)):
                movesList.append((currentLocation[0], currentLocation[1] + 1))
        # Look diagonal right, up
        # Avoid out of bound look ups
        if ((currentLocation[0] + 1) < wrld.width() and (currentLocation[1] + 1) < wrld.height()):
            if (wrld.empty_at(currentLocation[0] + 1, currentLocation[1] + 1)):
                movesList.append((currentLocation[0] + 1, currentLocation[1] + 1))
        # Look diagonal right, down
        # Avoid out of bound look ups
        if ((currentLocation[0] + 1) < wrld.width() and (currentLocation[1] - 1) >= 0):
            if (wrld.empty_at(currentLocation[0] + 1, currentLocation[1] - 1)):
                movesList.append((currentLocation[0] + 1, currentLocation[1] - 1))
        # Look diagonal left, up
        # Avoid out of bound look ups
        if ((currentLocation[0] - 1) >= 0 and (currentLocation[1] + 1) < wrld.height()):
            if (wrld.empty_at(currentLocation[0] - 1, currentLocation[1] + 1)):
                movesList.append((currentLocation[0] - 1, currentLocation[1] + 1))
        # Look diagonal left, down
        # Avoid out of bound look ups
        if ((currentLocation[0] - 1) >= 0 and (currentLocation[1] - 1) >= 0):
            if (wrld.empty_at(currentLocation[0] - 1, currentLocation[1] - 1)):
                movesList.append((currentLocation[0] - 1, currentLocation[1] - 1))

        return movesList

    # Returns list of all the possible directions for agent (up, down, left, right, diagonal)
    #
    # PARAM: [world, [int, int]] wrld: the current world configuration
    #        [start.x, start.y] currentLocation: the x and y coordinated the agent is located at
    # RETURNS: [list [int, int]] allMoves: a list of all the possible moves for agent
    #
    def getAllDirections(self, wrld, currentLocation):
        directionList = []

        # Look right
        # Avoid out of bound look ups
        if ((currentLocation[0] + 1) < wrld.width()):
            if (wrld.empty_at(currentLocation[0] + 1, currentLocation[1])):
                directionList.append((1, 0))
        # Look left
        # Avoid out of bound look ups
        if ((currentLocation[0] - 1) >= 0):
            if (wrld.empty_at(currentLocation[0] - 1, currentLocation[1])):
                directionList.append((-1, 0))
        # Look down
        # Avoid out of bound look ups
        if ((currentLocation[1] - 1) >= 0):
            if (wrld.empty_at(currentLocation[0], currentLocation[1] - 1)):
                directionList.append((0, -1))
        # Look up
        # Avoid out of bound look ups
        if ((currentLocation[1] + 1) < wrld.height()):
            if (wrld.empty_at(currentLocation[0], currentLocation[1] + 1)):
                directionList.append((0, 1))
        # Look diagonal right, up
        # Avoid out of bound look ups
        if ((currentLocation[0] + 1) < wrld.width() and (currentLocation[1] + 1) < wrld.height()):
            if (wrld.empty_at(currentLocation[0] + 1, currentLocation[1] + 1)):
                directionList.append((1, 1))
        # Look diagonal right, down
        # Avoid out of bound look ups
        if ((currentLocation[0] + 1) < wrld.width() and (currentLocation[1] - 1) >= 0):
            if (wrld.empty_at(currentLocation[0] + 1, currentLocation[1] - 1)):
                directionList.append((1, -1))
        # Look diagonal left, up
        # Avoid out of bound look ups
        if ((currentLocation[0] - 1) >= 0 and (currentLocation[1] + 1) < wrld.height()):
            if (wrld.empty_at(currentLocation[0] - 1, currentLocation[1] + 1)):
                directionList.append((-1, 1))
        # Look diagonal left, down
        # Avoid out of bound look ups
        if ((currentLocation[0] - 1) >= 0 and (currentLocation[1] - 1) >= 0):
            if (wrld.empty_at(currentLocation[0] - 1, currentLocation[1] - 1)):
                directionList.append((-1, -1))

        return directionList


    # Finds the A* path to the goal
    #
    # PARAM: [start.x, start.y] currentLocation: the x and y coordinated the agent is located at
    #        [world] wrld: the current world configuration
    #        [world] a_star_grpah: a graph representing the a_star path fro the agent
    # RETURNS: [list [int, int]] path: a list of the path to the goal
    #
    def findPath(self, start, goal, wrld, a_star_graph):
        path = []
        lastMove = []

        possibleGoalEnds = self.getAllSpaces(wrld, goal)
        for endMove in possibleGoalEnds:
            for next in a_star_graph[1]:
                if (next == endMove):
                    lastMove = endMove

        path.append(lastMove)

        while (lastMove != start):
            for next in a_star_graph[0]:
                if(next == a_star_graph[0][lastMove]):
                    lastMove = next
                    path.append(lastMove)

        return path


    # Returns the move recommended by a*
    #
    # PARAM: [world, [int, int], [int, int]] wrld: the current world configuration
    #                                       [start.x, start.y]: the x and y coordinated the agent is located at
    #                                       [goal.x, goal.y]: the x and y coordinated of the goal / exit
    #
    # RETURNS: [int, int]: a_star_move: the move recommended by a*
    #
    def get_a_star_move(self, wrld, start, goal):
        a_star_path = self.a_star_search(wrld, start, goal)

        direction = self.findPath(start, goal, wrld, a_star_path)

        nextMove = direction[len(direction) - 2]
        a_star_move = (nextMove[0] - self.x, nextMove[1] - self.y)
        return a_star_move
