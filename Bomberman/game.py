import real_world
import entity
import cell
import colorama

class Game:
    """Game class"""

    def __init__(self, width, height, max_time, bomb_time, expl_duration, expl_range):
        self.world = real_world.RealWorld.from_params(width, height, max_time, bomb_time, expl_duration, expl_range)

    @classmethod
    def fromfile(cls, fname):
        with open(fname, 'r') as fd:
            # First lines are parameters
            max_time = int(fd.readline().split()[1])
            bomb_time = int(fd.readline().split()[1])
            expl_duration = int(fd.readline().split()[1])
            expl_range = int(fd.readline().split()[1])
            # Next line is top border, use it for width
            width = len(fd.readline()) - 2
            # Count the rows
            startpos = fd.tell()
            height = 0
            row = fd.readline()
            while row and row[0] == '|':
                height = height + 1
                if len(row) != width + 2:
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
                        gm.world.add_exit(x,y)
                    elif ln[x+1] == 'W':
                        gm.world.add_wall(x,y)
            # All done
            return gm

    def go(self):
        colorama.init(autoreset=True)
        self.draw()
        while not self.done():
            self.step()
            self.draw()
        colorama.deinit()

    def step(self):
        (self.world, ev) = self.world.next()
        input("Press Enter to continue...")

    def draw(self):
        self.world.printit()

    def done(self):
        return self.world.time <= 0

    # def step_monsters(self, wrld):
    #     for m in self.monsters:
    #         m.do(wrld)
    #         self.world.move_entity(m)

    # def step_characters(self, wrld):
    #     for c in self.characters:
    #         c.do(wrld)
    #         if c.place_bomb:
    #             self.add_bomb(c.x, c.y)
    #             c.place_bomb = False
    #         self.world.move_entity(c)
