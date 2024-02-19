"""
Utility functions for the teamNN package.
Import to any file using: from teamNN.utility import *

Includes:
float euclidean_dist(point_one:tuple, point_two:tuple)
bool is_cell_walkable(wrld:World, x:int, y:int)
tuple[] eight_neighbors(wrld:World, x:int, y:int)
tuple character_location(wrld:World) //Returns First Character
tuple monster_location(wrld:World) //Returns First Monster
int manhattan_distance_to_exit(wrld:World)
int manhattan_distance_to_monster(wrld:World) //Returns Nearest Monster
int euclidean_distance_to_exit(wrld:World)
int euclidean_distance_to_monster(wrld:World) //Returns Nearest Monster

"""
from PriorityQueue import PriorityQueue

prevMove = [0, 0]


def euclidean_dist(point_one, point_two):
    """Returns the euclidean distance between two points.
    point_one: (x, y) tuple
    point_two: (x, y) tuple
    returns: float"""
    return ((point_one[0] - point_two[0]) ** 2 + (point_one[1] - point_two[1]) ** 2) ** 0.5


def is_cell_walkable(wrld, x, y):
    """Returns True if the cell at (x, y) is walkable.
    wrld: World object
    x: int
    y: int
    returns: bool"""
    if is_cell_in_range(wrld, x, y):
        return wrld.exit_at(x, y) or wrld.empty_at(x, y) or wrld.monsters_at(x, y) or wrld.characters_at(x, y)
    return False


def is_cell_in_range(wrld, x, y):
    """Returns True if the cell at (x, y) is in range.
    wrld: World object
    x: int
    y: int
    returns: bool"""
    return wrld.width() > x >= 0 and wrld.height() > y >= 0


def eight_neighbors(wrld, x, y):
    """
    Returns the walkable 8-neighbors cells of (x,y) in wrld
    wrld: World object
    x: int
    y: int
    returns: list of (x, y) tuples
    """
    return_list = []

    if x != 0 and is_cell_walkable(wrld, x - 1, y):
        return_list.append((x - 1, y))
    if x != wrld.width() - 1 and is_cell_walkable(wrld, x + 1, y):
        return_list.append((x + 1, y))
    if y != 0 and is_cell_walkable(wrld, x, y - 1):
        return_list.append((x, y - 1))
    if y != wrld.height() - 1 and is_cell_walkable(wrld, x, y + 1):
        return_list.append((x, y + 1))
    if x != 0 and y != 0 and is_cell_walkable(wrld, x - 1, y - 1):
        return_list.append((x - 1, y - 1))
    if x != wrld.width() - 1 and y != 0 and is_cell_walkable(wrld, x + 1, y - 1):
        return_list.append((x + 1, y - 1))
    if y != wrld.height() - 1 and x != 0 and is_cell_walkable(wrld, x - 1, y + 1):
        return_list.append((x - 1, y + 1))
    if x != wrld.width() - 1 and y != wrld.height() - 1 and is_cell_walkable(wrld, x + 1, y + 1):
        return_list.append((x + 1, y + 1))

    return return_list


def a_star(wrld, goal=None, start=None):
    print("Astar is thinking")
    found = False

    if start is None:
        start = character_location(wrld)  # Start at current position
    if goal is None:
        goal = wrld.exitcell  # Goal is exit cell

    cost_so_far = {start: 0}  # Dictionary of costs to get to each cell
    came_from = {start: None}  # Dictionary of where each cell came from

    frontier = PriorityQueue()  # Priority queue of cells to visit
    frontier.put(start, 0)

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            found = True
            break

        successors = identifySuccessors(current, wrld, goal)

        # Check all walkable neighbors of current cell
        for successor in successors:
            # Calculate cost to get to neighbor - 1 or 1.4
            diagonal = 0
            if successor in cost_so_far and \
                    successor[0] - current[0] != 0 and successor[1] - current[1] != 0:
                diagonal += 2
            new_cost = cost_so_far[current] + euclidean_dist(current, successor) + diagonal

            # If neighbor has no path or new path is better, update path
            if successor not in cost_so_far or new_cost < cost_so_far[successor]:
                cost_so_far[successor] = new_cost
                priority = new_cost + euclidean_dist(successor, goal)
                frontier.put(successor, priority)
                came_from[successor] = current

    if not found:
        return [start, start]
    # Reconstruct path using came_from dictionary
    currPos = goal
    finalPath = [goal]
    while currPos != start:
        currPos = came_from[currPos]
        finalPath.append(currPos)

    finalPath.reverse()
    return finalPath


def identifySuccessors(current, wrld, goal):
    succesors = []
    for neighbour in eight_neighbors(wrld, current[0], current[1]):
        dx = neighbour[0] - current[0]
        dy = neighbour[1] - current[1]
        direction = [dx, dy]
        pointfump = jump(current, direction[0], direction[1], wrld, goal)
        if pointfump:
            succesors.append(pointfump)
    return succesors


def jump(current, dx, dy, wrld, goal):
    nx = current[0] + dx
    ny = current[1] + dy

    if (nx, ny) == goal:
        return (nx, ny)

    # Original position
    ox = nx
    oy = ny
    original = (ox, oy)

    if dx != 0 and dy != 0:
        while True:
            if is_cell_walkable(wrld, ox - dx, oy + dy) \
                    and not is_cell_walkable(wrld, ox + dx, oy - dy) \
                    or is_cell_walkable(wrld, ox + dx, oy - dy) \
                    and not is_cell_walkable(wrld, ox - dx, oy + dy):
                return ox, oy
            if jump(original, dx, 0, wrld, goal) or jump(original, 0, dy, wrld, goal):
                return ox, oy

            ox += dx
            oy += dy

            if not is_cell_walkable(wrld, ox, oy):
                return None
            if (ox, oy) == goal:
                return (ox, oy)
    else:
        # Moving in y-axis
        if dx != 0:
            while True:
                if is_cell_walkable(wrld, ox + dx, ny + 1) \
                        and not is_cell_walkable(wrld, ox, ny + 1) \
                        or is_cell_walkable(wrld, ox + dx, ny - 1) \
                        and not is_cell_walkable(wrld, ox, ny - 1):
                    return ox, ny
                ox += dx
                if (ox, ny) == goal:
                    return (ox, ny)
                if not is_cell_walkable(wrld, ox, ny):
                    return None
        # Moving in x-axis
        else:
            while True:
                if is_cell_walkable(wrld, nx + 1, oy + dy) \
                        and not is_cell_walkable(wrld, nx + 1, oy) \
                        or is_cell_walkable(wrld, nx - 1, oy + dy) \
                        and not is_cell_walkable(wrld, nx - 1, oy):
                    return nx, oy
                oy += dy
                if (nx, oy) == goal:
                    return (nx, oy)
                if not is_cell_walkable(wrld, nx, oy):
                    return None
    return jump(current, dx, dy, wrld, goal)


def checkinsamedirection(prevmove, current, neighbor):
    if abs(prevmove[0] - current[0]) == abs(current[0] - neighbor[0]):
        return True
    elif abs(prevmove[1] - current[1]) == abs(current[1] - neighbor[1]):
        return True
    else:
        return False


def a_star2(wrld, goal=None, start=None):
    # Original astar
    found = False
    if start is None:
        start = character_location(wrld)  # Start at current position
    if goal is None:
        goal = wrld.exitcell  # Goal is exit cell

    cost_so_far = {start: 0}  # Dictionary of costs to get to each cell
    came_from = {start: None}  # Dictionary of where each cell came from

    frontier = PriorityQueue()  # Priority queue of cells to visit
    frontier.put(start, 0)

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            found = True
            break

        # Check all walkable neighbors of current cell
        for neighbor in eight_neighbors(wrld, current[0], current[1]):
            # Calculate cost to get to neighbor - 1 or 1.4
            new_cost = cost_so_far[current] + euclidean_dist(current, neighbor)

            # If neighbor has no path or new path is better, update path
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + euclidean_dist(neighbor, goal)
                frontier.put(neighbor, priority)
                came_from[neighbor] = current

    if not found:
        return [(start), (start)]

    # Reconstruct path using came_from dictionary
    currPos = goal
    finalPath = []
    finalPath.append(goal)
    while currPos != start:
        currPos = came_from[currPos]
        finalPath.append(currPos)
    finalPath.reverse()
    return finalPath


def character_location(wrld):
    """Returns the location of the character in wrld.
    wrld: World object
    returns: (x, y) tuple"""
    if len(wrld.characters) == 0:
        Exception("No character in world")
    return next(iter(wrld.characters.items()))[1][0].x, next(iter(wrld.characters.items()))[1][0].y


def exit_location(wrld):
    """Returns the location of the exit in wrld.
    wrld: World object
    returns: (x, y) tuple"""
    return wrld.exitcell[0], wrld.exitcell[1]


def monster_location(wrld):
    """Returns the location of the nearest monster in wrld.
    wrld: World object
    returns: (x, y) tuple"""
    if len(wrld.monsters) == 0:
        print("No monster in world")
        return 1, 0
    realMonsters = []
    monsters = list(wrld.monsters.values())
    for monster in monsters:
        realMonsters.append(monster[0])
    monsters = realMonsters
    monsters.sort(key=lambda m: euclidean_dist(character_location(wrld), (m.x, m.y)))
    return monsters[0].x, monsters[0].y


def manhattan_distance_to_exit(wrld, start=None):
    """Returns the manhattan distance to the exit.
    wrld: World object
    start (optional): (x, y) tuple to start from, defaults to character location
    returns: float"""
    if start is None:
        start = character_location(wrld)

    return abs(start[0] - wrld.exitcell[0]) + abs(start[1] - wrld.exitcell[1])


def euclidean_distance_to_exit(wrld, start=None):
    """Returns the euclidean distance to the exit.
    wrld: World object
    start (optional): (x, y) tuple to start from, defaults to character location
    returns: float"""
    if start is None:
        start = character_location(wrld)

    return ((start[0] - wrld.exitcell[0]) ** 2 + (start[1] - wrld.exitcell[1]) ** 2) ** 0.5


def manhattan_distance_to_monster(wrld, start=None):
    """Returns the manhattan distance to the closest monster.
    wrld: World object
    start (optional): (x, y) tuple to start from, defaults to character location
    returns: float"""

    if start is None:
        start = character_location(wrld)

    if len(wrld.monsters) == 0:
        return 999
    else:
        return min(
            [abs(start[0] - monster[1][0].x) + abs(start[1] - monster[1][0].y) for monster in wrld.monsters.items()])


def euclidean_distance_to_monster(wrld, start=None):
    """Returns the euclidean distance to the closest monster.
    wrld: World object
    start (optional): (x, y) tuple to start from, defaults to character location
    returns: float"""

    if start is None:
        start = character_location(wrld)

    if len(wrld.monsters) == 0:
        return 999
    else:
        return min([((start[0] - monster[1][0].x) ** 2 + (start[1] - monster[1][0].y) ** 2) ** 0.5 for monster in
                    wrld.monsters.items()])


def a_star_distance_to_exit(wrld, start=None):
    """Returns the a* distance to the exit.
    wrld: World object
    start (optional): (x, y) tuple to start from, defaults to character location
    returns: float"""
    if start is None:
        return len(a_star(wrld, goal=wrld.exitcell))
    else:
        path = a_star(wrld, goal=wrld.exitcell, start=start);
        # print("astar is")
        # print(path.pop(len(path)-1))
        if path.pop(len(path) - 1) != wrld.exitcell:
            return -1
        else:
            return len(path)


def a_star_distance_to_monster(wrld, start=None):
    """Returns the a* distance to the closest monster.
    wrld: World object
    start (optional): (x, y) tuple to start from, defaults to character location
    returns: float"""

    if start is None:
        return len(a_star(wrld, goal=monster_location(wrld)))
    else:
        return len(a_star(wrld, goal=monster_location(wrld), start=start))


def a_star_distance(wrld, start, goal):
    """Returns the a* distance between two points.
    wrld: World object
    start: (x, y) tuple to start from
    goal: (x, y) tuple to end at
    returns: float"""
    if not is_cell_walkable(wrld, goal[0], goal[1]):
        print("Goal is not walkable!")
        raise Exception("Goal is not walkable!", goal)
    if not is_cell_walkable(wrld, start[0], start[1]):
        print("Start is not walkable!")
        raise Exception("Start is not walkable!", start)

    try:
        return len(a_star(wrld, goal=goal, start=start))
    except:  # When A* fails and returns None, return a large number
        return 999


def monster_travel_direction(wrld):
    """Returns the direction the monster is moving in.
    wrld: World object
    returns: (x, y) tuple"""
    if len(wrld.monsters) == 0:
        Exception("No monster in world")
    return next(iter(wrld.monsters.items()))[1][0].dx, next(iter(wrld.monsters.items()))[1][0].dy
