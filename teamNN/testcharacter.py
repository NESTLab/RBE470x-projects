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

    def a_star(self, wrld):
        start = (self.x, self.y) #Start at current position
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

        print("A* is done")

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
        return wrld.exit_at(x, y) or wrld.empty_at(x, y)


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

    def do(self, wrld):
        """Pick an action for the agent"""


        if self.firstTime:
            print("Doing something")
            print("Character at", self.x, self.y)
            print("Exit at", wrld.exitcell)
            print("Explosions:", wrld.explosions)
            print("Monsters:", wrld.monsters)
            self.a_star_path = self.a_star(wrld)
            print("A* path:", self.a_star_path)
            for point in self.a_star_path:
                #Mark path on world
                self.set_cell_color(point[0],point[1], Fore.RED + Back.GREEN)
            self.firstTime = False
        else:
            nextCell = self.a_star_path.pop(0)
            # print("Next cell:", nextCell)
            self.move(nextCell[0] - self.x, nextCell[1] - self.y)
        




def euclidean_dist(point_one, point_two):
    return ((point_one[0] - point_two[0]) ** 2 + (point_one[1] - point_two[1]) ** 2) ** 0.5