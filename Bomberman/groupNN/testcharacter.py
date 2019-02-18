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
        self.move(1, 1)
        self.get_exit(wrld)
        self.get_my_location(wrld)

    @staticmethod
    def get_exit(wrld):
        # Find the exit to use for heuristic A*
        for x in range(wrld.width()):
            for y in range(wrld.height()):
                if wrld.exit_at(x, y):
                    print(x, y)
                    return x, y
        pass

    # @staticmethod
    # def make_graph(wrld):
    #     graph_wrld = [wrld.width][wrld.height]
    #
    #     for i in range(0, wrld.width):
    #         for j in range(0, wrld.height):
    #             if wrld(i, j)

    # PARAM [tuple (int, int)] start: tuple with x and y coordinates of current position in board
    # PARAM [SensedWorld] wrld: wrld grid, used to get boundries
    # RETURN [list of (int x, int y)]: coordinate positions of neighbors, it doesn't return a neighbor that has a
    def get_neighbors(self, start, wrld):
        x = start[0]
        y = start[1]
        neighbors = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        result = []
        # check that neighbors are inside wrld bounds and are not walls
        for neighbor in neighbors:
            if neighbor[0] >= 0 and neighbor < wrld.height() and neighbor[1] >= 0 and neighbor[1] < wrld.width():
                if wrld.wall_at(neighbor[0], neighbor[1]):
                    result.append(neighbor)
        return result

    def get_my_location(self, wrld):
        # Find the exit to use for heuristic A*
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.characters_at(x, y):
                    print(x, y)
                    return x, y
        pass

    def best_move(self, wrld):
        pass



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
        frontier = heapq() # Priority Queue - How is this implemented?? How to check the value of the nodes. Value comes from optimal path to reach + heuristic
        frontier.push(start, 0) # what is this zero??
        came_from = {}
        cumulative_cost = {}
        came_from[start] = None
        cumulative_cost[start] = 0

        while not frontier.empty():
            current = frontier.pop()

            if current == goal:
                break

            neighbors = self.get_neighbors(start, wrld)

            for neighbor in graphNEIGHBORS(current):
                cost = cumulative_cost[current] + COST[current, neighbor]
                if neighbor not in cumulative_cost or cost < cumulative_cost[neighbor]:
                    cumulative_cost[neighbor] = cost
                    priority = cost + self.heuristic(neighbor, goal)
                    frontier.push(neighbor, priority)
                    came_from[neighbor] = current

        return came_from, cumulative_cost
