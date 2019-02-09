# import sys
# sys.path.insert(0, '..')
from entity import MonsterEntity
import random

class StupidMonster(MonsterEntity):
    """A pretty stupid monster"""

    def look_for_empty_cell(self, wrld):
        # List of empty cells
        cells = []
        # Go through neighboring cells
        for dx in [-1, 0, 1]:
            # Avoid out-of-bounds access
            if ((self.x + dx >= 0) and (self.x + dx < wrld.width())):
                for dy in [-1, 0, 1]:
                    # Avoid out-of-bounds access
                    if ((self.y + dy >= 0) and (self.y + dy < wrld.height())):
                        # Is this cell walkable?
                        if not wrld.wall_at(self.x + dx, self.y + dy):
                            cells.append((dx, dy))
        # All done
        return cells

    def do(self, wrld):
        """Pick an action for the monster"""
        # Get list of safe moves
        safe = self.look_for_empty_cell(wrld)
        # Pick a move at random
        (dx, dy) = random.choice(safe)
        self.move(dx, dy)
