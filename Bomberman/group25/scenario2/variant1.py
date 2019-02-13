# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../group25')
from testcharacter import TestCharacter
from scen2var1character import Scen2Var1Character


# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character
g.add_character(Scen2Var1Character("me", # name
                              "C",  # avatar
                              0, 0,  # position
                              1 #depth
))

# Run!
g.go()
