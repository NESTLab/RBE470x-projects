# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import heapq


class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
        self.move(0,1)
        # shreeja was here something
        # jose attacks

        pass

    @staticmethod
    def get_exit(wrld):
        x1 = -1
        y1 = -1
        # Find the exit to use for heuristic A*
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.exit_at(x, y):
                    x1 = x
                    y1 = y
        if x1 == -1:
            return -1
        return x1, y1

    # @staticmethod
    # def make_graph(wrld):
    #     graph_wrld = [wrld.width][wrld.height]
    #
    #     for i in range(0, wrld.width):
    #         for j in range(0, wrld.height):
    #             if wrld(i, j)

    # Determining the heuristic value, being Euclidean Distance
    @staticmethod
    def heuristic(start, goal):
        (x1, y1) = start
        (x2, y2) = goal

        # Euclidean distance is the hypotenuse
        # We add the squared values, and finding the sqrt is
        # not necessary as it will never effect the outcome
        value = (x1 + x2)**2 + (y1 + y2)**2
        return value

    def a_star(self, wrld, start, goal):
        frontier = heapq()
        frontier.push(start, 0)
        came_from = {}
        cumulative_cost = {}
        came_from[start] = None
        cumulative_cost[start] = 0

        while not frontier.empty():
            current = frontier.pop()

            if current == goal:
                break

            # NEED WAY TO FIND NEIGHBORS
            for neighbor in graphNEIGHBORS(current):
                cost = cumulative_cost[current] + COST[current, neighbor]
                if neighbor not in cumulative_cost or cost < cumulative_cost[neighbor]:
                    cumulative_cost[neighbor] = cost
                    priority = cost + self.heuristic(neighbor, goal)
                    frontier.push(neighbor, priority)
                    came_from[neighbor] = current

        return came_from, cumulative_cost
