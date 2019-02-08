from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        w = wrld
        w.me(self).place_bomb()
        w.me(self).move(1,0)
        for i in range(5):
            w = w.next()[0]
            w.printit()
