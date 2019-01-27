import game
import monster

g = game.Game(80, # width
              20, # height
              100, # max time
              2,  # bomb time
              3,  # expl_duration
              4)  # expl range

# Exit cell
g.add_exit(7,4)

# Top left fort
g.add_wall(0,5,1,0,10)
g.add_wall(9,0,0,1,5)
g.add_wall(10,0,0,1,5)
g.add_bomb(6,2)

g.add_monster(monster.Monster(5,2))
g.add_monster(monster.Monster(4,2))

g.go()
