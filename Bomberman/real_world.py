import cell
import world

class RealWorld(world.World):
    """The real world state"""

    def add_exit(self, x, y):
        """Adds an exit cell at (x,y)"""
        self.exitcell = (x,y)

    def add_wall(self, x, y):
        """Adds a wall cell at (x,y)"""
        self.grid[x][y] = True

    def add_monster(self, m):
        """Adds the given monster to the world"""
        self.monsters[self.index(m.x,m.y)] = m

    def add_character(self, c):
        """Adds the given character to the world"""
        self.characters[self.index(c.x,c.y)] = c

    def next(self):
        """Returns a new world state, along with the events that occurred"""
        new = self.from_world(self)
        new.time = new.time - 1
        new.update_explosions()
        ev = new.update_bombs()
        ev = new.update_monsters()
        ev = new.update_characters()
        return (new,ev)

    def update_monsters(self):
        """Update monster state"""
        return []

    def update_characters(self):
        """Update character state"""
        return []
