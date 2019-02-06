from game import Game
from random_monster import RandomMonster
from character import Character

g = Game.fromfile('simple.txt')

# g.add_monster(monster.Monster(5,2))
g.world.add_monster(RandomMonster(4,1))


c = Character("me", 0, 0)
g.world.add_character(c)
g.world.add_bomb(1,0,c)

g.go()
