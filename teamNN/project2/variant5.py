# This is necessary to find the main code
import sys

sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../teamNN')
from testcharacter import TestCharacter

# Create the game
numberOfGames = 1
scores = []
for i in range(numberOfGames):
    random.seed(14)
    g = Game.fromfile('map.txt')
    g.add_monster(StupidMonster("stupid",  # name
                                "S",  # avatar
                                3, 5,  # position
                                ))
    g.add_monster(SelfPreservingMonster("aggressive",  # name
                                        "A",  # avatar
                                        3, 13,  # position
                                        1  # detection range
                                        ))

    g.add_character(TestCharacter("me",  # name
                                  "C",  # avatar
                                  0, 0  # position
                                  ))

    g.go(10)
    scores.append(g.world.scores['me'])

average_score = sum(scores) / len(scores)
print("Played ", numberOfGames, " games with an average score of ", average_score)
# Print the number of score where the score is over 0
print("Number of games won: ", len([score for score in scores if score > 0]))
print("Scores: ", scores)
