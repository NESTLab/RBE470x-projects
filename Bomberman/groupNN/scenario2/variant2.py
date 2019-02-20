# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster

# TODO This is your code!
sys.path.insert(1, '../groupNN')
from greedycharacterS2 import GreedyCharacter

# Create the game
random.seed(1) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(StupidMonster("monster", # name
                            "M",       # avatar
                            3, 9       # position
))

# TODO Add your character
g.add_character(GreedyCharacter("me", # name
                              "C",  # avatar
                              0, 0  # position
))

# Run!
g.go()
