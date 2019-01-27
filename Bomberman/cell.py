import sys
from colorama import Fore, Back

#########
# Cells #
#########

class Cell(object):
    """Abstract cell"""
    EMPTY     = 0
    EXIT      = 1
    WALL      = 2
    BOMB      = 3
    EXPLOSION = 4
    MONSTER   = 5
    CHARACTER = 6

    def __init__(self, tpe, data):
        """Class constructor"""
        self.tpe = tpe
        self.data = data

    def draw(self):
        """Draws the cell"""
        pass

##############
# Empty cell #
##############

class EmptyCell(Cell):
    """Empty cell"""
    
    def __init__(self):
        super().__init__(self.EMPTY, None)

    def draw(self):
        """Draws the cell"""
        sys.stdout.write(" ")

#############
# Exit cell #
#############

class ExitCell(Cell):
    """Exit cell"""
    
    def __init__(self):
        super().__init__(self.EXIT, None)

    def draw(self):
        """Draws the cell"""
        sys.stdout.write(Back.YELLOW + "E")

#############
# Wall cell #
#############

class WallCell(Cell):
    """Wall cell"""
    def __init__(self):
        super().__init__(self.WALL, None)

    def draw(self):
        """Draws the cell"""
        sys.stdout.write(Back.WHITE + " ")

#############
# Bomb cell #
#############

class BombCell(Cell):
    """Bomb cell"""
    def __init__(self, bomb):
        super().__init__(self.BOMB, bomb)

    def draw(self):
        """Draws the cell"""
        sys.stdout.write(Back.MAGENTA + "B")

##################
# Explosion cell #
##################

class ExplosionCell(Cell):
    """Explosion cell"""
    def __init__(self, explosion):
        super().__init__(self.EXPLOSION, explosion)

    def draw(self):
        """Draws the cell"""
        sys.stdout.write(Fore.RED + "*")

################
# Monster cell #
################

class MonsterCell(Cell):
    """Monster cell"""
    def __init__(self, monster):
        super().__init__(self.MONSTER, monster)

    def draw(self):
        """Draws the cell"""
        sys.stdout.write(Back.BLUE + "M")

##################
# Character cell #
##################

class CharacterCell(Cell):
    """Character cell"""
    def __init__(self, character):
        super().__init__(self.CHARACTER, character)

    def draw(self):
        """Draws the cell"""
        sys.stdout.write(Fore.GREEN + "C")
