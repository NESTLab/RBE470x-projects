import cell
import entity

class Character(entity.AIEntity, entity.MovableEntity):
    """Basic definitions for a custom-made character"""

    def __init__(self, name, x, y):
        entity.MovableEntity.__init__(self, x, y)
        self.name = name
        self.place_bomb = False

    def do(self, wrld):
        pass

    def place_bomb(self):
        self.place_bomb = True
