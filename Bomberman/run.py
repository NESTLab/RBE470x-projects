from game import Game
from entity import MonsterEntity
from selfpreserving_monster import SelfPreservingMonster
from testcharacter import TestCharacter

g = Game.fromfile('simple.txt')

# g.add_monster(MonsterEntity(0,0))
# g.add_monster(SelfPreservingMonster(4,1))

c = TestCharacter("me", 0, 0)
g.add_character(c)
# c = TestCharacter("you", 0, 1)
# g.add_character(c)
# g.world.add_bomb(8,0,c)

g.go()
