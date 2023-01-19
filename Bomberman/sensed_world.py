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
        mmapping = {}
        for k, omonsters in wrld.monsters.items():
            # Make a new list of monsters at k
            nmonsters = []
            # Create a new generic monster for each monster
            # This way, every monster instance can be manipulated individually
            for m in omonsters:
                nm = MonsterEntity.from_monster(m)
                nmonsters.append(nm)
                mmapping[m] = nm
            # Set list of monsters at k
            new.monsters[k] = nmonsters
        # Copy characters, scores, and build a mapping between old and new
        cmapping = {}
        for k, ocharacters in wrld.characters.items():
            # Make a new list of characters at k
            ncharacters = []
            # Create a new generic character for each character
            # This way, every character instance can be manipulated individually
            # Plus, you can't peek into other characters' variables
            for oc in ocharacters:
                # Add to new list of characters
                nc = CharacterEntity.from_character(oc)
                ncharacters.append(nc)
                # Add to mapping
                cmapping[oc] = nc
            new.characters[k] = ncharacters
        # Copy bombs
        for k, ob in wrld.bombs.items():
            c = cmapping.get(ob.owner, ob.owner)
            new.bombs[k] = BombEntity(ob.x, ob.y, ob.timer, c)
        # Copy explosions
        for k, oe in wrld.explosions.items():
            c = cmapping.get(oe.owner)
            if c:
                new.explosions[k] = ExplosionEntity(oe.x, oe.y, oe.timer, c)
        # Copy events
        for e in wrld.events:
            # Create a new event
            # Tricky: if the character related to the event has died, duplicate the original character
            newev = Event(e.tpe, cmapping.get(e.character, CharacterEntity.from_character(e.character)))
            # Manage other attribute
            if e.tpe == Event.BOMB_HIT_MONSTER:
                newev.other = MonsterEntity.from_monster(e.other)
            elif e.tpe == Event.BOMB_HIT_CHARACTER:
                newev.other = CharacterEntity.from_character(e.other)
            elif e.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                newev.other = mmapping.get(e.other, MonsterEntity.from_monster(e.other))
            new.events.append(newev)
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
        new.events = new.update_bombs() + new.update_monsters() + new.update_characters()
        new.update_scores()
        new.manage_events()
        return (new, new.events)

    ###################
    # Private methods #
    ###################

    def aientity_do(self, entities):
        """Call AI to get actions for next step"""
        for i, elist in entities.items():
            for e in elist:
                # Call AI
                e.do(None)

    def manage_events(self):
        for e in self.events:
            if e.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                self.remove_character(e.character)
