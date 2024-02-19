# This is necessary to find the main code
import sys


sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster

# TODO This is your code!
sys.path.insert(1, '../teamNN')
from testcharacter import TestCharacter
from interactivecharacter import InteractiveCharacter


# Create the game
# random.seed(123)  # TODO Change this if you want different random choices
# g = Game.fromfile('map.txt')
# g.add_monster(StupidMonster("stupid",  # name
#                             "S",  # avatar
#                             3, 9  # position
#                             ))
#
# # TODO Add your character
# # g.add_character(InteractiveCharacter("me",  # name
# #                                      "C",  # avatar
# #                                      0, 0  # position
# #                                      ))
#
# # Uncomment this if you want the test character
# g.add_character(TestCharacter("me",  # name
#                               "C",  # avatar
#                               0, 0  # position
#                               ))
#
# # Run!
# g.go(200)


numberOfGames = 10
scores = []
for i in range(numberOfGames):
    random.seed(i)
    g = Game.fromfile('map.txt')
    g.add_monster(StupidMonster("stupid",  # name
                                "S",  # avatar
                                3, 9  # position
                                ))
    g.add_character(TestCharacter("me",  # name
                                  "C",  # avatar
                                  0, 0  # position
                                  ))

    g.go(100)
    scores.append(g.world.scores['me'])

average_score = sum(scores) / len(scores)
print("Played ", numberOfGames, " games with an average score of ", average_score)
# Print the number of score where the score is over 0
print("Number of games won: ", len([score for score in scores if score > 0]))
print("Scores: ", scores)
