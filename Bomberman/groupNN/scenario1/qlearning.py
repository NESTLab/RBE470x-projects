# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../groupNN')
from qlearning_character import QCharacter

qtable = {"q" : 1}

for i in range(0, 2):
    # Create the game
    g = Game.fromfile('map.txt')
    # TODO Add your character
    g.add_character(QCharacter("Q", # name
                                    "Q",  # avatar
                                    0, 0,  # position
                                    qtable  # starting Q table
                                    ))
    # Run!
    g.go()


print(qtable)