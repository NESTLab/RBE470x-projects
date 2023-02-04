# This is necessary to find the main code
import sys

from teamNN.interactivecharacter import InteractiveCharacter

sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../teamNN')
from testcharacter import TestCharacter

# Create the game
random.seed(3)  # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(SelfPreservingMonster("aggressive",  # name
                                    "A",  # avatar
                                    3, 13,  # position
                                    2  # detection range
                                    ))

# TODO Add your character
# g.add_character(InteractiveCharacter("me",  # name
#                                      "C",  # avatar
#                                      0, 0  # position
#                                      ))

# Uncomment this if you want the test character
g.add_character(TestCharacter("me",  # name
                              "C",  # avatar
                              0, 0  # position
                              ))
# Run!
g.go(200)
