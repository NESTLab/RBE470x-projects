import world
import entity
import cell
import colorama

class Game:
    """Game class"""

    def __init__(self, width, height, max_time, bomb_time, expl_duration, expl_range):
        self.bomb_time = bomb_time
        self.expl_duration = expl_duration
        self.expl_range = expl_range
        self.world = world.World(width, height, max_time)
        self.monsters = set()
        self.characters = set()
        self.bombs = set()
        self.explosions = set()

    def go(self):
        colorama.init(autoreset=True)
        self.draw()
        while not self.done():
            self.step()
            self.draw()
        colorama.deinit()

    def step(self):
        # Update time
        self.world.time = self.world.time - 1
        # Take care of bombs and explosions
        self.step_bombs()
        self.step_explosions()
        # Make sure the game hasn't ended
        if not self.done():
            # Update monsters
            self.step_monsters()
            # Update characters
            pass
        input("Press Enter to continue...")

    def draw(self):
        self.world.draw()

    def done(self):
        return self.world.time <= 0

    def add_exit(self, x, y):
        self.world.place_exit(x, y)

    def add_wall(self, sx, sy, dx, dy, length):
        for x in range(sx, min(sx + dx*length + 1, self.world.width)):
            for y in range(sy, min(sy + dy*length + 1, self.world.height)):
                self.world.place_wall(x, y)

    def add_monster(self, monster):
        """Add monster to world"""
        self.monsters.add(monster)
        self.world.place_monster(monster)

    def add_character(self, character):
        """Add character to world"""
        self.characters.add(character)
        self.world.place_character(character)

    def add_bomb(self, x, y):
        """Add a bomb in the grid"""
        bomb = entity.BombEntity(x, y, self.bomb_time)
        self.bombs.add(bomb)
        self.world.place_bomb(bomb)

    def add_explosion_dxdy(self, explosion, x, y, dx, dy):
        xx = x + dx
        yy = y + dy
        rng = 0
        while ((rng < self.expl_range) and
               (xx >= 0) and (xx < self.world.width) and
               (yy >= 0) and (yy < self.world.height)):
            # Get entity at current position
            e = self.world.at(xx, yy)
            # Cannot destroy exit
            if e.tpe == cell.Cell.EXIT:
                return
            # Place explosion cell
            self.world.place_explosion(explosion, xx, yy)
            # Check if a monster has been hit
            if e.tpe == cell.Cell.MONSTER:
                self.monsters.remove(e.data)
            # Check if a character has been hit
            elif e.tpe == cell.Cell.CHARACTER:
                self.characters.remove(e.data)
            # Check if a bomb has been hit
            elif e.tpe == cell.Cell.BOMB:
                self.bombs.remove(e.data)
            # Continue only if an empty or explosion cell was traversed
            if ((e.tpe != cell.Cell.EMPTY) and
                (e.tpe != cell.Cell.EXPLOSION)):
                return
            # Next cell
            xx = xx + dx
            yy = yy + dy
            rng = rng + 1

    def add_explosion(self, x, y):
        """Add an explosion in the grid"""
        explosion = entity.ExplosionEntity(x, y, self.expl_duration)
        self.explosions.add(explosion)
        self.world.place_explosion(explosion, x, y)
        self.add_explosion_dxdy(explosion, x, y,  1,  0)
        self.add_explosion_dxdy(explosion, x, y, -1,  0)
        self.add_explosion_dxdy(explosion, x, y,  0,  1)
        self.add_explosion_dxdy(explosion, x, y,  0, -1)
        self.add_explosion_dxdy(explosion, x, y,  1,  1)
        self.add_explosion_dxdy(explosion, x, y,  1, -1)
        self.add_explosion_dxdy(explosion, x, y, -1,  1)
        self.add_explosion_dxdy(explosion, x, y, -1, -1)

    def clear_explosion_dxdy(self, explosion, dx, dy):
        """Clear an explosion from the grid"""
        xx = explosion.x + dx
        yy = explosion.y + dy
        rng = 0
        while ((rng < self.expl_range) and
               (xx >= 0) and (xx < self.world.width) and
               (yy >= 0) and (yy < self.world.height)):
            # Get entity at current position
            e = self.world.at(xx, yy)
            # Make sure it's the explosion we want to delete
            if ((e.tpe != cell.Cell.EXPLOSION) or
                (e.data != explosion)):
                # It's not, we're done
                return
            # Put an empty spot
            self.world.place_empty(xx, yy)
            # Next cell
            xx = xx + dx
            yy = yy + dy
            rng = rng + 1

    def clear_explosion(self, explosion):
        """Clear an explosion from the grid"""
        # Get entity at current position
        e = self.world.at(explosion.x, explosion.y)
        # Make sure it's the explosion we want to delete
        if ((e.tpe == cell.Cell.EXPLOSION) and
            (e.data == explosion)):
            self.world.place_empty(explosion.x, explosion.y)
        self.clear_explosion_dxdy(explosion,  1,  0)
        self.clear_explosion_dxdy(explosion, -1,  0)
        self.clear_explosion_dxdy(explosion,  0,  1)
        self.clear_explosion_dxdy(explosion,  0, -1)
        self.clear_explosion_dxdy(explosion,  1,  1)
        self.clear_explosion_dxdy(explosion,  1, -1)
        self.clear_explosion_dxdy(explosion, -1,  1)
        self.clear_explosion_dxdy(explosion, -1, -1)

    def step_bombs(self):
        to_delete = set()
        for b in self.bombs:
            b.tick()
            if b.expired():
                to_delete.add(b)
                self.add_explosion(b.x, b.y)
        for b in to_delete:
            self.bombs.remove(b)

    def step_explosions(self):
        to_delete = set()
        for e in self.explosions:
            e.tick()
            if e.expired():
                to_delete.add(e)
                self.clear_explosion(e)
        for e in to_delete:
            self.explosions.remove(e)

    def step_monsters(self):
        for m in self.monsters:
            m.do(self.world)
            self.world.move_entity(m)

    def step_characters(self):
        for c in self.characters:
            c.do(self.world)
            # # If motion
            # self.world.move_entity(c)
            # # If place bomb
            # self.add_bomb(c.x, c.y)
