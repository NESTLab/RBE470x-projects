import game
import monster
import character

g = game.Game.fromfile('simple.txt')

# g.add_monster(monster.Monster(5,2))
# g.add_monster(monster.Monster(4,2))
g.add_character(character.Character("me", 0, 0))

g.go()
