def nodevalue(self, world, player):
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
    return value
