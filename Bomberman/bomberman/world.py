from entity import *
from events import Event
import sys
from colorama import Fore, Back, Style

class World:

    def __init__(self):
        """Class constructor"""
        # Time for bomb to explode
        self.bomb_time = -1
        # Explosion duration
        self.expl_duration = -1
        # Explosion range
        self.expl_range = -1
        # A pointer to the exit cell, if present
        self.exitcell = None
        # Time left
        self.time = -1
        # Grid of cell types
        self.grid       = None
        # List of dynamic elements
        self.bombs      = {}
        self.explosions = {}
        self.monsters   = {}
        self.characters = {}
        # Scores
        self.scores = {}
        # Events
        self.events = []

    @classmethod
    def from_params(cls, width, height, max_time, bomb_time, expl_duration, expl_range):
        """Create a new empty world state"""
        new = cls()
        new.bomb_time     = bomb_time
        new.expl_duration = expl_duration
        new.expl_range    = expl_range
        new.time          = max_time
        new.grid          = [[False for y in range(height)] for x in range(width)]
        return new
        
    def width(self):
        """Returns the world width"""
        return len(self.grid)

    def height(self):
        """Returns the world height"""
        return len(self.grid[0])

    def empty_at(self, x, y):
        """Returns True if there is nothing at (x,y)"""
        return not (self.exit_at(x,y) or
                    self.wall_at(x,y) or
                    self.bomb_at(x,y) or
                    self.explosion_at(x,y) or
                    self.monsters_at(x,y) or
                    self.characters_at(x,y))

    def exit_at(self, x, y):
        """Returns True if there is a wall at (x,y)"""
        return self.exitcell == (x,y)

    def wall_at(self, x, y):
        """Returns True if there is a wall at (x,y)"""
        return self.grid[x][y]

    def bomb_at(self, x, y):
        """Returns the bomb at (x,y) or None"""
        return self.bombs.get(self.index(x,y))

    def explosion_at(self, x, y):
        """Returns the explosion at (x,y) or None"""
        return self.explosions.get(self.index(x,y))

    def monsters_at(self, x, y):
        """Returns the monsters at (x,y) or None"""
        return self.monsters.get(self.index(x,y))

    def characters_at(self, x, y):
        """Returns the characters at (x,y) or None"""
        return self.characters.get(self.index(x,y))

    def next(self):
        """Returns a new world state, along with the events that occurred"""
        raise NotImplementedError("Method not implemented")

    def printit(self):
        """Prints the current state of the world"""
        border = "+" + "-" * self.width() + "+\n"
        print("\nTIME LEFT: ", self.time)
        sys.stdout.write(border)
        for y in range(self.height()):
            sys.stdout.write("|")
            for x in range(self.width()):
                if self.characters_at(x,y):
                    for c in self.characters_at(x,y):
                        sys.stdout.write(Back.GREEN + c.avatar)
                elif self.monsters_at(x,y):
                    for m in self.monsters_at(x,y):
                        sys.stdout.write(Back.BLUE + m.avatar)
                elif self.exit_at(x,y):
                    sys.stdout.write(Back.YELLOW + "#")
                elif self.bomb_at(x,y):
                    sys.stdout.write(Back.MAGENTA + "@")
                elif self.explosion_at(x,y):
                    sys.stdout.write(Fore.RED + "*")
                elif self.wall_at(x,y):
                    sys.stdout.write(Back.WHITE + " ")
                else:
                    tile = False
                    for k,clist in self.characters.items():
                        for c in clist:
                            if c.tiles.get((x,y)):
                                sys.stdout.write(c.tiles[(x,y)] + ".")
                                tile = True
                                break
                    if not tile:
                        sys.stdout.write(" ")
                sys.stdout.write(Style.RESET_ALL)
            sys.stdout.write("|\n")
        sys.stdout.write(border)
        sys.stdout.flush()
        print("SCORES")
        for c,s in self.scores.items():
            print(c,s)
        print("EVENTS")
        for e in self.events:
            print(e)

    ###################
    # Private methods #
    ###################

    def index(self, x, y):
        """Returns an index used in internal dictionaries"""
        return x + y * self.width()

    def add_explosion(self, x, y, bomb):
        """Adds an explosion to the world state"""
        self.explosions[self.index(x,y)] = ExplosionEntity(x, y, self.expl_duration, bomb.owner)

    def add_bomb(self, x, y, character):
        """Adds a bomb to the world state"""
        self.bombs[self.index(x,y)] = BombEntity(x, y, self.bomb_time, character)

    def remove_character(self, character):
        # Remove character
        self.characters[self.index(character.x, character.y)].remove(character)

    def check_blast(self, bomb, x, y):
        # Check if a wall has been hit
        if self.wall_at(x, y):
            return [Event(Event.BOMB_HIT_WALL, bomb.owner)]
        # Check monsters and characters
        ev = []
        # Check if a monster has been hit
        mlist = self.monsters_at(x,y)
        if mlist:
            for m in mlist:
                ev.append(Event(Event.BOMB_HIT_MONSTER, bomb.owner, m))
                self.monsters[self.index(x,y)].remove(m)
        # Check if a character has been hit
        clist = self.characters_at(x,y)
        if clist:
            for c in clist:
                ev.append(Event(Event.BOMB_HIT_CHARACTER, bomb.owner, c))
                self.remove_character(c)
        # Return collected events
        return ev

    def add_blast_dxdy(self, bomb, dx, dy):
        # Current position
        xx = bomb.x + dx
        yy = bomb.y + dy
        # Range
        rnge = 0
        while ((rnge < self.expl_range) and
               (xx >= 0) and (xx < self.width()) and
               (yy >= 0) and (yy < self.height())):
            # Cannot destroy exit or another bomb
            if (self.exitcell == (xx,yy)) or (self.bomb_at(xx, yy)):
                return []
            # Place explosion
            self.add_explosion(xx, yy, bomb)
            # Check what has been killed, stop if so
            ev = self.check_blast(bomb, xx, yy)
            if ev:
                return ev
            # Next cell
            xx = xx + dx
            yy = yy + dy
            rnge = rnge + 1
        # No events happened
        return []

    def add_blast(self, bomb):
        """Add blast, return hit events"""
        # Add explosion at current position
        self.add_explosion(bomb.x, bomb.y, bomb)
        # Check what has been killed, stop if so
        ev = self.check_blast(bomb, bomb.x, bomb.y)
        if ev:
            return ev
        # Add explosions within range
        ev =      self.add_blast_dxdy(bomb, 1, 0)
        ev = ev + self.add_blast_dxdy(bomb,-1, 0)
        ev = ev + self.add_blast_dxdy(bomb, 0, 1)
        ev = ev + self.add_blast_dxdy(bomb, 0,-1)
        return ev

    def update_movable_entity(self, e):
        """Moves a movable entity in the world, return True if actually moved"""
        # Get the desired next position of the entity
        (nx, ny) = e.nextpos()
        # Make sure the position is within the bounds
        nx = max(0, min(self.width() - 1, nx))
        ny = max(0, min(self.height() - 1, ny))
        # Make sure we are actually moving
        if(((nx != e.x) or (ny != e.y)) and (not self.wall_at(nx, ny))):
            # Save new entity position
            e.x = nx
            e.y = ny
            return True
        return False

    def update_monster_move(self, monster, update_dict):
        # Save old index
        oi = self.index(monster.x, monster.y)
        # Try to move
        if self.update_movable_entity(monster):
            ev = []
            # Check for collision with explosion
            expl = self.explosion_at(monster.x, monster.y)
            if expl:
                ev.append(Event(Event.BOMB_HIT_MONSTER, expl.owner, monster))
                if update_dict:
                    # Remove monster
                    self.monsters[oi].remove(monster)
                return ev
            # Otherwise, the monster can walk safely
            if update_dict:
                # Remove monster from previous position
                self.monsters[oi].remove(monster)
                # Put monster in new position
                ni = self.index(monster.x, monster.y)
                np = self.monsters.get(ni, [])
                np.append(monster)
                self.monsters[ni] = np                
            # Check for collisions with characters
            characters = self.characters_at(monster.x, monster.y)
            if characters:
                for c in characters:
                    ev.append(Event(Event.CHARACTER_KILLED_BY_MONSTER, c, monster))
                return ev
        return []

    def update_character_move(self, character, update_dict):
        # Save old index
        oi = self.index(character.x, character.y)
        # Try to move
        if self.update_movable_entity(character):
            ev = []
            # Check for collision with explosion
            expl = self.explosion_at(character.x, character.y)
            if expl:
                ev.append(Event(Event.BOMB_HIT_CHARACTER, expl.owner, character))
                if update_dict:
                    # Remove character
                    self.characters[oi].remove(character)
                return ev
            # Otherwise, the character can walk
            if update_dict:
                # Remove character from previous position
                self.characters[oi].remove(character)
                # Put character in new position
                ni = self.index(character.x, character.y)
                np = self.characters.get(ni, [])
                np.append(character)
                self.characters[ni] = np
            # Check for collision with monster
            monsters = self.monsters_at(character.x, character.y)
            if monsters:
                return [Event(Event.CHARACTER_KILLED_BY_MONSTER,
                              character, monsters[0])]
            # Check for exit cell
            if self.exitcell == (character.x, character.y):
                return [Event(Event.CHARACTER_FOUND_EXIT, character)]
        return []

    def update_explosions(self):
        """Updates explosions"""
        todelete = []
        for i,e in self.explosions.items():
            e.tick()
            if e.expired():
                todelete.append(i)
                self.grid[e.x][e.y] = False
        for i in todelete:
            del self.explosions[i]

    def update_bombs(self):
        """Updates explosions"""
        todelete = []
        ev = []
        for i,b in self.bombs.items():
            b.tick()
            if b.expired():
                todelete.append(i)
                ev = ev + self.add_blast(b)
        for i in todelete:
            del self.bombs[i]
        return ev

    def manage_events_and_scores(self, events):
        for e in events:
            if e.tpe == Event.BOMB_HIT_WALL:
                self.scores[e.character.name] = self.scores[e.character.name] + 10
            elif e.tpe == Event.BOMB_HIT_MONSTER:
                self.scores[e.character.name] = self.scores[e.character.name] + 50
            elif e.tpe == Event.BOMB_HIT_CHARACTER:
                if e.character != e.other:
                    self.scores[e.character.name] = self.scores[e.character.name] + 100
            elif e.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                self.remove_character(e.character)
            elif e.tpe == Event.CHARACTER_FOUND_EXIT:
                self.scores[e.character.name] = self.scores[e.character.name] + 2 * self.time
        for k,clist in self.characters.items():
            for c in clist:
                self.scores[c.name] = self.scores[c.name] + 1
            
