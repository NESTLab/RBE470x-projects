from real_world import RealWorld
from events import Event
import colorama
import pygame
import math
import game


class Tournament(game.Game):
    def __init__(self, width, height, max_time, bomb_time, expl_duration, expl_range):
        super().__init__(width, height, max_time, bomb_time, expl_duration, expl_range)
        self.timesKilledByMonster = 0
        self.timesKilledByTheColdAndUnforgivingPassageOfTime = 0
        self.timesFoundExit = 0
        self.timesLastManStanding = 0
        self.timesQuit = 0

    def runTournament(self, wait=0):
        """ Main game loop. """

        for i in range(0, 100):

            if wait is 0:
                def step():
                    input("Press Enter to continue or CTRL-C to stop...")
            else:
                def step():
                    pygame.time.wait(abs(wait))

            colorama.init(autoreset=True)
            self.display_gui()
            self.draw()

            isDone = self.done()
            while isDone is False:
                self.display_gui()
                (self.world, self.events) = self.world.next()
                self.display_gui()
                self.draw()
                step()
            colorama.deinit()

            if isDone == "quit":
                self.timesQuit += 1

            elif isDone == "killed by monster":
                self.timesKilledByMonster += 1

            elif isDone == "found exit":
                self.timesFoundExit += 1

            elif isDone == "timeout":
                self.timesKilledByTheColdAndUnforgivingPassageOfTime += 1

            elif isDone == "last man standing":
                self.timesLastManStanding += 1

        print("Times quit: " + str(self.timesQuit))
        print("Times killed by monster: " + str(self.timesKilledByMonster))
        print("Times found exit: " + str(self.timesFoundExit))
        print("Times killed by the cold and unforgiving passage of time: " + str(self.timesKilledByTheColdAndUnforgivingPassageOfTime))
        print("Times last man standing: " + str(self.timesLastManStanding))

    def done(self):
        # User Exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        for event in self.world.events:
            if event.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                return "killed by monster"
            if event.tpe == Event.CHARACTER_FOUND_EXIT:
                return "found exit"
        # Time's up
        if self.world.time <= 0:
            return "timeout"
        # Last man standing
        if not self.world.exitcell:
            count = 0
            for k,clist in self.world.characters.items():
                count = count + len(clist)
            if count == 0:
                return "last man standing"
        return False

