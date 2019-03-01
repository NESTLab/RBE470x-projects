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


class MinMax(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        super().__init__(name, avatar, x, y)
        self.exit_position = None
        self.start = (self.x, self.y)
        self.came_from = {self.start: None}
        self.state = NORMAL
        self.prev_state = None
        self.monster_dist = 0
        self.max_depth = 4

    def do(self, wrld):
        if self.exit_position is None:
            for x in range(0, wrld.width()):
                for y in range(0, wrld.height()):
                    if wrld.exit_at(x, y):
                        self.exit_position = (x, y)
                        break
                if self.exit_position is not None:
                    break

        monster = None
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.monsters_at(x, y):
                    monster = (x, y)
                if monster is not None:
                    break

        self.prev_state = self.state
        self.monster_dist = self.get_distance_between((self.x, self.y), (monster[0], monster[1]))
        if self.monster_dist < 5:

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
            max_val = self.max_value(wrld, (self.x, self.y), monster, -99999, 99999, 0)
            next_move = max_val[1]
            # self.a_star(frontier, cost_so_far, wrld, monster)

        self.move(next_move[0] - self.x, next_move[1] - self.y)

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

    def find_next_move(self, came_from, exit_position):
        next_move = exit_position

        while came_from[next_move] is not (self.x, self.y):
            if came_from[next_move] == (self.x, self.y):
                break
            next_move = came_from[next_move]

        return next_move

    def max_value(self, wrld, char, monster, alpha, beta, depth):
        monst_distance = self.get_distance_between(char, monster)
        if char == monster:
            return ((0.9 ** depth) * -10000), char
        elif char == self.exit_position:
            return ((0.9 ** depth) * 100000), char
        elif monst_distance < 2:
            return ((0.9 ** depth) * -3000), char
        elif depth > self.max_depth:
            return (self.heuristic(char[0], char[1], depth, monst_distance)), char

        moves = self.get_possible_moves(char[0], char[1], wrld)
        value = (-9999999, None)  # (value, move)
        for move in moves:
            min_value = self.min_value(wrld, move, monster, alpha, beta, depth+1)
            temp = max(value[0], min_value[0])
            if temp is not value[0]:
                value = [temp, move]
            if value[0] >= beta:
                return value
            alpha = max(alpha, value[0])
        return value

    def min_value(self, wrld, char, monster, alpha, beta, depth):
        monst_distance = self.get_distance_between(char, monster)
        if char == monster:
            return ((0.9 ** depth) * -10000), char
        elif char == self.exit_position:
            return ((0.9 ** depth) * 100000), char
        elif monst_distance < 2:
            return ((0.9 ** depth) * -3000), char
        elif depth > self.max_depth:
            return (self.heuristic(char[0], char[1], depth, monst_distance)), char

        moves = self.get_possible_moves(monster[0], monster[1], wrld)
        value = (9999999, None)
        for move in moves:
            max_value = self.max_value(wrld, char, move, alpha, beta, depth+1)
            temp = min(value[0], max_value[0])
            if temp is not value[0]:
                value = (temp, move)
            if value[0] <= alpha:
                return value
            beta = min(beta, value[0])
        return value

    def heuristic(self, char_x, char_y, depth, monst_distance):
        exit_dist = self.get_distance_between((char_x, char_y), self.exit_position)
        # if monst_distance < 3:
        #     monst_distance = -10
        # return (0.9 ** depth) * ((monst_distance / 2) + (40 / exit_dist))
        return (0.9 ** depth) * (monst_distance + (75 / (1 + exit_dist)))

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


