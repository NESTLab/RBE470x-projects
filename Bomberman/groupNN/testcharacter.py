# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import math
import queue


class TestCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        super().__init__(name, avatar, x, y)
        self.exit_position = None
        self.start = (self.x, self.y)
        self.came_from = {self.start: None}

    def do(self, wrld):
        if self.exit_position is None:
            for x in range(0, wrld.width()):
                for y in range(0, wrld.height()):
                    if wrld.exit_at(x, y):
                        self.exit_position = (x, y)
                        break
                if self.exit_position is not None:
                    break

        frontier = PQueue()
        frontier.put((self.x, self.y), 0)  # come back to
        # came_from = {}
        cost_so_far = {}
        cost_so_far[(self.x, self.y)] = 0

        if self.x == self.start[0] and self.y == self.start[1] or (self.x, self.y) not in self.came_from:
                self.a_star(frontier, cost_so_far, wrld)

        next_move = self.find_next_move(self.came_from, self.exit_position)
        # print(next_move)
        self.move(next_move[0] - self.x, next_move[1] - self.y)

    def find_next_move(self, came_from, exit_position):
        next_move = exit_position

        while came_from[next_move] is not (self.x, self.y):
            if came_from[next_move] == (self.x, self.y):
                break
            next_move = came_from[next_move]

        return next_move

    def a_star(self, frontier, cost_so_far, wrld):
        while not frontier.empty():
            current = frontier.get()
            if current == self.exit_position:
                break

            possible_moves = self.get_possible_moves(current[0], current[1], wrld)
            for next in possible_moves:
                new_cost = cost_so_far[(self.x, self.y)] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.get_distance_to_exit(next, self.exit_position)
                    frontier.put((next[0], next[1]), priority)
                    self.came_from[next] = current

    def get_possible_moves(self, x, y, wrld):
        array = []
        for dx in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            if (x+dx >=0) and (x+dx < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    # Make sure the monster is moving
                    if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                        if (y+dy >=0) and (y+dy < wrld.height()):
                            # No need to check impossible moves
                            if not wrld.wall_at(x+dx, y+dy):
                                array.append((x + dx, y + dy))
        return array
        
    def get_distance_to_exit(self, position, exit_position):
        return math.sqrt((position[1] - exit_position[1]) * (position[1] - exit_position[1]) +
                         (position[0] - exit_position[0]) * (position[0] - exit_position[0]))


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
