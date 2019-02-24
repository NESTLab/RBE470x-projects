from entity import *
from events import *
from world import World

class SensedWorld(World):
    """The world state as seen by a monster or a robot"""

    @classmethod
    def from_world(cls, wrld):
        """Create a new world state from an existing state"""
        new = cls()
        new.bomb_time     = wrld.bomb_time
        new.expl_duration = wrld.expl_duration
        new.expl_range    = wrld.expl_range
        new.exitcell      = wrld.exitcell
        new.time          = wrld.time
        # Copy grid
        new.grid          = [[wrld.wall_at(x,y) for y in range(wrld.height())] for x in range(wrld.width())]
        # Copy monsters
        for k, omonsters in wrld.monsters.items():
            # Make a new list of monsters at k
            nmonsters = []
            # Create a new generic monster for each monster
            # This way, every monster instance can be manipulated individually
            for m in omonsters:
                nmonsters.append(MonsterEntity.from_monster(m))
            # Set list of monsters at k
            new.monsters[k] = nmonsters
        # Copy characters, scores, and build a mapping between old and new
        mapping = {}
        for k, ocharacters in wrld.characters.items():
            # Make a new list of characters at k
            ncharacters = []
            # Create a new generic character for each monster
            # This way, every character instance can be manipulated individually
            # Plus, you can't peek into other characters' variables
            for oc in ocharacters:
                # Add to new list of characters
                nc = CharacterEntity.from_character(oc)
                ncharacters.append(nc)
                # Add to mapping
                mapping[oc] = nc
            new.characters[k] = ncharacters
        # Copy bombs
        for k, ob in wrld.bombs.items():
            c = mapping.get(ob.owner, ob.owner)
            new.bombs[k] = BombEntity(ob.x, ob.y, ob.timer, c)
        # Copy explosions
        for k, oe in wrld.explosions.items():
            c = mapping.get(oe.owner)
            if c:
                new.explosions[k] = ExplosionEntity(oe.x, oe.y, oe.timer, c)
        # Copy scores
        for name,score in wrld.scores.items():
            new.scores[name] = score
        return new

    def me(self, character):
        for k,clist in self.characters.items():
            for c in clist:
                if c.name == character.name:
                    return c

    def next(self):
        """Returns a new world state, along with the events that occurred"""
        new = SensedWorld.from_world(self)
        new.time = new.time - 1
        new.update_explosions()
        ev = new.update_bombs()
        ev = ev + new.update_monsters()
        ev = ev + new.update_characters()
        new.manage_events_and_scores(ev)
        new.aientity_do(self.monsters)
        new.aientity_do(self.characters)
        new.events = ev
        return (new,ev)

    ###################
    # Private methods #
    ###################

    def aientity_do(self, entities):
        """Call AI to get actions for next step"""
        for i, elist in entities.items():
            for e in elist:
                # Call AI
                e.do(None)
