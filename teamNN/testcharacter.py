# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from PriorityQueue import PriorityQueue

class TestCharacter(CharacterEntity):
    firstTime = True
    a_star_path = []

    def a_star(self, wrld, goal=None, start=None):
        if start is None:
            start = (self.x, self.y) #Start at current position
        if goal is None:
            goal = wrld.exitcell #Goal is exit cell

        cost_so_far = {start: 0} #Dictionary of costs to get to each cell
        came_from = {start: None} #Dictionary of where each cell came from

        frontier = PriorityQueue() #Priority queue of cells to visit
        frontier.put(start, 0)

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            #Check all walkable neighbors of current cell
            for neighbor in self.eight_neighbors(wrld, current[0], current[1]):
                #Calculate cost to get to neighbor - 1 or 1.4
                new_cost = cost_so_far[current] + euclidean_dist(current, neighbor)

                #If neighbor has no path or new path is better, update path
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + euclidean_dist(neighbor, goal)
                    frontier.put(neighbor, priority)
                    came_from[neighbor] = current

        #Reconstruct path using came_from dictionary
        currPos = goal
        finalPath = []
        finalPath.append(goal)
        while currPos != start:
            currPos = came_from[currPos]
            finalPath.append(currPos)

        finalPath.reverse()
        return finalPath

    def is_cell_walkable(self, wrld, x, y):
        return wrld.exit_at(x, y) or wrld.empty_at(x, y) or wrld.monsters_at(x, y)

    def eight_neighbors(self, wrld, x, y):
        """
        Returns the walkable 8-neighbors cells of (x,y) in wrld
        """
        return_list = []

        if x != 0 and self.is_cell_walkable(wrld, x - 1, y):
            return_list.append((x - 1, y))
        if x != wrld.width() - 1 and self.is_cell_walkable(wrld, x + 1, y):
            return_list.append((x + 1, y))
        if y != 0 and self.is_cell_walkable(wrld, x, y - 1):
            return_list.append((x, y - 1))
        if y != wrld.height() - 1 and self.is_cell_walkable(wrld, x, y + 1):
            return_list.append((x, y + 1))
        if x != 0 and y != 0 and self.is_cell_walkable(wrld, x - 1, y - 1):
            return_list.append((x - 1, y - 1))
        if x != wrld.width() - 1 and y != 0 and self.is_cell_walkable(wrld, x + 1, y - 1):
            return_list.append((x + 1, y - 1))
        if y != wrld.height() - 1 and x != 0 and self.is_cell_walkable(wrld, x - 1, y + 1):
            return_list.append((x - 1, y + 1))
        if x != wrld.width() - 1 and y != wrld.height() - 1 and self.is_cell_walkable(wrld, x + 1, y + 1):
            return_list.append((x + 1, y + 1))

        return return_list

    def manhattan_distance_to_exit(self, wrld):
        return abs(self.x - wrld.exitcell[0]) + abs(self.y - wrld.exitcell[1])

    def euclidean_distance_to_exit(self, wrld):
        return ((self.x - wrld.exitcell[0])**2 + (self.y - wrld.exitcell[1])**2)**0.5

    def a_star_distance_to_exit(self, wrld):
        return len(self.a_star(wrld))

    def manhattan_distance_to_monster(self, wrld):
        if len(wrld.monsters) == 0:
            return 0
        else:
            return min([abs(self.x - monster[1][0].x) + abs(self.y - monster[1][0].y) for monster in wrld.monsters.items()])

    def euclidean_distance_to_monster(self, wrld):
        if len(wrld.monsters) == 0:
            return 0
        else:
            return min([((self.x - monster[1][0].x)**2 + (self.y - monster[1][0].y)**2)**0.5 for monster in wrld.monsters.items()])
    def a_star_distance_to_monster(self, wrld):

        if len(wrld.monsters) == 0:
            return 0
        else:
            return min([len(self.a_star(wrld, (monster[1][0].x,monster[1][0].y))) for monster in wrld.monsters.items()])


    def do(self, wrld):
        if self.firstTime:
            print("Character at", self.x, self.y)
            print("Exit at", wrld.exitcell)
            print("Explosions:", wrld.explosions)
            print("Monsters:", wrld.monsters)
            print("Euclidean distance to exit:", self.euclidean_distance_to_exit(wrld))
            print("Manhattan distance to exit:", self.manhattan_distance_to_exit(wrld))
            print("A* distance to exit:", self.a_star_distance_to_exit(wrld))
            print("Euclidean distance to monster:", self.euclidean_distance_to_monster(wrld))
            print("Manhattan distance to monster:", self.manhattan_distance_to_monster(wrld))
            print("A* distance to monster:", self.a_star_distance_to_monster(wrld))
            self.a_star_path = self.a_star(wrld)
            print("A* path to goal:", self.a_star_path)

            for point in self.a_star_path:
                #Mark path on world
                self.set_cell_color(point[0],point[1], Fore.RED + Back.GREEN)
            self.firstTime = False
        else:
            nextCell = self.a_star_path.pop(0)
            self.move(nextCell[0] - self.x, nextCell[1] - self.y)


def euclidean_dist(point_one, point_two):
    return ((point_one[0] - point_two[0]) ** 2 + (point_one[1] - point_two[1]) ** 2) ** 0.5