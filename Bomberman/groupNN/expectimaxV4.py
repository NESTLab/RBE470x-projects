import sys
import math

def cost(wrld):
    #get monster
    m = next(iter(wrld.monsters.values()))[0]
    try:
        #get char
        c = next(iter(wrld.characters.values()))[0]
    #if charicter is dead
    except IndexError:
        return -100
    #if charicter reached exit
    except StopIteration:
        return 1

    #hardcode exit
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
    #if position is at exit
    if c.x == exit[0] and c.y == exit[1]:
        return 1


    # cost = -manhattandist([c.x,  c.y], [exit[0],exit[1]]) - 10**(3-manhattandist( [c.x,  c.y], [m.x,m.y]))
    #the cost from the monster is exponential, shifted from 4 away from the charicter up
    #make it more expensive to go to positions that are closed off
    cost = - 5 ** (4 - moveDist([c.x, c.y], [m.x, m.y])) - 5 ** (8 - len(find_actions(wrld, c.x, c.y)))
    return cost


#find how far something has to move to get to you by finding the length of the greatest side, due to 8 connected
def moveDist(start, end):
    return max(abs(start[0] - end[0]), abs(start[1] - end[1]))

def exptectiMax(wrld, Depth):
    #this can't do 0 depth or non monsters, as error would be thrown
    #may need to do try cach for above here, but it should exit before this becomes a conflict
    #TODO Watch for bug here, iteration error. To fix, see Cost or expVal
    m = next(iter(wrld.monsters.values()))[0]
    c = next(iter(wrld.characters.values()))[0]

    #get actions
    mActList = find_actions(wrld, m.x, m.y)
    cActList = find_actions(wrld, c.x, c.y)

    #set worst state possible
    BestAction = [ -(sys.maxsize-1), [c.x,c.y]]

    #for every action that the monster or you take, store the action that corrilates to the value
    #and return that
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
    #check and end early if the char exited
    Exited = False
    m = None
    c = None
    m = next(iter(wrld.monsters.values()))[0]

    try:
        c = next(iter(wrld.characters.values()))[0]
    #if Dead
    except IndexError:
        Exited = True
    #if reached the exit
    except StopIteration:
        Exited = True

    #evaluate board state
    if Depth >= dM or Exited:
        v = cost(wrld)
        return v
    #set cost to 0, as it will be a sum, inital state shouldn't affect it
    v=0

    #for each action
    mActList = find_actions(wrld, m.x,m.y)
    cActList = find_actions(wrld, c.x,c.y)

    #get all possible worlds
    for mAct in mActList:
        for cAct in cActList:
            m.move(-m.x + mAct[0], -m.y + mAct[1])
            c.move(-c.x + cAct[0], -c.y + cAct[1])
            (newwrld, events) = wrld.next()

            #TODO Update this so that actions, such as moving towards the player, or moving in the same direction it was
            #is higher
            p = 1/(len(mActList)+len(cActList)) #can change later
            #update as sum of all Ps
            v = v + p*maxValue(newwrld, Depth+1, dM)

    return v

def maxValue(wrld, Depth, dM):

#see logic of expval
    Exited = False
    m = None
    c = None
    m = next(iter(wrld.monsters.values()))[0]
    try:
        c = next(iter(wrld.characters.values()))[0]
    except IndexError:
        Exited = True
    except StopIteration:
        Exited = True

    if Depth >= dM or Exited:
        v = cost(wrld)
        return v

    #set so that any value is better than it
    v = -(sys.maxsize-1)

    mActList = find_actions(wrld, m.x, m.y)
    cActList = find_actions(wrld, c.x, c.y)

    for mAct in mActList:
        for cAct in cActList:
            m.move(-m.x + mAct[0], -m.y + mAct[1])
            c.move(-c.x + cAct[0], -c.y + cAct[1])
            (newwrld, events) = wrld.next()
            #max of expectimax
            v = max(v, expVal(newwrld, Depth + 1, dM))

    return v

def find_actions(state, x, y):
    actions = []

    width = state.width()
    height = state.height()


    #check 8 connected for walls and out of bounds.
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