# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import math

NORMAL = 0  # not in danger
MONSTER = 1  # in danger from monster
BOMB = 2  # in danger from bomb


class TestCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        super().__init__(name, avatar, x, y)
        self.exit_position = None
        self.start = (self.x, self.y)
        self.came_from = {self.start: None}
        self.state = NORMAL
        self.prev_state = None
        self.nearest_monster = 0
        self.last_mon = None
        self.bomb = None
        self.explosions = []
        self.max_depth = 1

    def do(self, wrld):
        self.max_depth = 1
        if self.exit_position is None:
            for x in range(0, wrld.width()):
                for y in range(0, wrld.height()):
                    if wrld.exit_at(x, y):
                        self.exit_position = (x, y)
                        break
                if self.exit_position is not None:
                    break

        monsters = []
        self.explosions = []
        self.bomb = None
        # explosion = None
        # bomb = None
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.monsters_at(x, y):
                    monsters.append((x, y))
                explosion = wrld.explosion_at(x, y)
                if explosion is not None:
                    self.explosions.append(explosion)
                bomb = wrld.bomb_at(x, y)
                if bomb is not None:
                    self.bomb = bomb

        self.prev_state = self.state
        self.nearest_monster = 100
        if len(monsters):
            for monster in monsters:
                dist = self.get_distance_between((self.x, self.y), (monster[0], monster[1]))
                if dist < self.nearest_monster:
                    self.nearest_monster = dist

        if self.in_corner(wrld) and self.nearest_monster > 3 and self.bomb is None and len(self.explosions) == 0:
            self.state = BOMB
            self.place_bomb()
        elif len(self.explosions) > 0 or self.bomb is not None:
            self.state = BOMB
        elif self.nearest_monster < 6:
            self.state = MONSTER
        else:
            self.state = NORMAL

        frontier = PQueue()
        frontier.put((self.x, self.y), 0)
        cost_so_far = {(self.x, self.y): 0}

        next_move = None
        if self.state == NORMAL:
            # if self.x == self.start[0] and self.y == self.start[1] or self.prev_state is not NORMAL:
            self.a_star(frontier, cost_so_far, wrld)
            next_move = self.find_next_move(self.came_from, self.exit_position)
        elif self.state == MONSTER:
            next_move = self.avoid_monster(wrld, monsters)
            # self.a_star(frontier, cost_so_far, wrld, monster)
        elif self.state == BOMB:
            next_move = self.avoid_bomb(wrld, monsters)

        self.move(next_move[0] - self.x, next_move[1] - self.y)

    def avoid_monster(self, wrld, monsters):
        next_move = None
        if len(monsters) < 0:
            monsters.append((0, 0))
        if self.nearest_monster < 6:
            self.max_depth = 2
        possible_moves = self.get_possible_moves(self.x, self.y, wrld)
        value = -10000000
        for move in possible_moves:
            expected = self.exp_value(wrld, self.exit_position, move[0], move[1], monsters, 0)
            if expected >= value:
                value = expected
                next_move = move
        return next_move

    def avoid_bomb(self, wrld, monsters):
        next_move = None
        if len(monsters) < 0:
            monsters.append((0, 0))
        possible_moves = self.get_possible_moves(self.x, self.y, wrld)
        value = -10000000
        for move in possible_moves:
            expected = self.exp_value_bomb(wrld, self.exit_position, move[0], move[1], monsters, 0)
            if expected >= value:
                value = expected
                next_move = move
        return next_move

    def a_star(self, frontier, cost_so_far, wrld):
        while not frontier.empty():
            current = frontier.get()
            if current == self.exit_position:
                break

            possible_moves = self.get_possible_moves(current[0], current[1], wrld)
            for next in possible_moves:
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.get_distance_between(next, self.exit_position)
                    frontier.put((next[0], next[1]), priority)
                    self.came_from[next] = current

    def exp_value(self, wrld, exit_position, char_x, char_y, monsters, depth):
        char = (char_x, char_y)
        if char == exit_position:
            return (0.9 ** depth) * 100000
        monst_value = 0
        for monster in monsters:
            dist = self.get_distance_between(char, monster)
            if dist == 0:
                return (0.9 ** depth) * -10000
            if dist < 3:
                monst_value += (0.9 ** depth) * -5000
        if monst_value != 0:
            return monst_value

        value = 0
        if len(monsters) == 2:
            moves_array = []
            for monster in monsters:
                moves_array.append(self.get_possible_moves(monster[0], monster[1], wrld))
            for move1 in moves_array[0]:
                for move2 in moves_array[1]:
                    prob = 1 / (len(moves_array[0]) + len(moves_array[1]))
                    new_monsters = [move1, move2]
                    v = self.max_value(wrld, exit_position, char_x, char_y, new_monsters, depth)
                    value = value + prob * v
            return value
        else:
            monster = monsters[0]
            monster_moves = self.get_possible_moves(monster[0], monster[1], wrld)
            for move in monster_moves:
                prob = 1 / len(monster_moves)
                new_monsters = [move]
                v = self.max_value(wrld, exit_position, char_x, char_y, new_monsters, depth)
                value = value + prob * v
        return value

    def max_value(self, wrld, exit_position, char_x, char_y, monsters, depth):
        char = (char_x, char_y)
        monst_value = 0
        monst_distances = []
        for monster in monsters:
            dist = self.get_distance_between(char, monster)
            monst_distances.append(dist)
            if dist == 0:
                return (0.9 ** depth) * -10000
            if dist < 3:
                monst_value += (0.9 ** depth) * -5000
        if monst_value != 0:
            return monst_value
        elif depth > 1:
            exit_dist = self.get_distance_between(char, exit_position)
            m_weight = 0
            for m_dist in monst_distances:
                w = 20 - m_dist
                if w == 0:
                    w -= 1
                m_weight += (20 / w)
            return (0.9 ** depth) * (m_weight + (55 / (1 + exit_dist)))

        value = -100000000
        character_moves = self.get_possible_moves(char_x, char_y, wrld)
        for move in character_moves:
            v = self.exp_value(wrld, exit_position, move[0], move[1], monsters, depth + 1)
            value = max(value, v)
        return value

    def exp_value_bomb(self, wrld, exit_position, char_x, char_y, monsters, depth):
        terminal = self.terminal_state(char_x, char_y, monsters, depth)
        if terminal is not None:
            return terminal
        close_monsters = []
        for monster in monsters:
            dist = self.get_distance_between((char_x, char_y), monster)
            if dist < 6:
                close_monsters.append(monster)

        value = 0
        if len(close_monsters) == 2:
            moves_array = []
            for monster in close_monsters:
                moves_array.append(self.get_possible_moves(monster[0], monster[1], wrld))
            for move1 in moves_array[0]:
                for move2 in moves_array[1]:
                    prob = 1 / (len(moves_array[0]) + len(moves_array[1]))
                    new_monsters = [move1, move2]
                    v = self.max_value_bomb(wrld, exit_position, char_x, char_y, new_monsters, depth)
                    value = value + prob * v
            return value
        elif len(close_monsters) == 1:
            monster = close_monsters[0]
            monster_moves = self.get_possible_moves(monster[0], monster[1], wrld)
            for move in monster_moves:
                prob = 1 / len(monster_moves)
                new_monsters = [move]
                v = self.max_value(wrld, exit_position, char_x, char_y, new_monsters, depth)
                value = value + prob * v
        return value

    def max_value_bomb(self, wrld, exit_position, char_x, char_y, monsters, depth):
        terminal = self.terminal_state(char_x, char_y, monsters, depth)
        if terminal is not None:
            return terminal
        value = -1000000000
        character_moves = self.get_possible_moves(char_x, char_y, wrld)
        for move in character_moves:
            v = self.exp_value_bomb(wrld, exit_position, move[0], move[1], monsters, depth + 1)
            value = max(value, v)
        return value

    def terminal_state(self, char_x, char_y, monsters, depth):
        bad = (0.9 ** depth) * -100
        char = (char_x, char_y)
        monst_value = 0
        monst_distances = []
        for monster in monsters:
            dist = self.get_distance_between(char, monster)
            monst_distances.append(dist)
            if dist == 0:
                return bad
            if dist < 3:
                monst_value += (0.9 ** depth) * -5000
        if monst_value != 0:
            return monst_value
        if self.bomb is not None and self.bomb.timer - depth <= 1:
            if char_x == self.bomb.x or char_y == self.bomb.y:
                return bad
        if len(self.explosions) > 0:
            for explo in self.explosions:
                explo_dist = self.get_distance_between((char_x, char_y), (explo.x, explo.y))
                if explo_dist == 0:
                    return bad
        if (char_x, char_y) == self.exit_position:
            return (0.9 ** depth) * 100000
        if depth > self.max_depth:
            exit_dist = self.get_distance_between(char, self.exit_position)
            m_weight = 0
            for m_dist in monst_distances:
                w = 40 - (2 * m_dist)
                if w == 0:
                    w -= 1
                m_weight += (100 / w)
            return (0.9 ** depth) * (m_weight + (15 / (1 + exit_dist)))
        return None

    def find_next_move(self, came_from, exit_position):
        next_move = exit_position

        while came_from[next_move] is not (self.x, self.y):
            if came_from[next_move] == (self.x, self.y):
                break
            next_move = came_from[next_move]

        return next_move

    def get_possible_moves(self, x, y, wrld):
        array = []
        for dx in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            if (x + dx >= 0) and (x + dx < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    # Make sure the monster is moving
                    if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                        if (y + dy >= 0) and (y + dy < wrld.height()):
                            # No need to check impossible moves
                            if not wrld.wall_at(x + dx, y + dy):
                                array.append((x + dx, y + dy))
        return array

    def get_distance_between(self, position, position2):
        # return math.sqrt((position[1] - position2[1]) * (position[1] - position2[1]) +
        #                  (position[0] - position2[0]) * (position[0] - position2[0]))
        return max(abs(position[0] - position2[0]), abs(position[1] - position2[1]))

    def in_corner(self, wrld):
        x = self.x
        y = self.y
        array = [-3, -2, -1, 0, 1, 2, 3]
        for dx in array:
            # Avoid out-of-bound indexing
            if (x + dx >= 0) and (x + dx < wrld.width()):
                # Loop through delta y
                for dy in array:
                    # Make sure the monster is moving
                    if (dx == 0) or (dy == 0):
                        # Avoid out-of-bound indexing
                        if (y + dy >= 0) and (y + dy < wrld.height()):
                            # No need to check impossible moves
                            if wrld.wall_at(x + dx, y + dy):
                                return True
        return False



class PQueue:
    def __init__(self):
        self.queue = []

    def put(self, item, priority):
        for x in range(0, len(self.queue)):
            if self.queue[x][1] > priority:
                self.queue.insert(x, (item, priority))
                return
        self.queue.append((item, priority))

    def get(self):
        temp = self.queue[0]
        self.queue.remove(temp)
        return temp[0]

    def empty(self):
        if len(self.queue) == 0:
            return True
        return False
