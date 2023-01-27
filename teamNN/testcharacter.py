# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from PriorityQueue import PriorityQueue

class TestCharacter(CharacterEntity):

    def a_star(self, wrld):
        start = (self.x, self.y)
        goal = wrld.exitcell
        cost_so_far = {start: 0}
        came_from = {start: None}

        frontier = PriorityQueue()
        frontier.put(start, 0)

        while not frontier.empty():
            current = frontier.get()
            # print()
            # print("------ Iteration ------ ")
            # print("current: ", current)
            # print("goal: ", goal)
            # print("cost_so_far: ", cost_so_far)
            # print("came_from: ", came_from)
            # print("frontier: ", frontier.get_queue())

            if current == goal:
                break

            for neighbor in self.eight_neighbors(wrld, current[0], current[1]):
                new_cost = cost_so_far[current] + euclidean_dist(current, neighbor)

                #Update cost if lower
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + euclidean_dist(neighbor, goal)
                    frontier.put(neighbor, priority)
                    # print("Added ",neighbor, " to Frontiner")
                    came_from[neighbor] = current

        print("A* is done")
        currPos = goal
        finalPath = []
        finalPath.append(goal)
        while currPos != start:
            currPos = came_from[currPos]
            finalPath.append(currPos)

        finalPath.reverse()
        return finalPath

    def is_cell_walkable(self, wrld, x, y):
        return wrld.exit_at(x, y) or wrld.empty_at(x, y)


    def eight_neighbors(self, wrld, x, y):
        """
        Returns the walkable 8-neighbors cells of (x,y) in the occupancy grid.
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

    def do(self, wrld):
        """Pick an action for the agent"""
        print("Doing something")
        print("Character at", self.x, self.y)
        print("Exit at", wrld.exitcell)
        print("Explosions:", wrld.explosions)
        print("Monsters:", wrld.monsters)
        # print("Empty cells (None, None):", self.eight_neighbors(wrld))
        # print("Empty cells (0,0):", self.eight_neighbors(wrld, 0, 0))
        # print("Empty cells (1,0):", self.eight_neighbors(wrld, 1, 0))
        # print("Empty cells (1,0):", self.eight_neighbors(wrld, 2, 0))
        # print("Empty cells (1,1):", self.eight_neighbors(wrld, 1, 1))
        print("A* path:", self.a_star(wrld))



def euclidean_dist(point_one, point_two):
    return ((point_one[0] - point_two[0]) ** 2 + (point_one[1] - point_two[1]) ** 2) ** 0.5