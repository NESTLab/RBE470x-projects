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
STAY = 5



class TestCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        super().__init__(name, avatar, x, y)
        self.exit_position = None
        self.start = (self.x, self.y)
        self.came_from = {self.start: (None, 0)}
        self.state = NORMAL
        self.prev_state = None
        self.stillness_counter = 0
        self.lastx = 0
        self.lasty = 0
        self.dist_min = 1000000

    def do(self, wrld):
        if self.exit_position is None:
            for x in range(0, wrld.width()):
                for y in range(0, wrld.height()):
                    if wrld.exit_at(x, y):
                        self.exit_position = (x, y)
                        break
                if self.exit_position is not None:
                    break

        monsters = []
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                monster = wrld.monsters_at(x, y)
                if monster is not None:
                    monsters.append(monster)
        self.dist_min = 1000000
        for monster in monsters:
            temp_dist = self.get_chebyshev((monster[0].x, monster[0].y), (self.x, self.y))
            if temp_dist < self.dist_min:
                self.dist_min = temp_dist

        self.prev_state = self.state
        if(self.dist_min < 6):
            self.state = MONSTER
        else:
            self.state = NORMAL

        frontier = PQueue()
        frontier.put((self.x, self.y), 0)
        cost_so_far = {(self.x, self.y): 0}
        print("state: ", self.state)
        print("prev_state: ", self.prev_state)

        if self.state == (NORMAL) or self.state == BLOCKED:
            if self.x == self.start[0] and self.y == self.start[1] or self.prev_state is not NORMAL:
                self.a_star(frontier, cost_so_far, wrld, None)
        elif self.state == MONSTER:
            self.a_star(frontier, cost_so_far, wrld, monster)
        elif self.state == BOMB:
            self.a_star(frontier, cost_so_far, wrld, None)

        next_move = self.find_next_move(self.came_from, self.exit_position, wrld)

        if (self.lastx == self.x and self.lasty == self.y):
            self.stillness_counter += 1
        else:
            self.stillness_counter = 0
            self.lastx = self.x
            self.lasty = self.y
        print("stillness_counter: ", self.stillness_counter)

        if (self.stillness_counter == 3):
            # drop a bomb
            self.place_bomb()
            curr_state = self.state
            self.prev_state = curr_state
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
                if self.state == MONSTER and self.dist_min<6:
                    expected = self.exp_value(wrld, self.exit_position, next[0], next[1], monster[0].x, monster[0].y, 0)
                # if self.state == BOMB:
                #     #print("expected bomb values injected")
                #     expected = self.bomb(wrld, next[0], next[1])
                new_cost = cost_so_far[(current[0], current[1])] + 1 - expected
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + (20 - self.get_distance_to_exit(next, self.exit_position))
                    frontier.put((next[0], next[1]), priority)
                    self.came_from[next] = (current, priority)

    def exp_value(self, wrld, exit_position, char_x, char_y, monster_x, monster_y, depth):
        if (char_x, char_y) == exit_position:
            return 00000
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

    def find_next_move(self, came_from, exit_position, wrld):
        next_move = exit_position

        # list of possible moves for other circumstances
        possible_moves = self.get_possible_moves(self.x, self.y, wrld)
        move_values = [0] * len(possible_moves)
        monsters = []  # list of monsters in map
        explosions = []  # list of explosions in map
        bombs = []  # list of bombs in map

        # check for presence of all important entities
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                monster = wrld.monsters_at(x, y)
                explosion = wrld.explosion_at(x, y)
                bomb = wrld.bomb_at(x, y)

                if monster is not None:
                    monsters.append(monster)
                if explosion is not None:
                    explosions.append((x, y))
                if bomb is not None:
                    bombs.append(bomb)

        # no monsters and path not blocked
        if(exit_position in came_from.keys()):
            if len(monsters) == 0:
                self.state = NORMAL
            else:
                self.state = MONSTER
            while came_from[next_move][0] is not (self.x, self.y):
                if came_from[next_move][0] == (self.x, self.y):
                    break
                next_move = came_from[next_move][0]

        else:
            self.state = BLOCKED
            move_values = self.find_blocked_value(wrld, exit_position, possible_moves, move_values)
            # if bombs present:
            if len(bombs) > 0:
                move_values = self.find_bomb_value(wrld, bombs, possible_moves, move_values)
            # if explosions present:
            if len(explosions) > 0:
                self.stillness_counter = 0
                move_values = self.find_explosion_value(wrld, explosions, possible_moves, move_values)
            # if monsters present:
            if len(monsters) > 0:
                move_values = self.find_monster_value(wrld, monsters, exit_position, possible_moves, move_values)

            # find max value for moves
            max = 0
            max_value = -1000000000
            for i in range(len(move_values)):
                if move_values[i] > max_value:
                    max_value = move_values[i]
                    max = i

            print("max: ", max)
            print(move_values)
            print(possible_moves)

            # return move with max value
            next_move = possible_moves[max]

        print(next_move)
        return next_move


    def find_explosion_value(self, wrld, explosions, possible_moves, move_values):
        for i in range(len(possible_moves)):
            for explosion in explosions:
                if self.get_chebyshev((possible_moves[i]), (explosion[0], explosion[1])) == 0:
                    move_values[i] -= 100


        return move_values

    def find_monster_value(self, wrld, monsters, exit_position, possible_moves, move_values):
        dist_min = 1000000
        for monster in monsters:
            dist = self.get_chebyshev((monster[0].x, monster[0].y), (self.x, self.y))
            if dist < dist_min:
                dist_min = dist
        if dist > 6:
            return move_values

        for i in range(len(possible_moves)):
            for monster in monsters:
                monster_moves = self.get_smart_monster_move(monster[0], wrld)
                if (len(monster_moves) > 1):
                    for monster_move in monster_moves:
                        temp_val = self.exp_value(wrld, exit_position, possible_moves[i][0], possible_moves[i][1], monster_move[0], monster_move[1], 1)
                        dist = self.get_chebyshev((monster_move[0], monster_move[1]), possible_moves[i])
                        if dist < 5:
                            move_values[i] += 2 * temp_val
                        else:
                            move_values[i] += temp_val / 2
                else:
                    dist = self.get_manhattan((monster_moves[0][0], monster_moves[0][1]), possible_moves[i])
                    if dist < 5:
                        move_values[i] -= 50 - dist


        return move_values



    def find_blocked_value(self, wrld, exit_position, possible_moves, move_values):
        for i in range(len(possible_moves)):
            move_values[i] += 60 - (3 * self.get_chebyshev(possible_moves[i], exit_position))
        return move_values


    def find_bomb_value(self, wrld, bombs, possible_moves, move_values):

        for i in range(len(possible_moves)):
            value = 0

            for bomb in bombs:
                dist = self.get_chebyshev((bomb.x, bomb.y), possible_moves[i])

                if (dist < 5):
                    if (abs(bomb.x - possible_moves[i][0]) == 0):
                        # on the same y axis
                        value -= 8 - dist
                        if bomb.timer <= 1:
                            value -= 100
                    elif (abs(bomb.y - possible_moves[i][1]) == 0):
                        # on the same x axis
                        value -= 8 - dist
                        if bomb.timer <= 1:
                            value -= 100
                    # else:
                    #     return 100 - self.get_chebyshev((bomb.x, bomb.y), (char_x, char_y))

            move_values[i] += value

        return move_values

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
            self.state = STAY
            self.prev_state = BOMB
            return 0
        else:
            for bomb in bombs:
                dist = self.get_chebyshev((bomb.x, bomb.y), (char_x, char_y))
                if (dist < 4):
                    if(abs(bomb.x - char_x) == 0):
                        # on the same y axis
                        value -= 5 - dist
                    elif(abs(bomb.y - char_y) == 0):
                        # on the same x axis
                        value -= 5 - dist
                    else:
                        return 100 - self.get_chebyshev((bomb.x, bomb.y), (char_x, char_y))

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

    def get_smart_monster_move(self, monster, wrld):
        array = []
        if not wrld.wall_at(monster.x + monster.dx, monster.y + monster.dy):
            array.append((monster.x + monster.dx, monster.y + monster.dy))
            return array
        else:
            for dx in [-1, 0, 1]:
                # Avoid out-of-bound indexing
                if (monster.x + dx >= 0) and (monster.x + dx < wrld.width()):
                    # Loop through delta y
                    for dy in [-1, 0, 1]:
                        # Make sure the monster is moving
                        if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                            if (monster.y + dy >= 0) and (monster.y + dy < wrld.height()):
                                # No need to check impossible moves
                                if not wrld.wall_at(monster.x + dx, monster.y + dy):
                                    array.append((monster.x + dx, monster.y + dy))
        return array

    def get_smart_monster_future(self, monster, wrld):
        future_positions = []
        temp = self.get_smart_monster_move(monster, wrld)
        future_positions.append(temp[0])


    def get_distance_to_exit(self, position, exit_position):
        return math.sqrt((position[1] - exit_position[1]) * (position[1] - exit_position[1]) +
                        (position[0] - exit_position[0]) * (position[0] - exit_position[0]))

    def get_chebyshev(self, position, exit_position):
        return max(abs(position[0] - exit_position[0]), abs(position[1] - exit_position[1]))

    def get_manhattan(self, position, exit_position):
        return (abs(position[0] - exit_position[0]) + abs(position[1]) - exit_position[1])


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
