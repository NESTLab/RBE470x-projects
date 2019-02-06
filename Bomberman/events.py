class Event:

    BOMB_HIT_WALL               = 0
    BOMB_HIT_MONSTER            = 1
    BOMB_HIT_CHARACTER          = 2
    CHARACTER_KILLED_BY_MONSTER = 3
    CHARACTER_FOUND_EXIT        = 4

    def __init__(self, tpe, character, other):
        self.tpe = tpe
        self.character = character
        self.other = other
