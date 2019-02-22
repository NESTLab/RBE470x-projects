# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import heapq
import operator


class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
        goal = self.get_exit(wrld)
        start = self.get_my_location(wrld)
        bomb = self.get_bomb(wrld)
        x_dir, y_dir = self.get_direction(start, wrld)
        monster = self.get_monster(wrld)
        next_move = self.a_star(wrld, start, goal) # returns (x,y) coordinate of next move
        dx = next_move[0] - start[0]
        dy = next_move[1] - start[1]

        monstersNear = self.check_monster(start, wrld) # list of monsters near

        try:
            if wrld.wall_at(start[0], start[1] + 1) and not wrld.next()[0].explosion_at(start[0] - 1, start[1] - 1):
                print("STATE: 1")
                self.place_bomb()
                self.move(-1, -1)

            elif monstersNear:
                # STATE: MONSTER ( There are a monsters within our range)
                print("STATE: MONSTER")
                self.place_bomb()
                print("My current position is:")
                print(start[0], start[1])
                monster_move_away = self.bestMove_Monster(start,wrld, monstersNear)
                dx = monster_move_away[0] - start[0]
                dy = monster_move_away[1] - start[1]
                print("Move: {}, {}".format(dx, dy))
                self.move(dx, dy)

            # elif monster_move_away[0] != 0 and monster_move_away[1] != 0:
            #     print('monster_move_away')
            #     self.place_bomb()
            #     self.move(*monster_move_away)
            elif wrld.wall_at(*next_move) or wrld.next()[0].explosion_at(*start):
                print("STATE: 3")
                self.move(x_dir, y_dir)
            elif next_move[0] == bomb[0] or next_move[1] == bomb[1] or wrld.explosion_at(*next_move):
                print("STATE: 4")
                self.move(0, 0)
            else:
                print("STATE: 5")
                self.move(dx, dy)
        except IndexError:
            pass


    # Becareful of multiple monsters
    # RETURN [list of (int x, int y)]: coordinate positions of monsters within range
    @staticmethod
    def check_monster(start, wrld):
        dx = 0
        dy = 0
        monstersNear = [] # list of tuples (int x, int y)
        for x in range(-4, 4):
            for y in range(-4, 4):
                if wrld.monsters_at(start[0] + x, start[1] + y):
                    # monster was found
                    monstersNear.append((start[0] + x, start[1] + y))
                    # dx = start[0] - (start[0] + x)
                    # dy = start[1] - (start[1] + y)
                    # if dx < 0:
                    #     dx = -1
                    # else:
                    #     dx = 1
                    # if dy < 0:
                    #     dy = -1
                    # else:
                    #     dy = 1
                    # return dx, dy
        return monstersNear

    # PARAM [SensedWorld] wrld: wrld grid, used to get boundries
    # RETURN (int x, int y): best next move coordinates taking in account monsters and bomb range
    def bestMove_Monster(self, start, wrld, monsterList):
        moves = self.get_neighbors(start, wrld) # possible moves within board bounds (no need to check for bounds again)
        moves.append(start)
        result = []
        newWorld = wrld.next()[0]

        # filter out next moves that are walls or have an explosion in the next board configuration
        for neighbor in moves:
            # print("Is there a explosion???")
            # print(wrld.next()[0].explosion_at(*neighbor))
            # if wrld.wall_at(*neighbor) or newWorld.explosion_at(*neighbor) or newWorld.monsters_at(*
            # todo TO CHECK FOR EXPLOSION IN THE BOARD WE DONT NEED TO GET THE NEXT BOARD
            if wrld.wall_at(*neighbor) or wrld.explosion_at(*neighbor):
            # if wrld.wall_at(*neighbor) or wrld.explosion_at(*neighbor):
                print("Found wall or explosion")
            elif newWorld.explosion_at(*neighbor):
            # elif wrld.explosion_at(*neighbor):
                print("Im a a explotion at: ")
                print(*neighbor)
            else:
                print("Neighbor is not wall or explosion")
                result.append(neighbor)

        if not result:
            # there is no escape, you are dead
            print("WE DIEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            return 0,0
        return self.a_star_monsters(wrld,result,monsterList)


    @staticmethod
    def get_direction(start, wrld):
        x = 1
        y = 1
        if start[0] > wrld.width()/2:
            x = -1
        if start[1] > wrld.height()/2:
            y = -1
        if wrld.wall_at(start[0] + x, start[1] + y):
            return 0, 1
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

    # @staticmethod
    # def make_graph(wrld):
    #     graph_wrld = [wrld.width][wrld.height]
    #
    #     for i in range(0, wrld.width):
    #         for j in range(0, wrld.height):
    #             if wrld(i, j)

    # PARAM [tuple (int, int)] start: tuple with x and y coordinates of current position in board
    # PARAM [SensedWorld] wrld: wrld grid, used to get boundries
    # RETURN [list of (int x, int y)]: coordinate positions of neighbors including walls
    def get_neighbors(self, start, wrld):
        x = start[0]
        y = start[1]
        neighbors = [(x+1, y), (x, y-1), (x-1, y), (x, y+1),
                     (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
        result = []
        # check that neighbors are inside wrld bounds
        for neighbor in neighbors:
            if 0 <= neighbor[0] < wrld.width() and 0 <= neighbor[1] < wrld.height():
                result.append(neighbor)
        return result

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
    def heuristic(start, goal):
        (x1, y1) = start
        (x2, y2) = goal

        # Euclidean distance is the hypotenuse
        # We add the squared values, and finding the sqrt is
        # not necessary as it will never effect the outcome
        value = (x2 - x1)**2 + (y2 - y1)**2
        return value

    # this a* algorithm picks the *CLOSEST* distance to the goal
    # PARAM [SensedWorld] wrld: wrld grid, used to get boundries
    # PARAM [tuple (int, int)] start: tuple with x and y coordinates of starting position in board
    # PARAM [tuple (int, int)] goal: tuple with x and y coordinates of exit position in board
    # RETURN [?????]: Possibly return list with tuples of (int, int). This would be the optimal path to traverse
    def a_star(self, wrld, start, goal):
        neighbors = self.get_neighbors(start, wrld)
        neighbors_values = []
        for neighbor in neighbors:
            neighbors_values.append((neighbor[0], neighbor[1], self.heuristic(neighbor, goal)))
        neighbors_values.sort(key=operator.itemgetter(2))
        print(neighbors_values)

        return neighbors_values[0][0], neighbors_values[0][1]

    # this a* algorithm picks the *FURTHEST* distance to the goal (monster)
    # todo what to do if there are two monsters??
    # RETURN [(int x, int y)]: Returns best move to do
    def a_star_monsters(self, wrld, possibleMoves, monsterList):
        neighbors_values = []
        for neighbor in possibleMoves:
            # todo change this to accept multiple monsters
            neighbors_values.append((neighbor[0], neighbor[1], self.heuristic(neighbor, monsterList[0])))
        # sort by distance to monster. Its in DECREASING order.
        neighbors_values.sort(key=operator.itemgetter(2))
        print("Monster A* values: ")
        print(neighbors_values)
        # pick the furthest values
        return neighbors_values[-1][0], neighbors_values[-1][1]
