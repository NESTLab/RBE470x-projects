# This is necessary to find the main code
import sys

from teamNN.utility import *

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
            start = (self.x, self.y)  # Start at current position
        if goal is None:
            goal = wrld.exitcell  # Goal is exit cell

        cost_so_far = {start: 0}  # Dictionary of costs to get to each cell
        came_from = {start: None}  # Dictionary of where each cell came from

        frontier = PriorityQueue()  # Priority queue of cells to visit
        frontier.put(start, 0)

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            # Check all walkable neighbors of current cell
            for neighbor in eight_neighbors(wrld, current[0], current[1]):
                # Calculate cost to get to neighbor - 1 or 1.4
                new_cost = cost_so_far[current] + euclidean_dist(current, neighbor)

                # If neighbor has no path or new path is better, update path
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + euclidean_dist(neighbor, goal)
                    frontier.put(neighbor, priority)
                    came_from[neighbor] = current

        # Reconstruct path using came_from dictionary
        currPos = goal
        finalPath = []
        finalPath.append(goal)
        while currPos != start:
            currPos = came_from[currPos]
            finalPath.append(currPos)

        finalPath.reverse()
        return finalPath

    def do(self, wrld):
        if self.firstTime:
            print("Character at", self.x, self.y)
            print("Exit at", wrld.exitcell)
            print("Explosions:", wrld.explosions)
            print("Monsters:", wrld.monsters)
            print("Monster Location", monster_location(wrld))
            print("Euclidean distance to exit:", euclidean_distance_to_exit(wrld))
            print("Manhattan distance to exit:", manhattan_distance_to_exit(wrld))
            print("Euclidean distance to monster:", euclidean_distance_to_monster(wrld))
            print("Manhattan distance to monster:", manhattan_distance_to_monster(wrld))
            self.a_star_path = self.a_star(wrld)
            print("A* path to goal:", self.a_star_path)

            for point in self.a_star_path:
                # Mark path on world
                self.set_cell_color(point[0], point[1], Fore.RED + Back.GREEN)
            self.firstTime = False
        else:
            nextCell = self.a_star_path.pop(0)
            self.move(nextCell[0] - self.x, nextCell[1] - self.y)
