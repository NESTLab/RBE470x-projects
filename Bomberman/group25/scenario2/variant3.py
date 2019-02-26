# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../group25')
from testcharacter import TestCharacter
from scen2var3character import Scen2Var3Character

# Create the game
random.seed(123) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(SelfPreservingMonster("monster", # name
                                    "M",       # avatar
                                    3, 9,      # position
                                    1          # detection range
))

# TODO Add your character
g.add_character(Scen2Var3Character("me", # name
                              "C",  # avatar
                              0, 0,  # position
                              3 # depth
))

# Run!
g.go()