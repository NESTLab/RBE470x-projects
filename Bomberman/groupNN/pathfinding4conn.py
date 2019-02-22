import queue


#an objct that holds the position of the gridcell, and the previous object
#(IE Postition) that the grid came from. This "camefrom" is used in the Greedy bfs
#(And eventually a*) to recreate the path from finish to start
class gridcell():

    def __init__(self, current, camefrom = None):
        self.current = current
        self.camefrom = camefrom

#getNextStep([x,y], [x,y], world)->[x,y]
#Given a start tuple [x,y], end tuple [x,y] and the world
#returns a tuple [x,y] that is the next position to move to using the current algorithm
#Currently GREEDYBFS
def getNextStep(start, end, wrld, w):
    #Call pathing algorithm, returns Gridcell with complete path to be reconstructed
    pathNode = greedyBFS(start, end, wrld,w)

    prev = pathNode

    #reverse order of the graph by following camefrom obj until reaching the start position.
    #use this to find the positon that comes just after the start position
    while pathNode is not None and pathNode.current is not start:
        prev = pathNode.current
        pathNode = pathNode.camefrom
    if pathNode is None:
        return None
    #return the position just after the start position
    return prev

#greedyBFS([x,y], [x,y], world)->gridcell
#Given a start tuple (usually players's start) [x,y], end tuple [x,y] and the world
#Return a gridcell at the goal. The <gridcell>.camefrom can be used to assemble the path to the goal
#uses a greedy BFS with a manhattan distance as a heuristic
def greedyBFS(start, end, wrld,w):
    #List of evaluated [x,y] pairs
    evaluated = []

    startcell = gridcell(start)
    endcell = gridcell(end)

    #heuristic is manhatten distance
    notEvaluated = [(manhattandist(startcell, endcell), startcell)]

    #While there are still evaluation options and not at the goal
    while notEvaluated:

        #sort via manhattan distance
        notEvaluated.sort(reverse=False, key=lambda x: x[0])

        #get gridcell object, don't worry about manhattan distance pairing
        popped = notEvaluated.pop(0)[1]

        #if at the goal
        if popped.current[0] == end[0] and popped.current[1] == end[1]:

            return popped

        #append the [x,y] coord corrisponding to the current gridcell to the list of evaluated
        evaluated.append(popped.current)

        width = wrld.width()
        height = wrld.height()

        #x,y position in world
        x = popped.current[0]
        y = popped.current[1]

        #check 8 connected. The current position is already in evaluated, so checking the current position
        #has no effect, not slow enought to require optimizeation
        for i, j in [[-1,0],[1,0],[0,-1],[0,1]]:

                #if the postition is in world bounds
                if not (x + i >= width or x + i < 0 or y + j >= height or y + j < 0):
                    #if the checked position has not already been checked, and there is not a wall at the location
                    if w ==1:
                        if [x + i, y + j] not in evaluated and not wrld.wall_at(x + i, y + j) and not wrld.explosion_at(x + i, y + j):
                            #create a new gridcell, with the previous postition being the gridcell used in this for for loop
                            #to reach the position
                            current = gridcell([x + i, y + j], popped)
                            #append to the fronter
                            notEvaluated.append((manhattandist(current, endcell), current))
                    else:
                        if [x + i, y + j] not in evaluated:
                            #create a new gridcell, with the previous postition being the gridcell used in this for for loop
                            #to reach the position
                            current = gridcell([x + i, y + j], popped)
                            #append to the fronter
                            notEvaluated.append((manhattandist(current, endcell), current))


#manhattandist(gridcell, gridcell)
#given 2 gridcells, use the current position of each to calculate the abs net manhattan distance
#startcell is usuall the current cell
#endcell is the goal cell
def manhattandist(startcell, endcell):

    start = startcell.current
    end = endcell.current

    return abs(start[0] - end[0]) + abs(start[1] - end[1])
