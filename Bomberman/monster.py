import cell
import entity
import random

class Monster(entity.AIEntity, entity.MovableEntity):
    """A pretty stupid monster"""

    def look_for_character(self, wrld):
        for dx in [-1, 0, 1]:
            # Avoid out-of-bounds access
            if ((self.x + dx >= 0) and (self.x + dx < len(wrld))):
                for dy in [-1, 0, 1]:
                    # Avoid out-of-bounds access
                    if ((self.y + dy >= 0) and (self.y + dy < len(wrld[0]))):
                        # Is a character at this position?
                        if (wrld[self.x + dx][self.y + dy] == cell.Cell.CHARACTER):
                            return (True, dx, dy)
        # Nothing found
        return (False, 0, 0)

    def going_to_die(self, wrld):
        # Get next desired position
        (nx, ny) = self.nextpos()
        # If next pos is out of bounds, must change direction
        if ((nx < 0) or (nx >= len(wrld)) or
            (ny < 0) or (ny >= len(wrld[0]))):
            return True
        # Get data of current cell
        cc = wrld[self.x][self.y]
        # Get data of next cell
        nc = wrld[nx][ny]
        # If these cells are an explosion, a wall, or a monster, go away
        return ((cc == cell.Cell.EXPLOSION) or
                (nc in [cell.Cell.WALL, cell.Cell.EXPLOSION, cell.Cell.MONSTER, cell.Cell.EXIT]))

    def look_for_empty_cell(self, wrld):
        # List of empty cells
        cells = []
        # Go through neighboring cells
        for dx in [-1, 0, 1]:
            # Avoid out-of-bounds access
            if ((self.x + dx >= 0) and (self.x + dx < len(wrld))):
                for dy in [-1, 0, 1]:
                    # Avoid out-of-bounds access
                    if ((self.y + dy >= 0) and (self.y + dy < len(wrld[0]))):
                        # Is this cell safe?
                        if (wrld[self.x + dx][self.y + dy] == cell.Cell.EMPTY):
                            # Yes
                            cells.append((dx, dy))
        # All done
        return cells

    def do(self, wrld):
        """Pick an action for the monster"""
        # If a character is in the neighborhood, go to it
        (found, dx, dy) = self.look_for_character(wrld)
        if found:
            self.move(dx, dy)
            return
        # If I'm idle or going to die, change direction
        if ((self.dx == 0 and self.dy == 0) or
            self.going_to_die(wrld)):
            # Get list of safe moves
            safe = self.look_for_empty_cell(wrld)
            if not safe:
                # Accept death
                self.move(0,0)
            else:
                # Pick a move at random
                (dx, dy) = random.choice(safe)
                self.move(dx, dy)
