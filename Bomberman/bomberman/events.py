class Event:

    BOMB_HIT_WALL               = 0
    BOMB_HIT_MONSTER            = 1
    BOMB_HIT_CHARACTER          = 2
    CHARACTER_KILLED_BY_MONSTER = 3
    CHARACTER_FOUND_EXIT        = 4

    def __init__(self, tpe, character, other=None):
        self.tpe = tpe
        self.character = character
        self.other = other

    def __str__(self):
        if self.tpe == self.BOMB_HIT_WALL:
            return self.character.name + "'s bomb hit a wall"
        if self.tpe == self.BOMB_HIT_MONSTER:
            return self.character.name + "'s bomb hit a monster"
        if self.tpe == self.BOMB_HIT_CHARACTER:
            if self.character != self.other:
                return self.character.name + "'s bomb hit " + self.other.name
            else:
                return self.character.name + " killed itself"
        if self.tpe == self.CHARACTER_KILLED_BY_MONSTER:
            return self.character.name + " was killed by " + self.other.name
        if self.tpe == self.CHARACTER_FOUND_EXIT:
            return self.character.name + " found the exit"
