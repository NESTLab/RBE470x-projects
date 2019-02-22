# This is necessary to find the main code
import sys
import expectimax as EM

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity

from colorama import Fore, Back

class ExpectiCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
        meX = wrld.me(self).x
        meY = wrld.me(self).y

        goTo = EM.exptectiMax(wrld,2)
        self.move(-meX + goTo[0], -meY + goTo[1])

