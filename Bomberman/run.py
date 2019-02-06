from game import Game
from selfpreserving_monster import SelfPreservingMonster
from character import Character

g = Game.fromfile('simple.txt')

# g.add_monster(monster.Monster(5,2))
g.add_monster(SelfPreservingMonster(4,1))

c = Character("me", 0, 0)
g.add_character(c)
# g.world.add_bomb(1,0,c)

g.go()
