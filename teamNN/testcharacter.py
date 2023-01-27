# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from PriorityQueue import PriorityQueue

class TestCharacter(CharacterEntity):

    def a_star(self, wrld):
        pQueue = PriorityQueue()

    def look_for_empty_cells(self, wrld):
        # List of empty cells
        cells = []
        # Go through neighboring cells
        for dx in [-1, 0, 1]:
            # Avoid out-of-bounds access
            if ((self.x + dx >= 0) and (self.x + dx < wrld.width())):
                for dy in [-1, 0, 1]:
                    # Avoid out-of-bounds access
                    if ((self.y + dy >= 0) and (self.y + dy < wrld.height())):
                        # Is this cell safe?
                        if(wrld.exit_at(self.x + dx, self.y + dy) or
                           wrld.empty_at(self.x + dx, self.y + dy)):
                            # Yes
                            cells.append((dx, dy))
        # All done
        return cells

    def do(self, wrld):
        """Pick an action for the agent"""
        print("Doing something")
        print("Character at", self.x, self.y)
        print("Exit at", wrld.exitcell)
        print("Explosions:", wrld.explosions)
        print("Monsters:", wrld.monsters)
        print("Empty cells:", self.look_for_empty_cells(wrld))



