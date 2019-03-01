# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../group25')
from scenario1_AStarCharacterWithBomb import TestCharacter


# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character
#g.add_character(TestCharacter("me", # name
#                              "C",  # avatar
#                              0, 0  # position
#))
g.add_character(TestCharacter("me", # name
                              "C",  # avatar
                              0, 0,  # position
                              True,
                              5, 7))



# Run!
g.go()
