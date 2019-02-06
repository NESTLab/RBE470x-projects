from copy import deepcopy
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
            nmonsters = []
            for m in omonsters:
                nmonsters.append(deepcopy(m))
            new.monsters[k] = nmonsters
        # Copy characters and build a mapping between old and new
        mapping = {}
        for k, ocharacters in wrld.characters.items():
            ncharacters = []
            for oc in ocharacters:
                nc = deepcopy(oc)
                ncharacters.append(nc)
                mapping[oc] = nc
            new.characters[k] = ncharacters
        # Copy bombs
        for k, ob in wrld.bombs.items():
            c = mapping.get(ob.owner)
            if c:
                new.bombs[k] = BombEntity(ob.x, ob.y, ob.timer, c)
        # Copy explosions
        for k, oe in wrld.explosions.items():
            c = mapping.get(oe.owner)
            if c:
                new.explosions[k] = ExplosionEntity(oe.x, oe.y, oe.timer, c)
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

    def move_monster(self, monster, dx, dy):
        """Moves a monster by (dx, dy), returns event"""
        # Set desired move
        monster.move(dx, dy)
        # Perform move
        return self.update_monster_move(monster, True)

    def move_character(self, character, dx, dy):
        """Moves a character by (dx, dy), returns event"""
        # Set desired move
        character.move(dx, dy)
        # Perform move
        return self.update_character_move(character, True)

    def printit(self):
        """Prints the current state of the world"""
        border = "+" + "-" * self.width() + "+\n"
        print("\nTIME LEFT: ", self.time)
        sys.stdout.write(border)
        for y in range(self.height()):
            sys.stdout.write("|")
            for x in range(self.width()):
                if self.characters_at(x,y):
                    sys.stdout.write(Back.GREEN + "C")
                elif self.monsters_at(x,y):
                    sys.stdout.write(Back.BLUE + "M")
                elif self.exit_at(x,y):
                    sys.stdout.write(Back.YELLOW + "E")
                elif self.bomb_at(x,y):
                    sys.stdout.write(Back.MAGENTA + "B")
                elif self.explosion_at(x,y):
                    sys.stdout.write(Fore.RED + "*")
                elif self.wall_at(x,y):
                    sys.stdout.write(Back.WHITE + " ")
                else:
                    sys.stdout.write(" ")
                sys.stdout.write(Style.RESET_ALL)
            sys.stdout.write("|\n")
        sys.stdout.write(border)
        sys.stdout.flush()
        print("CHARACTERS")
        for k,clist in self.characters.items():
            for c in clist:
                print(k, c)
        print("BOMBS")
        for k,b in self.bombs.items():
            print(k, b, b.owner)

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
        # Remove bombs left by character
        bfound = None
        for i, b in self.bombs.items():
            if b.owner == character:
                bfound = i
                break
        if bfound:
            del self.bombs[bfound]
        # Remove character
        self.characters[self.index(character.x, character.y)].remove(character)

    def add_blast_dxdy(self, bomb, dx, dy):
        # Current position
        xx = bomb.x + dx
        yy = bomb.y + dy
        # Range
        rnge = 0
        while ((rnge < self.expl_range) and
               (xx >= 0) and (xx < self.width()) and
               (yy >= 0) and (yy < self.height())):
            # Cannot destroy exit
            if self.exitcell == (xx,yy):
                return []
            # Place explosion
            self.add_explosion(xx, yy, bomb)
            # Check if a bomb has been hit
            if self.bomb_at(xx, yy):
                del self.bombs[self.index(x,y)]
                return []
            # Check if a wall has been hit
            if self.wall_at(xx, yy):
                return [Event(Event.BOMB_HIT_WALL, bomb.owner, None)]
            # Check if a monster has been hit
            m = self.monsters_at(xx,yy)
            if m:
                self.monsters[self.index(xx,yy)].remove(m)
                return [Event(Event.BOMB_HIT_MONSTER, bomb.owner, m)]
            # Check if a character has been hit
            c = self.characters_at(xx,yy)
            if c:
                self.remove_character(c)
                return [Event(Event.BOMB_HIT_CHARACTER, bomb.owner, c)]
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
        if((nx != e.x) or (ny != e.y) and (not self.wall_at(nx, ny))):
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
                ev = []
                for c in characters:
                    ev.append(Event(Event.CHARACTER_KILLED_BY_MONSTER, c, monster))
                return ev
        return []

    def update_character_move(self, character, update_dict):
        # Save old index
        oi = self.index(character.x, character.y)
        # Try to move
        if self.update_movable_entity(character):
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
