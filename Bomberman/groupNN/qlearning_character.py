# This is necessary to find the main code
import sys
import operator

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from entity import AIEntity
from entity import MovableEntity
from colorama import Fore, Back, Style, init
from sensed_world import SensedWorld
from events import Event
init(autoreset=True)

class QCharacter(CharacterEntity):

    def __init__(self, qtable, *args, **kwargs):
        super(QCharacter, self).__init__(*args, **kwargs)
        # Whether this character wants to place a bomb
        self.maybe_place_bomb = False
        # Debugging elements
        self.tiles = {}
        self.qtable = qtable

    def do(self, wrld):
        valid_moves = self.updateQ(wrld)
        print("QTABLE: " + str(self.qtable))
        # path = self.aStar(wrld, (7, 18), True)
        # move = path[len(path) - 1]

        #print("MAX: " + str(max(self.qtable)))

        global bestmove
        bestmove = (0, 0)
        maxval = 0

        print("Valid moves:")
        for m in valid_moves:
            if self.qtable[m] > maxval:
                bestmove = m

        print("BEST:")
        print(bestmove)

        self.move(bestmove[1][0], bestmove[1][1])

        print("Calculated state before moving: ")
        print(self.calculate_state(wrld))
        pass

    def updateQ(self, wrld):
        alpha = 0.3
        possible_moves = []
        moves = get_adjacent((self.x, self.y), wrld)
        for m in moves:
            if not wrld.wall_at(m[0], m[1]):
                sim = SensedWorld.from_world(wrld)  # creates simulated world
                c = sim.me(self)  # finds character from simulated world
                c.move(m[0] - self.x, m[1] - self.y)  # moves character in simulated world
                s = sim.next()  # updates simulated world
                c = s[0].me(c)  # gives us character. this is a tuple, we want the board, not the list of elapsed events

                # Check if game is over
                if c is None:
                    print("ENDED!")
                    print(s[0])
                    print(s[1])
                    print("EVENT 0: ")
                    print(s[1][0])
                    event = s[1][0]
                    if event.tpe == Event.CHARACTER_KILLED_BY_MONSTER and event.character.name == self.name:
                        arg1 = self.calculate_state(wrld)
                        arg2 = (m[0] - self.x, m[1] - self.y)
                        arg3 = 5
                        if (arg1, arg2, arg3) not in self.qtable.keys():
                            self.qtable[arg1, arg2, arg3] = 0
                        self.qtable[arg1, arg2, arg3] = self.qtable[arg1, arg2, arg3] + alpha * -100
                        #self.qtable[self.calculate_state(wrld), 5] = -100
                    elif event.tpe == Event.CHARACTER_FOUND_EXIT and event.character.name == self.name:
                        arg1 = self.calculate_state(wrld)
                        arg2 = (m[0] - self.x, m[1] - self.y)
                        arg3 = 4
                        if (arg1, arg2, arg3) not in self.qtable.keys():
                            self.qtable[arg1, arg2, arg3] = 0
                        self.qtable[arg1, arg2, arg3] = self.qtable[arg1, arg2, arg3] + alpha * 100
                        #self.qtable[self.calculate_state(wrld), 4] = 100  #  We don't really care about move, just state.

                else:
                    print("Xcoord: " + str(c.x) + ", Ycoord: " + str(c.y))
                    self.qtable[(self.calculate_state(wrld), (m[0] - self.x, m[1] - self.y), calculate_state(c, wrld))] = distance_to_exit(c, wrld)
                    possible_moves.append((self.calculate_state(wrld), (m[0] - self.x, m[1] - self.y), calculate_state(c, wrld)))
                    print("Added " + str((self.calculate_state(wrld), (m[0] - self.x, m[1] - self.y), calculate_state(c, wrld))) + " to valid moves")
        return possible_moves

    # Resets styling for each cell. Prevents unexpected/inconsistent behavior that otherwise appears with coloring.
    def reset_cells(self, wrld):
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                self.set_cell_color(x, y, Fore.RESET + Back.RESET)

    def printWorld(self, wrld):
        w, h = len(wrld.grid), len(wrld.grid[0])
        print('\n\n')
        world = [[0 for x in range(w)] for y in range(h)]

        world[self.y][self.x] = "X"

        for row in world:
            print(row)

    # Returns a list of tiles which are occupied by at least 1 monster.
    def monster_tiles(self, wrld):
        tiles = []
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.monsters_at(x, y):
                    tiles.append((x, y))
        return tiles

    # Figures out which state the character is in: safe (0), near monster (1), near bomb (2), near both (3), exited (4)
    # or dead (5).
    def calculate_state(self, wrld):
        if self.closest_monster(wrld) < 2:
            return 1
        else:
            return 0

    # ==================== FEATURES ==================== #
    #   - Distance to closest bomb
    #   - Distance to closest monster
    #   - 1 / (Distance to exit)^2

    # Returns an integer representing the Manhattan distance to the closest bomb.
    def closest_bomb(self):
        return 1  # Will implement this later, in part 2 most likely. For now we don't care about bombs.

    # Returns an integer representing the A* distance to the closest monster.
    def closest_monster(self, wrld):
        monsters = self.monster_tiles(wrld)
        p = float('inf')
        for m in monsters:
            distance = len(self.aStar(wrld, m, False))
            if distance < p:
                p = distance
        return p

    # Returns 1/(A* distance to exit)^2.
    def distance_to_exit(self, wrld):
        return 1 / (len(self.aStar(wrld, wrld.exitcell, True)) ** 2)

    # A* Algorithm
    def aStar(self, wrld, goal, draw):
        # print("SELFX: " + str(self.x))
        # print("SELFY: " + str(self.y))
        frontier = []
        frontier.append(((self.x, self.y), 0))
        came_from = {}
        cost_so_far = {}
        came_from[(self.x, self.y)] = None
        cost_so_far[(self.x, self.y)] = 0

        monsters = []


        while not len(frontier) == 0:
            frontier.sort(key=lambda tup: tup[1])  # check that
            current = frontier.pop(0)
            if draw:
                self.set_cell_color(current[0][0], current[0][1], Fore.RESET + Back.RESET)  # resets color
            if (current[0][0], current[0][1]) == goal:
                break
            for next in self.get_adjacent(current[0], wrld):
                if wrld.wall_at(next[0], next[1]):
                    cost_so_far[(next[0], next[1])] = 999
                    new_cost = 1000
                else:
                    new_cost = cost_to(current[0], next) + cost_so_far[current[0]]
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    frontier.append((next, new_cost + manhattan_distance(next[0], next[1], goal[0], goal[1])))
                    came_from[next] = current[0]

        cursor = goal
        path = []
        while not cursor == (self.x, self.y):
            if draw:
                self.set_cell_color(cursor[0], cursor[1], Fore.RED + Back.GREEN)
            path.append(cursor)
            try:
                cursor = came_from[cursor]
            except KeyError:
                self.move(0, 0)
                pass
                break
        #if draw:
            #print("PATH: ")
            #print(path)

        return path

    # Returns a list of coordinates in the world surrounding the current one.
    # param current: An (x, y) point
    def get_adjacent(self, current, wrld):
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


# ==================== STATIC METHODS ==================== #
# Many of our methods actually need to be static because they need to be applied to different world state objects.

# Calculates manhattan distance between the two sets of coordinates. These could be tuples, but whatever.
def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


# Prioritizes downward
def cost_to(current, next):
    diff = (next[0] - current[0], next[1] - current[1])
    val = abs(diff[0]) + abs(diff[1])
    if val == 2:
        return 2
    else:
        return 1


# Figures out which state the character is in: safe (0), near monster (1), near bomb (2), near both (3), exited (4)
# or dead (5).
def calculate_state(c, wrld):
    x = c.x
    y = c.y
    if closest_monster((x, y), wrld) < 2:
        return 1
    else:
        return 0

# ==================== FEATURES ==================== #
#   - Distance to closest bomb
#   - Distance to closest monster
#   - 1 / (Distance to exit)^2


# Returns an integer representing the Manhattan distance to the closest bomb.
def closest_bomb(self):
   return 1  # Will implement this later, in part 2 most likely. For now we don't care about bombs.


# Returns an integer representing the A* distance to the closest monster.
def closest_monster(coords, wrld):
    x = coords[0]
    y = coords[1]
    monsters = monster_tiles(wrld)
    p = float('inf')
    for m in monsters:
        distance = len(aStar((x, y), wrld, m))
        if distance < p:
            p = distance
    return p


# Returns 1/(A* distance to exit)^2.
def distance_to_exit(c, wrld):
    start = (c.x, c.y)
    return 1 / (len(aStar(start, wrld, wrld.exitcell)) ** 2)


# Returns a list of tiles which are occupied by at least 1 monster.
def monster_tiles(wrld):
    tiles = []
    for x in range(0, wrld.width()):
        for y in range(0, wrld.height()):
            if wrld.monsters_at(x, y):
                tiles.append((x, y))
    return tiles


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


def aStar(start, wrld, goal):
    x = start[0]
    y = start[1]
    # print("SELFX: " + str(self.x))
    # print("SELFY: " + str(self.y))
    frontier = []
    frontier.append(((x, y), 0))
    came_from = {}
    cost_so_far = {}
    came_from[(x, y)] = None
    cost_so_far[(x, y)] = 0

    monsters = []


    while not len(frontier) == 0:
        frontier.sort(key=lambda tup: tup[1])  # check that
        current = frontier.pop(0)
        if (current[0][0], current[0][1]) == goal:
            break
        for next in get_adjacent(current[0], wrld):
            if wrld.wall_at(next[0], next[1]):
                cost_so_far[(next[0], next[1])] = 999
                new_cost = 1000
            else:
                new_cost = cost_to(current[0], next) + cost_so_far[current[0]]
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                frontier.append((next, new_cost + manhattan_distance(next[0], next[1], goal[0], goal[1])))
                came_from[next] = current[0]

    cursor = goal
    path = []
    while not cursor == (x, y):
        path.append(cursor)
        try:
            cursor = came_from[cursor]
        except KeyError:
            return 0, 0
    #if draw:
        #print("PATH: ")
        #print(path)

    return path