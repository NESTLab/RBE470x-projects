from real_world import RealWorld
from events import Event
import colorama

class Game:
    """Game class"""

    def __init__(self, width, height, max_time, bomb_time, expl_duration, expl_range):
        self.world = RealWorld.from_params(width, height, max_time, bomb_time, expl_duration, expl_range)
        self.events = []
        self.scores = {}

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
                        if not gm.world.exitcell:
                            gm.world.add_exit(x,y)
                        else:
                            raise RuntimeError("There can be only one exit cell, first one found at", x, y)
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
        (self.world, self.events) = self.world.next()
        self.manage_events_and_scores()
        input("Press Enter to continue...")

    ###################
    # Private methods #
    ###################

    def manage_events_and_scores(self):
        for e in self.events:
            if e.tpe == Event.BOMB_HIT_WALL:
                self.scores[e.character.name] = self.scores[e.character.name] + 10
            elif e.tpe == Event.BOMB_HIT_MONSTER:
                self.scores[e.character.name] = self.scores[e.character.name] + 50
            elif e.tpe == Event.BOMB_HIT_CHARACTER:
                if e.character != e.other:
                    self.scores[e.character.name] = self.scores[e.character.name] + 100
            elif e.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                self.world.remove_character(e.character)
            elif e.tpe == Event.CHARACTER_FOUND_EXIT:
                self.scores[e.character.name] = self.scores[e.character.name] + 2 * self.world.time
        for k,clist in self.world.characters.items():
            for c in clist:
                self.scores[c.name] = self.scores[c.name] + 1
            
    def draw(self):
        self.world.printit()
        print("SCORES")
        for c,s in self.scores.items():
            print(c,s)
        print("EVENTS")
        for e in self.events:
            print(e)

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
        self.scores[c.name] = -self.world.time
