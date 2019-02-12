import queue

class gridcell():

    def __init__(self, current, camefrom = None):
        self.current = current
        self.camefrom = camefrom

def getNextStep(start, end, wrld):
    pathNode = greedyBFS(start, end, wrld)

    prev = pathNode

    while pathNode.current is not start:
        prev = pathNode.current
        pathNode = pathNode.camefrom

    return prev

def greedyBFS(start, end, wrld):
    evaluated = []

    startcell = gridcell(start)
    endcell = gridcell(end)

    notEvaluated = [(manhattandist(startcell, endcell), startcell)]

    while notEvaluated:

        notEvaluated.sort(reverse=False, key=lambda x: x[0])

        popped = notEvaluated.pop(0)[1]

        if popped.current[0] == end[0] and popped.current[1] == end[1]:

            return popped

        evaluated.append(popped.current)

        width = wrld.width()
        height = wrld.height()

        x = popped.current[0]
        y = popped.current[1]

        for i in range(3):

            i -= 1

            for j in range(3):

                j -= 1

                if not (x + i >= width or x + i <= 0 or y + j >= height or y + j <= 0):

                    if [x + i, y + j] not in evaluated and not wrld.wall_at(x + i, y + j):
                        current = gridcell([x + i, y + j], popped)
                        notEvaluated.append((manhattandist(current, endcell), current))


def manhattandist(startcell, endcell):

    start = startcell.current
    end = endcell.current

    return abs(start[0] - end[0]) + abs(start[1] - end[1])