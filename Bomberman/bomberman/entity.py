from math import copysign

############
# Entities #
############

class Entity(object):
    """Abstract entity class"""
    pass

#####################
# Positional entity #
#####################

class PositionalEntity(Entity):
    """Entity with a position"""

    # PARAM x [int]: x coordinate in the grid
    # PARAM y [int]: y coordinate in the grid
    def __init__(self, x, y):
        """Class constructor"""
        self.x = x
        self.y = y

    ###################
    # Private methods #
    ###################

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        return not(self == other)

##################
# Movable entity #
##################

def __sign__(x):
    if x == 0.0:
        return 0
    return int(copysign(1, x))

class MovableEntity(PositionalEntity):
    """Positional entity that can move"""

    # PARAM x [int]: x coordinate in the grid
    # PARAM y [int]: y coordinate in the grid
    def __init__(self, x, y):
        """Class constructor"""
        super().__init__(x, y)
        self.dx = 0
        self.dy = 0

    # Sets the desired direction of the entity
    # PARAM dx [int]: delta x
    # PARAM dy [int]: delta y
    # The passed values are clamped in [-1,1]
    def move(self, dx, dy):
        """Move entity"""
        # Make sure dx is in [-1,1]
        self.dx = __sign__(dx)
        # Make sure dy is in [-1,1]
        self.dy = __sign__(dy)

    # Returns the next position of this entity as a tuple (x,y)
    def nextpos(self):
        """Returns the next position of this entity"""
        return (self.x + self.dx, self.y + self.dy)

    ###################
    # Private methods #
    ###################

    def __eq__(self, other):
        return (super().__eq__(other) and
                (self.dx, self.dy) == (other.dx, other.dy))

    def __ne__(self, other):
        return not(self == other)

################
# Timed entity #
################

class TimedEntity(Entity):
    """Entity with a time limit"""

    def __init__(self, timer):
        """Class constructor"""
        self.timer = timer

    def tick(self):
        """Performs a clock tick"""
        self.timer = self.timer - 1

    def expired(self):
        return self.timer < 0

    ###################
    # Private methods #
    ###################

    def __eq__(self, other):
        return self.timer == other.timer

    def __ne__(self, other):
        return not(self == other)

#############
# AI entity #
#############

class AIEntity(Entity):
    """Entity with an AI"""

    # PARAM name [string]: A unique name for this entity
    # PARAM rep [character]: A single character used to draw the entity
    def __init__(self, name, avatar):
        self.name = name
        self.avatar = avatar[0]

    def do(self, wrld):
        """Pick an action for the entity given the world state"""
        pass

    ###################
    # Private methods #
    ###################

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not(self == other)

################
# Owned entity #
################

class OwnedEntity(Entity):
    """Entity with an owner"""

    def __init__(self, owner):
        self.owner = owner

    ###################
    # Private methods #
    ###################

    def __eq__(self, other):
        return self.owner == other.owner

    def __ne__(self, other):
        return not(self == other)

###############
# Bomb entity #
###############

class BombEntity(PositionalEntity, TimedEntity, OwnedEntity):
    """Bomb entity"""

    def __init__(self, x, y, timer, character):
        PositionalEntity.__init__(self, x, y)
        TimedEntity.__init__(self, timer)
        OwnedEntity.__init__(self, character)

    ###################
    # Private methods #
    ###################

    def __eq__(self, other):
        return (super(PositionalEntity, self).__eq__(other) and
                super(TimedEntity, self).__eq__(other) and
                super(OwnedEntity, self).__eq__(other))

    def __ne__(self, other):
        return not(self == other)

####################
# Explosion entity #
####################

class ExplosionEntity(PositionalEntity, TimedEntity, OwnedEntity):
    """Explosion entity"""

    def __init__(self, x, y, timer, character):
        PositionalEntity.__init__(self, x, y)
        TimedEntity.__init__(self, timer)
        OwnedEntity.__init__(self, character)

    ###################
    # Private methods #
    ###################

    def __eq__(self, other):
        return (super(PositionalEntity, self).__eq__(other) and
                super(TimedEntity, self).__eq__(other) and
                super(OwnedEntity, self).__eq__(other))

    def __ne__(self, other):
        return not(self == other)

##################
# Monster entity #
##################

class MonsterEntity(AIEntity, MovableEntity):
    """Monster Entity"""

    def __init__(self, name, avatar, x, y):
        AIEntity.__init__(self, name, avatar)
        MovableEntity.__init__(self, x, y)

    ###################
    # Private methods #
    ###################
        
    @classmethod
    def from_monster(cls, monster):
        """Clone this monster"""
        return MonsterEntity(monster.name, monster.avatar, monster.x, monster.y)

    ###################
    # Private methods #
    ###################

    def __eq__(self, other):
        return (super(MovableEntity, self).__eq__(other) and
                super(AIEntity, self).__eq__(other))

    def __ne__(self, other):
        return not(self == other)

####################
# Character entity #
####################

class CharacterEntity(AIEntity, MovableEntity):
    """Basic definitions for a custom-made character"""

    def __init__(self, name, avatar, x, y):
        AIEntity.__init__(self, name, avatar)
        MovableEntity.__init__(self, x, y)
        # Whether this character wants to place a bomb
        self.maybe_place_bomb = False
        # Debugging elements
        self.tiles = {}

    def place_bomb(self):
        """Attempts to place a bomb"""
        self.maybe_place_bomb = True

    def set_cell_color(self, x, y, color):
        """Sets the cell color at (x,y)"""
        self.tiles[(x,y)] = color

    ###################
    # Private methods #
    ###################
        
    @classmethod
    def from_character(cls, character):
        """Clone this character"""
        new = CharacterEntity(character.name, character.avatar, character.x, character.y)
        new.dx = character.dx
        new.dy = character.dy
        new.maybe_place_bomb = character.maybe_place_bomb
        return new

    def __hash__(self):
        return hash((self.name, self.x, self.y))

    def __eq__(self, other):
        return (self.maybe_place_bomb == other.maybe_place_bomb and
                super(MovableEntity, self).__eq__(other) and
                super(AIEntity, self).__eq__(other))

    def __ne__(self, other):
        return not(self == other)

