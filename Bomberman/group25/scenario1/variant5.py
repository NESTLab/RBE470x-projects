# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
import tournament
from game import Game
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../group25')
from aStarCharacterWithHeuristic import TestCharacter

random.seed(6543252) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
# g = tournament.Tournament.fromfile('map.txt')

g.add_monster(StupidMonster("monster",  # name
                            "S",  # avatar
                            3, 5,  # position
                            ))
g.add_monster(SelfPreservingMonster("monster",  # name
                                    "A",  # avatar
                                    3, 13,  # position
                                    2  # detection range
                                    ))

# TODO Add your character
g.add_character(TestCharacter("me",  # name
                              "C",  # avatar
                              0, 0  # position
                              ))

# Run!
g.go()

# g.runTournament()
