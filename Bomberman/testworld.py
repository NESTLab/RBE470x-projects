import real_world
import entity
import random_monster as rm

w = real_world.RealWorld.from_params(20,10,10,1,1,1)
w.add_wall(0,0)
w.add_exit(1,0)
w.add_monster(rm.RandomMonster(2,0))
# w.add_character(0,1,None)
w.add_bomb(1,1,None)
w.add_explosion(2,1,entity.BombEntity(2,1,10,None))
w.printit()
