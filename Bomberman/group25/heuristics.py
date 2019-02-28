import customEntities
import astar
import math

# first version of nodevalue
def nodeValue(world, player):
    value = 0
    actions = world.events

    # exit found or character lost?
    for a in actions:
        if a.tpe == a.CHARACTER_FOUND_EXIT:
            return 11111
        elif a.tpe == a.BOMB_HIT_CHARACTER or a.tpe == a.CHARACTER_KILLED_BY_MONSTER:
            return -11111
        else:
            value += 2

    x = player.x
    y = player.y

    # check surroundings for monsters
    # will also add code to check for bombs
    for m in world.monsters:
        for b in world.bombs:
            if y-2 >= 0:
                if m.y != y-2:
                    value += 5
                else:
                    if x-2 >= 0:
                        if m.x != x-2:
                            value += 5
                        else:
                            value -= 2 * m.x
                    if x+2 < world.height():
                        if m.x != x+2:
                            value += 5
                        else:
                            value -= 2 * m.x
                if b.y != y-2:
                    value += 5
                else:
                    if x-2 >= 0:
                        if b.x != x-2:
                            value += 5
                        else:
                            value -= 2 * b.x
                    if x+2 < world.height():
                        if b.x != x+2:
                            value += 5
                        else:
                            value -= 2 * b.x
            if y+2 < world.width():
                if m.y != y+2:
                    value += 5
                else:
                    if x-2 >= 0:
                        if m.x != x-2:
                            value += 5
                        else:
                            value -= 2 * m.x
                    if x+2 < world.height():
                        if m.x != x+2:
                            value += 5
                        else:
                            value -= 2 * m.x
                if b.y != y+2:
                    value += 5
                else:
                    if x-2 >= 0:
                        if b.x != x-2:
                            value += 5
                        else:
                            value -= 2 * b.x
                    if x+2 < world.height():
                        if b.x != x+2:
                            value += 5
                        else:
                            value -= 2 * b.x
    return value

# second version of nodeValue, for the A star character specifically
# currNode must contain:
#   monsters
#   distanceStupid
#   distanceSmart
#   bombTimer
def nodeValueAStar(node, wrld):

    # if there's an explosion, don't add
    if wrld.explosion_at(node.x, node.y):
        return None

    # TODO account for other players bombs
    # do not include the nodes that would be in bomb's path of explosion
    for k, bomb in wrld.bombs.items():
        if node.bombTimer <= 2:
            bombRange = wrld.expl_range
            for x in range(-bombRange, bombRange):
                if node.x == bomb.x + x and node.y == bomb.y:
                    return None
            for y in range(-bombRange, bombRange):
                if node.x == bomb.x and node.y == bomb.y + y:
                    return None
    node.hval = math.inf

    currSum = 0
    # for monster in monsterlist:
    for monster in node.monsters:
        pathBetweenSelfAndMonster = astar.calculateAStarPath(node, monster, wrld, node.monsters, False)
        myDistance = len(astar.calculateAStarPath(node, monster, wrld, node.monsters, False)[1])

        # if there is a path between myself and the monster
        if pathBetweenSelfAndMonster[0]:
            distance = len(pathBetweenSelfAndMonster[1])
            # distance = self.distanceBetweenNodes(node, monster, False)
            if myDistance < node.distanceSmart and monster.type == "smart":
                if distance < (node.distanceSmart - 1):
                    # try very hard not to get into detection range
                    currSum -= 5

                elif distance < (node.distanceSmart - 2):
                    currSum -= 10

                currSum += distance

            elif myDistance < node.distanceStupid + 1:
                currSum += distance
    node.hval = currSum
    return node

