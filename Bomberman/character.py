from entity import AIEntity, MovableEntity

class Character(AIEntity, MovableEntity):
    """Basic definitions for a custom-made character"""

    def __init__(self, name, x, y):
        AIEntity.__init__(self)
        MovableEntity.__init__(self, x, y)
        # Character name
        self.name = name
        # Whether this character wants to place a bomb
        self.maybe_place_bomb = False
        # Debugging elements
        self.tiles = {}

    def place_bomb(self):
        """Attempts to place a bomb"""
        self.maybe_place_bomb = True

    def set_tile_color(self, x, y, color):
        """Sets the tile color at (x,y)"""
        self.tiles[(x,y)] = color

    ###################
    # Private methods #
    ###################
        
    def __hash__(self):
        return hash((self.name, self.x, self.y))

    def __eq__(self, other):
        return (self.name, self.x, self.y) == (other.name, other.x, other.y)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

