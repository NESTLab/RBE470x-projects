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

class MovableEntity(PositionalEntity):
    """Positional entity that can move"""

    def __init__(self, x, y):
        """Class constructor"""
        super().__init__(x, y)
        self.dx = 0
        self.dy = 0

    def move(self, dx, dy):
        """Move character"""
        self.dx = dx
        self.dy = dy

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

###############
# Bomb entity #
###############

class BombEntity(PositionalEntity, TimedEntity):
    """Bomb entity"""

    def __init__(self, x, y, timer):
        PositionalEntity.__init__(self, x, y)
        TimedEntity.__init__(self, timer)

####################
# Explosion entity #
####################

class ExplosionEntity(PositionalEntity, TimedEntity):
    """Explosion entity"""

    def __init__(self, x, y, timer):
        PositionalEntity.__init__(self, x, y)
        TimedEntity.__init__(self, timer)
