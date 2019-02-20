from real_world import RealWorld
from events import Event
import colorama
import pygame
import math

class Game:
    """Game class"""

    def __init__(self, width, height, max_time, bomb_time, expl_duration, expl_range):
        self.world = RealWorld.from_params(width, height, max_time, bomb_time, expl_duration, expl_range)
        self.sprite_dir = "../../bomberman/sprites/"
        self.load_gui(width, height)

    @classmethod
    def fromfile(cls, fname):
        with open(fname, 'r') as fd:
            # First lines are parameters
            max_time = int(fd.readline().split()[1])
            bomb_time = int(fd.readline().split()[1])
            expl_duration = int(fd.readline().split()[1])
            expl_range = int(fd.readline().split()[1])
            # Next line is top border, use it for width
            width = len(fd.readline()) - 3
            # Count the rows
            startpos = fd.tell()
            height = 0
            row = fd.readline()
            while row and row[0] == '|':
                height = height + 1
                if len(row) != width + 3:
                    raise RuntimeError("Row", height, "is not", width, "characters long")
                row = fd.readline()
            # Create empty world
            gm = cls(width, height, max_time, bomb_time, expl_duration, expl_range)
            # Now parse the data in the world
            fd.seek(startpos)
            for y in range(0, height):
                ln = fd.readline()
                for x in range(0, width):
                    if ln[x+1] == 'E':
                        if not gm.world.exitcell:
                            gm.world.add_exit(x,y)
                        else:
                            raise RuntimeError("There can be only one exit cell, first one found at", x, y)
                    elif ln[x+1] == 'W':
                        gm.world.add_wall(x,y)
            # All done
            return gm

    def load_gui(self, board_width, board_height):
        pygame.init()
        self.height = 24 * board_height
        self.width = 24 * board_width
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.block_height = int(math.floor(self.height / board_height))
        self.block_width = int(math.floor(self.width / board_width))
        rect = (self.block_height, self.block_width)
        self.wall_sprite = pygame.image.load(self.sprite_dir + "wall.png")
        self.wall_sprite = pygame.transform.scale(self.wall_sprite, rect)
        self.bomberman_sprite = pygame.image.load(self.sprite_dir + "bomberman.png")
        self.bomberman_sprite = pygame.transform.scale(self.bomberman_sprite, rect)
        self.monster_sprite = pygame.image.load(self.sprite_dir + "monster.png")
        self.monster_sprite = pygame.transform.scale(self.monster_sprite, rect)
        self.portal_sprite = pygame.image.load(self.sprite_dir + "portal.png")
        self.portal_sprite = pygame.transform.scale(self.portal_sprite, rect)
        self.bomb_sprite = pygame.image.load(self.sprite_dir + "bomb.png")
        self.bomb_sprite = pygame.transform.scale(self.bomb_sprite, rect)
        self.explosion_sprite = pygame.image.load(self.sprite_dir + "explosion.png")
        self.explosion_sprite = pygame.transform.scale(self.explosion_sprite, rect)

    def display_gui(self):
        pygame.event.clear()
        for x in range(self.world.width()):
            for y in range(self.world.height()):
                top = self.block_height * y
                left = self.block_width * x
                pygame.draw.rect(self.screen, (65, 132, 15), [left, top, self.block_width, self.block_height])
                rect = (left, top, self.block_width, self.block_height)
                if self.world.wall_at(x, y): # Walls
                    self.screen.blit(self.wall_sprite, rect)
                if self.world.explosion_at(x, y): # Explosion
                    self.screen.blit(self.explosion_sprite, rect)
                if self.world.characters_at(x, y): # Player
                    self.screen.blit(self.bomberman_sprite, rect)
                if self.world.monsters_at(x, y): # Monster
                    self.screen.blit(self.monster_sprite, rect)
                if self.world.exit_at(x, y): # Portal
                    self.screen.blit(self.portal_sprite, rect)
                if self.world.bomb_at(x, y): # Bomb
                    self.screen.blit(self.bomb_sprite, rect)
        pygame.display.flip()

    def go(self):
        colorama.init(autoreset=True)
        self.display_gui()
        self.draw()
        while not self.done():
            self.display_gui()
            self.step()
            self.display_gui()
            self.draw()
        colorama.deinit()

    def step(self):
        (self.world, self.events) = self.world.next()
        input("Press Enter to continue...")

    ###################
    # Private methods #
    ###################

    def draw(self):
        self.world.printit()

    def done(self):
        # Time's up
        if self.world.time <= 0:
            return True
        # No more characters left
        if not self.world.characters:
            return True
        # Last man standing
        if not self.world.exitcell:
            count = 0
            for k,clist in self.world.characters.items():
                count = count + len(clist)
            if count == 0:
                return True
        return False

    def add_monster(self, m):
        self.world.add_monster(m)

    def add_character(self, c):
        self.world.add_character(c)
