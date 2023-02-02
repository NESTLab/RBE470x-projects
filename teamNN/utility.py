"""Utility functions for the teamNN package."""


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


def character_location(wrld):
    """Returns the location of the character in wrld.
    wrld: World object
    returns: (x, y) tuple"""
    if len(wrld.characters) == 0:
        Exception("No character in world")
    return wrld.characters[0][0].x, wrld.characters[0][0].y


def manhattan_distance_to_exit(wrld):
    """Returns the manhattan distance to the exit.
    wrld: World object
    returns: float"""

    self = character_location(wrld)
    return abs(self[0] - wrld.exitcell[0]) + abs(self[1] - wrld.exitcell[1])


def euclidean_distance_to_exit(wrld):
    """Returns the euclidean distance to the exit.
    wrld: World object
    returns: float"""

    self = character_location(wrld)
    return ((self[0] - wrld.exitcell[0]) ** 2 + (self[1] - wrld.exitcell[1]) ** 2) ** 0.5


def manhattan_distance_to_monster(wrld):
    """Returns the manhattan distance to the closest monster.
    wrld: World object
    returns: float"""

    self = character_location(wrld)
    if len(wrld.monsters) == 0:
        return 999
    else:
        return min(
            [abs(self[0] - monster[1][0].x) + abs(self[1] - monster[1][0].y) for monster in wrld.monsters.items()])


def euclidean_distance_to_monster(wrld):
    """Returns the euclidean distance to the closest monster.
    wrld: World object
    returns: float"""

    self = character_location(wrld)
    if len(wrld.monsters) == 0:
        return 999
    else:
        return min([((self[0] - monster[1][0].x) ** 2 + (self[1] - monster[1][0].y) ** 2) ** 0.5 for monster in
                    wrld.monsters.items()])
