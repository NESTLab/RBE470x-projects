# This is necessary to find the main code
import sys
import math

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back


class TestCharacter(CharacterEntity):
    def do(self, wrld):
        ex = self.find_exit(wrld)
        # A*
        frontier = []
        frontier.append(((self.x, self.y), 0))
        came_from = {}
        cost_so_far = {}
        came_from[(self.x, self.y)] = None
        cost_so_far[(self.x, self.y)] = 0
        move = 1
        print("SELFX " + str(self.x))
        print("SELFY " + str(self.y))

        while not len(frontier) == 0:
            frontier.sort(key=lambda tup: tup[1])  # check that
            current = frontier.pop(0)
            if (current[0][0], current[0][1]) == ex:
                break
            for next in get_adjacent(current[0], wrld):
                if wrld.wall_at(next[0], next[1]):
                    cost_so_far[(next[0], next[1])] = 999
                    new_cost = 1000
                else:
                    new_cost = self.cost_to(current[0], next) + cost_so_far[current[0]]
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    frontier.append((next, new_cost + self.manhattan_distance(next[0], next[1], ex[0], ex[1])))
                    came_from[next] = current[0]

        self.printOurWorld(wrld, cost_so_far)

        cursor = ex
        path = []
        while not cursor == (self.x, self.y):
            move = cursor
            path.append(cursor)
            cursor = came_from[cursor]
        print(move)

        # carries momentum? mayhaps not the best
        self.move(move[0] - self.x, move[1] - self.y)
        pass

    def calculateMove(self, wrld):
        xcoord = self.x
        ycoord = self.x

    def manhattan_distance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    # Prioritizes downward
    def cost_to(self, current, next):
        diff = (next[0] - current[0], next[1] - current[1])
        val = abs(diff[0]) + abs(diff[1])
        if val == 2:
            return 2
        else:
            return 1

    # This is probably unnecessary, assuming all scenarios remain as provided, but good to double check!
    def find_exit(self, wrld):
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.exit_at(x, y):
                    return (x, y)

    def printOurWorld(self, wrld, cost_so_far):
        w, h = len(wrld.grid), len(wrld.grid[0])
        print('\n\n')
        world = [[0 for x in range(w)] for y in range(h)]

        # for row in world:
        #     print(row)
        keys = cost_so_far.keys()

        for key in keys:
            # x,y = val[0][0], val[0][1]
            # print(x, y)
            # print("Set value at " + str(val[0][0]-1) + " , " + str(val[0][1] -1) + " to: " + str(val[1]) )

            k = str(key).split(',')

            world[key[1]][key[0]] = "{0:03d}".format(cost_so_far[key])
        world[self.y][self.x] = "X"

        for row in world:
            print(row)


# Returns a list of coordinates in the world surrounding the current one.
# param current: An (x, y) point
def get_adjacent(current, wrld):
    # Returns a list of points in the form [(x1, y1), (x2, y2)]
    neighbors = []
    x = current[0]
    y = current[1]

    if x >= 1:
        if y >= 1:
            neighbors.append((x - 1, y - 1))  # top left
        neighbors.append((x - 1, y))  # middle left
        if y < wrld.height() - 1:
            neighbors.append((x - 1, y + 1))  # bottom left

    if y >= 1:
        neighbors.append((x, y - 1))  # top middle
    if y < wrld.height() - 1:
        neighbors.append((x, y + 1))  # bottom middle

    if x < wrld.width() - 1:
        if y >= 1:
            neighbors.append((x + 1, y - 1))  # top right
        neighbors.append((x + 1, y))  # middle right
        if y < wrld.height() - 1:
            neighbors.append((x + 1, y + 1))  # bottom right

    return neighbors


def printFrontier(frontier):
    for val in frontier:
        print(val)


