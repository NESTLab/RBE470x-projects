from world import World
from sensed_world import SensedWorld
from events import Event

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
        self.scores[c.name] = -self.time

    ###################
    # Private methods #
    ###################

    def next(self):
        """Returns a new world state, along with the events that occurred"""
        self.time = self.time - 1
        self.update_explosions()
        ev = self.update_bombs()
        ev = ev + self.update_monsters()
        ev = ev + self.update_characters()
        self.manage_events_and_scores(ev)
        self.events = ev
        return (self,ev)

    def update_monsters(self):
        """Update monster state"""
        # Event list
        ev = []
        # Update all the monsters
        nmonsters = {}
        for i, mlist in self.monsters.items():
            for m in mlist:
                # Call AI
                m.do(SensedWorld.from_world(self))
                # Update position and check for events
                ev2 = self.update_monster_move(m, False)
                ev = ev + ev2
                # Monster gets inserted in next step's list unless hit
                if not (ev2 and ev2[0].tpe == Event.BOMB_HIT_MONSTER):
                    # Update new index
                    ni = self.index(m.x, m.y)
                    np = nmonsters.get(ni, [])
                    np.append(m)
                    nmonsters[ni] = np
        # Save new index
        self.monsters = nmonsters
        # Return events
        return ev

    def update_characters(self):
        """Update character state"""
        # Event list
        ev = []
        # Update all the characters
        ncharacters = {}
        for i, clist in self.characters.items():
            for c in clist:
                # Call AI
                c.do(SensedWorld.from_world(self))
                # Attempt to place bomb
                if c.maybe_place_bomb:
                    c.maybe_place_bomb = False
                    can_bomb = True
                    # Make sure this character has not already placed another bomb
                    for k,b in self.bombs.items():
                        if b.owner == c:
                            can_bomb = False
                            break
                    if can_bomb:
                        self.add_bomb(c.x, c.y, c)
                # Update position and check for events
                ev2 = self.update_character_move(c, False)
                ev = ev + ev2
                # Character gets inserted in next step's list unless hit or
                # escaped
                if not (ev2 and ev2[0].tpe in [Event.BOMB_HIT_CHARACTER, Event.CHARACTER_FOUND_EXIT]):
                    # Update new index
                    ni = self.index(c.x, c.y)
                    np = ncharacters.get(ni, [])
                    np.append(c)
                    ncharacters[ni] = np
        # Save new index
        self.characters = ncharacters
        # Return events
        return ev
