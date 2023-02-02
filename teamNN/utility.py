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
from teamNN.PriorityQueue import PriorityQueue


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
    return wrld.exit_at(x, y) or wrld.empty_at(x, y) or wrld.monsters_at(x, y)


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
    """Returns the location of the first monster in wrld.
    wrld: World object
    returns: (x, y) tuple"""
    if len(wrld.monsters) == 0:
        Exception("No monster in world")
    return next(iter(wrld.monsters.items()))[1][0].x, next(iter(wrld.monsters.items()))[1][0].y


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
        return len(a_star(wrld, goal=wrld.exitcell, start=start))


def a_star_distance_to_monster(wrld, start=None):
    """Returns the a* distance to the closest monster.
    wrld: World object
    start (optional): (x, y) tuple to start from, defaults to character location
    returns: float"""

    if start is None:
        return len(a_star(wrld, goal=monster_location(wrld)))
    else:
        return len(a_star(wrld, goal=monster_location(wrld), start=start))
