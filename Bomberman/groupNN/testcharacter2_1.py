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
BLOCKED = 3  # path to exit is blocked (not in danger from monster)
CRAZY = 4  # in danger from monster and bombs



class TestCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        super().__init__(name, avatar, x, y)
        self.exit_position = None
        self.start = (self.x, self.y)
        self.came_from = {self.start: None}
        self.state = NORMAL
        self.prev_state = None
        self.stillness_counter = 0
        self.lastx = 0
        self.lasty = 0

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
        if(monster is not None):
            if self.get_distance_to_exit((self.x, self.y), (monster[0], monster[1])) < 4:
                self.state = MONSTER
            else:
                self.state = NORMAL

        frontier = PQueue()
        frontier.put((self.x, self.y), 0)
        cost_so_far = {(self.x, self.y): 0}
        print(self.state)

        if self.state == (NORMAL) or self.state == BLOCKED:
            if self.x == self.start[0] and self.y == self.start[1] or self.prev_state is not NORMAL:
                print("i should run astar 1")
                self.a_star(frontier, cost_so_far, wrld, None)
        elif self.state == MONSTER:
            self.a_star(frontier, cost_so_far, wrld, monster)
        elif self.state == BOMB:
            self.a_star(frontier, cost_so_far, wrld, None)

        next_move = self.find_next_move(self.came_from, self.exit_position)

        if (self.lastx == self.x and self.lasty == self.y):
            self.stillness_counter += 1
        else:
            self.stillness_counter = 0
            self.lastx = self.x
            self.lasty = self.y
        print("stillness_counter: ", self.stillness_counter)

        if (self.state is BLOCKED and self.stillness_counter == 2):
            # drop a bomb
            self.place_bomb()
            self.state = BOMB
            print("I'm dropping a bomb")
        else:
            self.move(next_move[0] - self.x, next_move[1] - self.y)

    def a_star(self, frontier, cost_so_far, wrld, monster):
        print("A star running")
        while not frontier.empty():
            current = frontier.get()
            if current == self.exit_position:
                break

            possible_moves = self.get_possible_moves(current[0], current[1], wrld)
            for next in possible_moves:
                expected = 0
                if self.state == MONSTER:
                    expected = self.exp_value(wrld, self.exit_position, next[0], next[1], monster[0], monster[1], 0)
                if self.state == BOMB:
                    #print("expected bomb values injected")
                    expected = self.bomb(wrld, next[0], next[1])
                new_cost = cost_so_far[(self.x, self.y)] + 1 - expected
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + (20 - self.get_distance_to_exit(next, self.exit_position))
                    frontier.put((next[0], next[1]), priority)
                    self.came_from[next] = current

    def exp_value(self, wrld, exit_position, char_x, char_y, monster_x, monster_y, depth):
        if (char_x, char_y) == exit_position:
            return 100000
        value = 0
        monster_moves = self.get_possible_moves(monster_x, monster_y, wrld)
        for move in monster_moves:
            prob = 1 / len(monster_moves)
            v = self.max_value(wrld, exit_position, char_x, char_y, move[0], move[1], depth)
            value = value + prob * v
        return value

    def max_value(self, wrld, exit_position, char_x, char_y, monster_x, monster_y, depth):
        if (char_x, char_y) == (monster_x, monster_y):
            return -100000
        elif depth > 0:
            return -1 * self.get_distance_to_exit((char_x, char_y), (monster_x, monster_y))
        value = -1000000000
        character_moves = self.get_possible_moves(char_x, char_y, wrld)
        for move in character_moves:
            value = max(value, self.exp_value(wrld, exit_position, move[0], move[1], monster_x, monster_y, depth + 1))
        return value

    def find_next_move(self, came_from, exit_position):
        next_move = exit_position

        if(exit_position in came_from.keys()):
            while came_from[next_move] is not (self.x, self.y):
                if came_from[next_move] == (self.x, self.y):
                    break
                next_move = came_from[next_move]
        elif(self.state is NORMAL or self.state is BLOCKED):
            self.state = BLOCKED


        return next_move

    def bomb(self, wrld, char_x, char_y):
        value = 0
        # print("Bomb has been called")
        bombs = []
        # grab the list of bombs
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                bomb = wrld.bomb_at(x, y)
                if (bomb is not None):
                    bombs.append(bomb)
        # check if on axis and assign value for expected
        if (len(bombs) == 0):
            self.state = NORMAL
            return 0
        else:
            for bomb in bombs:
                dist = self.get_chebyshev((bomb.x, bomb.y), (char_x, char_y))
                if (dist < 4):
                    if (abs(bomb.x - char_x) == abs(bomb.y - char_y)):
                        # on the diagonal axis
                        value -= (100000 - dist)
                    elif(abs(bomb.x - char_x) == 0):
                        # on the same y axis
                        value -= 100000 - dist
                    elif(abs(bomb.y - char_y) == 0):
                        # on the same x axis
                        value -= 100000 - dist
                    else:
                        return 0

        return value



    def get_possible_moves(self, x, y, wrld):
        array = []
        for dx in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            if (x + dx >= 0) and (x + dx < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    # Make sure the monster is moving
                    # if (dx != 0) or (dy != 0):
                    # Avoid out-of-bound indexing
                    if (y + dy >= 0) and (y + dy < wrld.height()):
                        # No need to check impossible moves
                        if not wrld.wall_at(x + dx, y + dy):
                            array.append((x + dx, y + dy))
        return array

    def get_distance_to_exit(self, position, exit_position):
        return math.sqrt((position[1] - exit_position[1]) * (position[1] - exit_position[1]) +
                        (position[0] - exit_position[0]) * (position[0] - exit_position[0]))

    def get_chebyshev(self, position, exit_position):
        return max(abs(position[0] - exit_position[0]), abs(position[1] - exit_position[1]))


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
