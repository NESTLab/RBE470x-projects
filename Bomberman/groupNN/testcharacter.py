# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
# Imports for code implementation
from queue import PriorityQueue

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here

        self.move(1, 0)

        # Prints the current position of the character after the character moves
        print(self.x, self.y)

        # Find the start (current position) and goal
        start = (self.x, self.y)
        goal = self.findGoal(wrld)

        a_star_path = self.a_star_search(wrld, start, goal)

        pass


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

        print(self.getAllMoves(wrld, start))
        # frontier = PriorityQueue()
        # frontier.put(start, 0)
        # came_from = {}
        # cost_so_far = {}
        # came_from[start] = None
        # cost_so_far[start] = 0
        #
        # while not frontier.empty():
        #     current = frontier.get()
        #
        #     if current == goal:
        #         break
        #
        #     for next in self.getAllMoves(wrld, current):
        #         new_cost = cost_so_far[current] + wrld.cost(current, next)
        #         if next not in cost_so_far or new_cost < cost_so_far[next]:
        #             cost_so_far[next] = new_cost
        #             priority = new_cost
        #             frontier.put(next, priority)
        #             came_from[next] = current
        #
        # return came_from, cost_so_far


    # Returns list of all the possible moves for agent (up, down, left, right)
    #
    # PARAM: [world, [int, int]] wrld: the current world configuration
    #        [start.x, start.y] currentLocation: the x and y coordinated the agent is located at
    # RETURNS: [list [int, int]] allMoves: a list of all the possible moves for agent
    #
    def getAllMoves(self, wrld, currentLocation):
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

        return movesList
