# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import operator


class TestCharacter(CharacterEntity):
    def do(self, wrld):
        # Your code here
        goal = self.get_exit(wrld)
        start = self.get_my_location(wrld)
        bomb = self.get_bomb(wrld)
        x_dir, y_dir = self.get_direction(start, wrld)
        monster = self.get_monster(wrld)
        next_move = self.a_star(wrld, start, goal, 0)  # returns (x,y) coordinate of next move

        try:
            dx = next_move[0] - start[0]
            dy = next_move[1] - start[1]
        except TypeError:
            pass
        # Monsters are within a range that you should run from
        run_from_monster = self.check_monster(start, wrld, 3)

        # Safe from monsters potentially, safe to place bombs and wait
        safe_from_monster = self.check_monster(start, wrld, 5)

        try:
            if run_from_monster:
                # STATE: MONSTER ( There are a monsters within our range)
                print("STATE: MONSTER")
                self.place_bomb()
                monster_move_away = self.a_star(wrld, start, run_from_monster[0], -1)
                dx = monster_move_away[0] - start[0]
                dy = monster_move_away[1] - start[1]
                print("Move: {}, {}".format(dx, dy))
                self.move(dx, dy)
            elif wrld.wall_at(*next_move):
                print("STATE: 3")
                print(x_dir, y_dir)
                self.move(x_dir, y_dir)
            elif next_move[0] == bomb[0] or next_move[1] == bomb[1] or wrld.explosion_at(*next_move):
                print("STATE: 4")
                if not run_from_monster and (bomb[0] == start[0] or bomb[1] == start[1]) \
                        and not wrld.explosion_at(start[0] + dx, start[1] + dy):
                    print("4.1")
                    bomb_move_away = self.a_star(wrld, start, bomb, -1)
                    dx = bomb_move_away[0] - start[0]
                    dy = bomb_move_away[1] - start[1]
                    print(dx, dy)
                    self.move(dx, dy)
                elif not run_from_monster:
                    print("4.2")
                    print(0, 0)
                    self.move(0, 0)
                monster_move_away = self.a_star(wrld, start, run_from_monster[0], -1)
                dx = monster_move_away[0] - start[0]
                dy = monster_move_away[1] - start[1]
                print('4.3')
                print("Move: {}, {}".format(dx, dy))
                self.move(dx, dy)
            else:
                print("STATE: 5")
                print(dx, dy)
                self.move(dx, dy)
                if wrld.wall_at(start[0], start[1] + 1) or wrld.wall_at(start[0], start[1] - 1):
                    self.place_bomb()
        except (IndexError, TypeError):
            pass


    # Becareful of multiple monsters
    # RETURN [list of (int x, int y)]: coordinate positions of monsters within range
    @staticmethod
    def check_monster(start, wrld, radius):
        monsters_near = [] # list of tuples (int x, int y)
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                if wrld.next()[0].monsters_at(start[0] + x, start[1] + y):
                    # monster was found
                    monsters_near.append((start[0] + x, start[1] + y))
        return monsters_near

    @staticmethod
    def get_direction(start, wrld):
        x = 1
        y = 1
        if start[0] > wrld.width()/2:
            x = -1
        if start[1] > wrld.height()/2:
            y = -1
        return x, y

    # TODO: SHOULDN'T THIS RETURN A LIST OF MONSTERS??? IN CASE THERE ARE MORE THAN ONE
    @staticmethod
    def get_monster(wrld):
        # Find monsters in board
        for x in range(wrld.width()):
            for y in range(wrld.height()):
                if wrld.monsters_at(x, y):
                    return x, y
        return -1, -1

    @staticmethod
    def get_exit(wrld):
        # Find the exit to use for heuristic A*
        for x in range(wrld.width()):
            for y in range(wrld.height()):
                if wrld.exit_at(x, y):
                    return x, y
        return -1, -1

    @staticmethod
    def get_bomb(wrld):
        # Find the exit to use for heuristic A*
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.bomb_at(x, y):
                    return x, y
        return -1, -1

    @staticmethod
    def get_my_location(wrld):
        # Find the exit to use for heuristic A*
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.characters_at(x, y):
                    return x, y

    # Determining the heuristic value, being Euclidean Distance
    @staticmethod
    def heuristic(start, goal, wrld):
        (x1, y1) = start
        (x2, y2) = goal
        value = (x2 - x1)**2 + (y2 - y1)**2
        return value

    # this a* algorithm picks the *CLOSEST* distance to the goal
    # PARAM [SensedWorld] wrld: wrld grid, used to get boundries
    # PARAM [tuple (int, int)] start: tuple with x and y coordinates of starting position in board
    # PARAM [tuple (int, int)] goal: tuple with x and y coordinates of exit position in board
    # RETURN [?????]: Possibly return list with tuples of (int, int). This would be the optimal path to traverse
    def a_star(self, wrld, start, goal, min_max):  # Min/max; 0 min 1 max
        neighbors = self.get_neighbors(start, wrld)
        neighbors_values = []
        for neighbor in neighbors:
            neighbors_values.append((neighbor[0], neighbor[1], self.heuristic(neighbor, goal, wrld)))
        neighbors_values.sort(key=operator.itemgetter(2))

        runaway_list = []

        if min_max == 0:
            try:
                return neighbors_values[0][0], neighbors_values[0][1]
            except IndexError:
                pass
        else:
            for neighbor in neighbors_values:
                if neighbor[0] != wrld.width() and neighbor[1] != wrld.height \
                        and neighbor[0] != 0 and neighbor[1] != 0 and not \
                        wrld.explosion_at(neighbor[0], neighbor[1]):
                    runaway_list.append(neighbor)
            try:
                print('run list')
                print(runaway_list)
                return runaway_list[-1][0], runaway_list[-1][1]
            except IndexError:
                pass

    @staticmethod
    def get_neighbors(start, wrld):
        x = start[0]
        y = start[1]
        neighbors = [(x+1, y), (x, y-1), (x-1, y), (x, y+1),
                     (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
        result = []
        # check that neighbors are inside wrld bounds
        for neighbor in neighbors:
            if 0 <= neighbor[0] < wrld.width() and 0 <= neighbor[1] < wrld.height():
                if not wrld.wall_at(*neighbor) and not wrld.monsters_at(*neighbor) \
                        and not wrld.bomb_at(*neighbor) and not wrld.next()[0].explosion_at(*neighbor):
                    result.append(neighbor)
        return result
