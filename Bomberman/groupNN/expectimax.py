import sys
import math

def cost(wrld):
    m = next(iter(wrld.monsters.values()))[0]
    try:
        c = next(iter(wrld.characters.values()))[0]
    except IndexError:
        return -100
    except StopIteration:
        return 1

    exit = [7, 18]#wildly inefficent
    # get current position
    # check every gridcell for the exit. Uses the last exit found as the "goal"
    # for i in range(wrld.width()):
    #
    #     for j in range(wrld.height()):
    #
    #         if wrld.exit_at(i, j):
    #             exit = [i, j]
    #if at goal, return high reward
    if c.x == exit[0] and c.y == exit[1]:
        return 1

    #if not at goal, prioritize getting to the goal linearly and staying away from the monster exponentially,
    #monster only has real effect when 3 away (may need to make 4)
    # cost = -manhattandist([c.x,  c.y], [exit[0],exit[1]]) - 10**(3-manhattandist( [c.x,  c.y], [m.x,m.y]))
    cost = - 5 ** (4 - manhattandist([c.x, c.y], [m.x, m.y])) -5**(8-len(find_actions(wrld, c.x, c.y)))
    return cost

def manhattandist(start, end):
    return max(abs(start[0] - end[0]), abs(start[1] - end[1]))

def exptectiMax(wrld, Depth):

    m = next(iter(wrld.monsters.values()))[0]
    c = next(iter(wrld.characters.values()))[0]

    mActList = find_actions(wrld, m.x, m.y)
    cActList = find_actions(wrld, c.x, c.y)

    BestAction = [ -(sys.maxsize-1), [c.x,c.y]]

    for mAct in mActList:
        for cAct in cActList:
            m.move(-m.x + mAct[0], -m.y + mAct[1])
            c.move(-c.x + cAct[0], -c.y + cAct[1])
            (newwrld, events) = wrld.next()
            v = expVal(newwrld,0,Depth)
            #print("x,y,v", cAct[0], cAct[1], v)
            if v > BestAction[0]:
                BestAction = [v, cAct]
    return BestAction[1]


def expVal(wrld, Depth, dM):
    Dead = False
    m = None
    c = None
    m = next(iter(wrld.monsters.values()))[0]
    try:
        c = next(iter(wrld.characters.values()))[0]
    except IndexError:
        Dead = True
    except StopIteration:
        Dead = True
    if Depth >= dM or Dead:
        v = cost(wrld)
        return v
    v=0


    mActList = find_actions(wrld, m.x,m.y)
    cActList = find_actions(wrld, c.x,c.y)

    for mAct in mActList:
        for cAct in cActList:
            m.move(-m.x + mAct[0], -m.y + mAct[1])
            c.move(-c.x + cAct[0], -c.y + cAct[1])
            (newwrld, events) = wrld.next()
            p = 1/(len(mActList)+len(cActList)) #can change later
            v = v + p*maxValue(newwrld, Depth+1, dM)

    return v

def maxValue(wrld, Depth, dM):

    Dead = False
    m = None
    c = None
    m = next(iter(wrld.monsters.values()))[0]
    try:
        c = next(iter(wrld.characters.values()))[0]
    except IndexError:
        Dead = True
    except StopIteration:
        Dead = True

    if Depth >= dM or Dead:
        v = cost(wrld)
        return v

    v = -(sys.maxsize-1)

    mActList = find_actions(wrld, m.x, m.y)
    cActList = find_actions(wrld, c.x, c.y)

    for mAct in mActList:
        for cAct in cActList:
            m.move(-m.x + mAct[0], -m.y + mAct[1])
            c.move(-c.x + cAct[0], -c.y + cAct[1])
            (newwrld, events) = wrld.next()
            v = max(v, expVal(newwrld, Depth + 1, dM))

    return v

def find_actions(state, x, y):
    actions = []

    width = state.width()
    height = state.height()

    for i in range(3):

        i -= 1

        for j in range(3):

            j -= 1

            if not (x + i >= width or x + i < 0 or y + j >= height or y + j < 0):

                if (not(i == 0 and j == 0)) and not (state.wall_at(x + i, y + j)):

                    actions.append([x + i, y + j])

                    # TODO Implement method to check for our own bomb
                    # TODO Check for our own bomb using the entity
                    # actions.append([[x + i, y + j], 1])

    return actions



# def look_for_empty_cell(self, wrld):
#     # List of empty cells
#     cells = []
#     # Go through neighboring cells
#     for dx in [-1, 0, 1]:
#         # Avoid out-of-bounds access
#         if ((self.x + dx >= 0) and (self.x + dx < wrld.width())):
#             for dy in [-1, 0, 1]:
#                 # Avoid out-of-bounds access
#                 if ((self.y + dy >= 0) and (self.y + dy < wrld.height())):
#                     # Is this cell walkable?
#                     if not wrld.wall_at(self.x + dx, self.y + dy):
#                         cells.append((dx, dy))
#     # All done
#     return cells
#
# def eval_function(state):
#     pass