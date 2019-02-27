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
        self.events = self.update_bombs() + self.update_monsters() + self.update_characters()
        self.update_scores()
        self.manage_events()
        return (self, self.events)

    def next_decisions(self):
        self.aientity_do(self.monsters)
        self.aientity_do(self.characters)

    def aientity_do(self, entities):
        """Call AI to get actions for next step"""
        for i, elist in entities.items():
            for e in elist:
                # Call AI
                e.do(SensedWorld.from_world(self))

    def manage_events(self):
        for e in self.events:
            if e.tpe == Event.BOMB_HIT_CHARACTER:
                e.other.done(SensedWorld.from_world(self))
            elif e.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                self.remove_character(e.character)
                e.character.done(SensedWorld.from_world(self))
            elif e.tpe == Event.CHARACTER_FOUND_EXIT:
                e.character.done(SensedWorld.from_world(self))
        
