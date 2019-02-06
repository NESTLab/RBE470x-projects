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

    def __init__(self, x, y):
        """Class constructor"""
        self.x = x
        self.y = y

##################
# Movable entity #
##################

def __sign__(x):
    if x == 0.0:
        return 0
    return int(copysign(1, x))

class MovableEntity(PositionalEntity):
    """Positional entity that can move"""

    def __init__(self, x, y):
        """Class constructor"""
        super().__init__(x, y)
        self.dx = 0
        self.dy = 0

    def move(self, dx, dy):
        """Move character"""
        # Make sure dx is in [-1,1]
        self.dx = __sign__(dx)
        # Make sure dy is in [-1,1]
        self.dy = __sign__(dy)

    def nextpos(self):
        """Returns the next position of this entity"""
        return (self.x + self.dx, self.y + self.dy)

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

#############
# AI entity #
#############

class AIEntity(Entity):
    """Entity with an AI"""

    def do(self, wrld):
        """Pick an action for the entity given the world state"""
        raise NotImplementedError("Please implement this method")

################
# Owned entity #
################

class OwnedEntity(Entity):
    """Entity with an owner"""

    def __init__(self, owner):
        self.owner = owner

###############
# Bomb entity #
###############

class BombEntity(PositionalEntity, TimedEntity, OwnedEntity):
    """Bomb entity"""

    def __init__(self, x, y, timer, character):
        PositionalEntity.__init__(self, x, y)
        TimedEntity.__init__(self, timer)
        OwnedEntity.__init__(self, character)

####################
# Explosion entity #
####################

class ExplosionEntity(PositionalEntity, TimedEntity, OwnedEntity):
    """Explosion entity"""

    def __init__(self, x, y, timer, character):
        PositionalEntity.__init__(self, x, y)
        TimedEntity.__init__(self, 1)
        OwnedEntity.__init__(self, character)

##################
# Monster entity #
##################

class MonsterEntity(AIEntity, MovableEntity):
    """Monster Entity"""

    def __init__(self, x, y):
        AIEntity.__init__(self)
        MovableEntity.__init__(self, x, y)
