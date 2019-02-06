import cell
import entity

class Character(entity.AIEntity, entity.MovableEntity):
    """Basic definitions for a custom-made character"""

    def __init__(self, name, x, y):
        entity.AIEntity.__init__(self)
        entity.MovableEntity.__init__(self, x, y)
        # Character name
        self.name = name
        # Whether this character wants to place a bomb
        self.place_bomb = False
        # Debugging elements
        self.tiles      = set()
        self.rays       = []

    def __hash__(self):
        return hash((self.name, self.x, self.y))

    def __eq__(self, other):
        return (self.name, self.x, self.y) == (other.name, other.x, other.y)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

    def do(self, wrld):
        pass

    def place_bomb(self):
        """Attempts to place a bomb"""
        self.place_bomb = True

    def set_tile_color(self, x, y, r, g, b):
        """Sets the tile color at (x,y)"""
        self.tiles[(x,y)] = (r,g,b)

    def draw_ray(self, sx, sy, ex, ey, r, g, b):
        """Draws a ray from (sx,sy) to (ex,ey)"""
        self.rays.append((sx, sy, ex, ey, r, g, b))
