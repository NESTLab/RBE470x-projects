from world import World
from sensed_world import SensedWorld

class RealWorld(World):
    """The real world state"""

    def add_exit(self, x, y):
        """Adds an exit cell at (x,y)"""
        self.exitcell = (x,y)

    def add_wall(self, x, y):
        """Adds a wall cell at (x,y)"""
        self.grid[x][y] = True

    def add_monster(self, m):
        """Adds the given monster to the world"""
        self.monsters[self.index(m.x,m.y)] = [m]

    def add_character(self, c):
        """Adds the given character to the world"""
        self.characters[self.index(c.x,c.y)] = [c]

    def next(self):
        """Returns a new world state, along with the events that occurred"""
        new = self.from_world(self)
        new.time = new.time - 1
        new.update_explosions()
        ev = new.update_bombs()
        sensed = SensedWorld.from_world(self)
        ev = ev + new.update_monsters(sensed)
        ev = ev + new.update_characters(sensed)
        return (new,ev)

    def update_monsters(self, wrld):
        """Update monster state"""
        # Event list
        ev = []
        # Update all the monsters
        nmonsters = {}
        for i, mlist in self.monsters.items():
            for m in mlist:
                # Call AI
                m.do(wrld)
                # Update position and check for events
                ev = ev + self.update_monster_move(m, False)
                # Update new index
                ni = self.index(m.x, m.y)
                np = nmonsters.get(ni, [])
                np.append(m)
                nmonsters[ni] = np
        # Save new index
        self.monsters = nmonsters
        # Return events
        return ev

    def update_characters(self, wrld):
        """Update character state"""
        # Event list
        ev = []
        # Update all the characters
        ncharacters = {}
        for i, clist in self.characters.items():
            for c in clist:
                # Call AI
                c.do(wrld)
                # Update position and check for events
                ev = ev + self.update_character_move(c, False)
                # Update new index
                ni = self.index(c.x, c.y)
                np = ncharacters.get(ni, [])
                np.append(c)
                ncharacters[ni] = np
        # Save new index
        self.characters = ncharacters
        # Return events
        return ev
