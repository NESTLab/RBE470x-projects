# This is necessary to find the main code
import math
import sys
import random
from events import Event

from pygame import Color

from Bomberman.bomberman.sensed_world import SensedWorld

sys.path.insert(0, '../bomberman')
from entity import CharacterEntity
from colorama import Fore, Back


class TestCharacter(CharacterEntity):
    positionX = 0
    positionY = 0

    def do(self, wrld):
        width = wrld.width()
        height = wrld.height()

        # Policy-Iteration with Q-learning
        ## Whether the placing bomb & moving are exclusive?
        maxNextScore = None
        maxNextAction = (1, 1)
        LIVING_SCORE = 1
        discount = 0.9
        x = self.x
        y = self.y

        # moves
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                self.move(dx, dy)
                nextX = self.nextpos()[0]
                nextY = self.nextpos()[1]

                if (width > nextX >= 0 and \
                    0 <= nextY < height) and \
                        (wrld.empty_at(nextX, nextY) or \
                         wrld.characters_at(nextX, nextY) or \
                         wrld.exit_at(nextX, nextY)):
                    value = self.getValue(wrld)
                    if maxNextScore is None or value >= maxNextScore:
                        print("update action")
                        maxNextScore = value
                        maxNextAction = (dx, dy)
        self.move(maxNextAction[0], maxNextAction[1])
        print("final action: ", maxNextAction[0], maxNextAction[1])
        # if maxNextAction == (0, 0):
        #     self.place_bomb()
        # else:
        min_y_distance = 100
        min_x_distance = 100
        for m in wrld.monsters.values():
            y_distance = m[0].y - self.nextpos()[1]
            x_distance = abs(self.nextpos()[0] - m[0].x)
            if y_distance < min_y_distance:
                min_y_distance = y_distance
                min_x_distance = x_distance


        walls = True
        if self.y < height - 1:
            for i in range(wrld.width()):
                if not wrld.wall_at(i, self.y + 1):
                    walls = False
        if walls:
            if self.wall_test(x, y, wrld, False) and min_x_distance >= 5:
                self.place_bomb()
        else:
            if self.wall_test(x, y, wrld, True) and min_y_distance <= 5:
                self.place_bomb()

        # for i in range(wrld.width()):
        #     if wrld.monsters_at(i, self.nextpos()[1]):
        #         self.place_bomb()
        #     if self.nextpos()[1] < wrld.height() - 1 and wrld.monsters_at(i, self.nextpos()[1] + 1):
        #         self.place_bomb()


    def getValue(self, wrld):
        width = wrld.width()
        height = wrld.height()

        scoreList = {
            Event.BOMB_HIT_WALL: 20,
            Event.BOMB_HIT_MONSTER: 50,
            Event.BOMB_HIT_CHARACTER: -10000,
            Event.CHARACTER_KILLED_BY_MONSTER: -10000,
            Event.CHARACTER_FOUND_EXIT: 10000
        }
        score = 0

        # Assuming worst case of monsters
        for m in wrld.monsters.values():
            mdx = self.one(self.x - m[0].x)
            mdy = self.one(self.y - m[0].y)
            nextX = m[0].x + mdx
            nextY = m[0].y + mdy
            if (width > nextX >= 0 and \
                0 <= nextY < height) and \
                    (wrld.empty_at(nextX, nextY) or \
                     wrld.characters_at(nextX, nextY) or \
                     wrld.exit_at(nextX, nextY)):
                # Set move in wrld
                m[0].move(mdx, mdy)

        (newwrld, events) = wrld.next()

        # event scores(happens directly)
        for i in range(len(events)):
            score += scoreList.get(events[i].tpe)

        # TODO:other scores(happens indirectly)
        ## distance from exit

        x = self.nextpos()[0]
        y = self.nextpos()[1]

        # Vertical distance (progress) score
        score += 3 * y

        ## possible actions
        if y >= height - 4:
            score += 1000 / (width - x + 1)
        # else:
        #     score += abs(width/2 - x)

        ## distance from monster
        min_y_distance = 100
        min_x_distance = 100

        for m in wrld.monsters.values():
            y_distance = abs(self.nextpos()[1] - m[0].y)
            x_distance = abs(self.nextpos()[0] - m[0].x)

            if y_distance < min_y_distance:
                min_y_distance = y_distance
                min_x_distance = x_distance

        if self.wall_test(x, y, newwrld, True) \
                and not newwrld.bomb_at(x, y) \
                and min_y_distance <= 5\
                and min_x_distance >= 5:
            score += 1000

        minDistance = max(min_x_distance, min_y_distance)
        score -= 60 / (minDistance + 1)
        if min_y_distance <= 3 and (not self.wall_before(y, newwrld, 4)):
            score -= 100 / (min_y_distance+1)

        score -= 100 / (minDistance + 1)
        if minDistance < 3:
            score -= 500

        # for i in range(width):
        #     if newwrld.monsters_at(i, x):
        #         score -= 500
        #     if y < height - 1 and newwrld.monsters_at(i, x + 1):
        #         score -= 500

        if newwrld.monsters_at(x, y):
            score -= 10000

        ## position relative to bombs
        num_bombs = len(newwrld.bombs)
        for i in range(num_bombs):
            b = next(iter(newwrld.bombs.values()))

            if b.x == x or b.y == y:
                print("run!")
                score -= 1500
            else:
                score += 1

        if newwrld.explosion_at(x, y):
            score -= 10000

        return score

    def one(self, n):
        if n > 0:
            return 1
        elif n < 0:
            return -1
        else:
            return 0

    def wall_test(self, x, y, wrld, omni):
        width = wrld.width()
        height = wrld.height()
        test = False

        if y < height - 1:
            if 1 <= x <= width - 2:
                if wrld.wall_at(x - 1, y + 1) and wrld.wall_at(x + 1, y + 1):
                    test = True
            elif x == 0:
                if wrld.wall_at(x + 1, y + 1):
                    test = True
            elif x == width - 1:
                if wrld.wall_at(x + -1, y + 1):
                    test = True
        if test:
            return (not wrld.wall_at(x, y + 1)) == omni
        else:
            return False

    def wall_before(self, y, wrld, layers):
        if y + layers > wrld.height() -1:
            return False

        for l in range(layers):
            walls = True
            for i in range(wrld.width()):
                if not wrld.wall_at(i, self.y + l):
                    walls = False
            if walls:
                return True

        return False
