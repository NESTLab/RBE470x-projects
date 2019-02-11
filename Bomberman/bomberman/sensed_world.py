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
        new.events = ev
        return (new,ev)

    ###################
    # Private methods #
    ###################

    def update_monsters(self):
        """Update monster state"""
        # Event list
        ev = []
        # Update all the monsters
        nmonsters = {}
        for i, mlist in self.monsters.items():
            for m in mlist:
                # Call AI
                m.do(None)
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
                c.do(None)
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
