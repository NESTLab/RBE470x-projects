# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here

        self.move(1, 0)

        # Prints the current position of the character after the character moves
        print(self.x, self.y)

        # Find the start (current position) and goal
        start = [self.x, self.y]
        goal = self.findGoal(wrld)

        a_star_path = self.a_star_search(wrld, start,goal)

        pass


    # Finds the goal / exit to the world
    #
    # PARAM: [world] wrld: the current world configuration
    # RETURNS: [int, int] x, y: the x and y coordinates of the goal / exit
    #
    def findGoal(self, wrld):
        x = 0
        y = 0
        for y in range(wrld.height()):
            for x in range(wrld.width()):
                if(wrld.exit_at(x,y)):
                    print(x,y)
                    return [x,y]

        # Return impossible exit coordinate to signal no exit found
        print('No Exit Found')
        return [-1,-1]

    # Returns a world with the A* path marked
    #
    # PARAM: [world, [int, int], [int, int]] wrld: the current world configuration
    #                                       [start.x, start.y]: the x and y coordinated the agent is located at
    #                                       [goal.x, goal.y]: the x and y coordinated of the goal / exit
    # RETURNS: [world] newWrld: a grid world marking the A* path to the goal
    #

