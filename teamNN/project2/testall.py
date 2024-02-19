# This is necessary to find the main code
import sys

import pygame

from monsters.selfpreserving_monster import SelfPreservingMonster
from teamNN.interactivecharacter import InteractiveCharacter

sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster

# TODO This is your code!
sys.path.insert(1, '../teamNN')
from testcharacter import TestCharacter

numberOfGames = 10  # Number of games to play for each variant
seedOffset = 10  # Offset for the random seed
waitTimeMS = 1000  # Wait time between frames in ms

pygame.display.set_caption('V1 G1 LastS: ' + str(0))
g = Game.fromfile('map.txt')
g.add_character(TestCharacter("me",  # name
                              "C",  # avatar
                              0, 0  # position
                              ))
g.go(waitTimeMS)
score = g.world.scores['me']
pygame.display.set_caption('V2 G1 S: ' + str(score))
scores2 = []
for i in range(numberOfGames):
    random.seed(seedOffset + i)
    g = Game.fromfile('map.txt')
    g.add_monster(StupidMonster("stupid",  # name
                                "S",  # avatar
                                3, 9  # position
                                ))
    g.add_character(TestCharacter("me",  # name
                                  "C",  # avatar
                                  0, 0  # position
                                  ))

    g.go(waitTimeMS)
    pygame.display.set_caption("V2 G%i S:%i" % (i + 2, g.world.scores['me']))
    scores2.append(g.world.scores['me'])

scores3 = []
pygame.display.set_caption('V3 G1 S: ' + str(scores2[numberOfGames - 1]))
for i in range(numberOfGames):
    random.seed(seedOffset + i)
    g = Game.fromfile('map.txt')
    g.add_monster(SelfPreservingMonster("selfpreserving",  # name
                                        "S",  # avatar
                                        3, 9,  # position
                                        1  # detection range
                                        ))

    g.add_character(TestCharacter("me",  # name
                                  "C",  # avatar
                                  0, 0  # position
                                  ))

    g.go(waitTimeMS)
    pygame.display.set_caption("V3 G%i S:%i" % (i + 2, g.world.scores['me']))
    scores3.append(g.world.scores['me'])

scores4 = []
pygame.display.set_caption('V4 G1 S: ' + str(scores3[numberOfGames - 1]))
for i in range(numberOfGames):
    random.seed(seedOffset + i)
    g = Game.fromfile('map.txt')
    g.add_monster(SelfPreservingMonster("aggressive",  # name
                                        "A",  # avatar
                                        3, 13,  # position
                                        2  # detection range
                                        ))

    g.add_character(TestCharacter("me",  # name
                                  "C",  # avatar
                                  0, 0  # position
                                  ))

    g.go(waitTimeMS)
    pygame.display.set_caption("V4 G%i S:%i" % (i + 2, g.world.scores['me']))
    scores4.append(g.world.scores['me'])

scores5 = []
pygame.display.set_caption('V5 G1 S: ' + str(scores4[numberOfGames - 1]))
for i in range(numberOfGames):
    random.seed(seedOffset + i)
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

    g.go(waitTimeMS)
    pygame.display.set_caption("V5 G%i S:%i" % (i + 2, g.world.scores['me']))
    scores5.append(g.world.scores['me'])

print("--- Variant 1 ---")
print("Score: ", score)
print()

average_score = sum(scores2) / len(scores2)
print("--- Variant 2 ---")
print("Played ", numberOfGames, " games with an average score of ", average_score, "Won ",
      len([score for score in scores2 if score > 0]), " games / ", numberOfGames)
print("Scores: ", scores2)
print()

print("--- Variant 3 ---")
average_score = sum(scores3) / len(scores3)
print("Played ", numberOfGames, " games with an average score of ", average_score, "Won ",
      len([score for score in scores3 if score > 0]), " games / ", numberOfGames)
print("Scores: ", scores3)
print()

print("--- Variant 4 ---")
average_score = sum(scores4) / len(scores4)
print("Played ", numberOfGames, " games with an average score of ", average_score, "Won ",
      len([score for score in scores4 if score > 0]), " games / ", numberOfGames)
print("Scores: ", scores4)
print()

print("--- Variant 5 ---")
average_score = sum(scores5) / len(scores5)
print("Played ", numberOfGames, " games with an average score of ", average_score, "Won ",
      len([score for score in scores5 if score > 0]), " games / ", numberOfGames)
print("Scores: ", scores5)
