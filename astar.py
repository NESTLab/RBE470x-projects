import customEntities

# includes the a star code as well as some useful utility functions


# take into account walls; if there is a wall in the way, move to it and bomb the heck out of it
# Returns
# > Boolean, <Nodes> tuple where Boolean says whether there is a clear path to the end and Nodes returns
# either the path or the set of closed nodes
def calculateAStarPath(startNode, endNode, wrld, listOfMonsters, shouldPathAroundMonsters):
    openNodes = []
    closedNodes = []
    # End node is position 7, 18
    startNode = customEntities.Node(startNode.x, startNode.y)
    openNodes.append(startNode)
    while len(openNodes) > 0:
        minNode = openNodes[0]
        currIndex = 0

        # find the smallest node fval and append it
        for index, currNode in enumerate(openNodes):
            if currNode.fval < minNode.fval:
                minNode = currNode
                currIndex = index

        openNodes.pop(currIndex)
        closedNodes.append(minNode)

        if minNode.x == endNode.x and minNode.y == endNode.y:
            path = []
            currNode = minNode
            while currNode is not None:
                path.append(currNode)
                currNode = currNode.parent
            return True, path[::-1]
        for neighbor in getNeighbors(minNode, endNode, wrld):
            isClosed = False
            isOpen = False

            sameNode = None
            nodeIndex = None
            for closedNode in closedNodes:
                if neighbor.x == closedNode.x and neighbor.y == closedNode.y:
                    isClosed = True
                    break
            for index, openNode in enumerate(openNodes):
                if neighbor.x == openNode.x and neighbor.y == openNode.y:
                    isOpen = True
                    sameNode = openNode
                    nodeIndex = index
                    break

            if not isClosed:
                neighbor.gval = minNode.gval + 1
                neighbor.hval = distanceBetweenNodes(neighbor, endNode, listOfMonsters, shouldPathAroundMonsters)
                neighbor.fval = neighbor.gval + neighbor.hval

                if isOpen and neighbor.fval < sameNode.fval:
                    openNodes[nodeIndex] = neighbor

                elif not isOpen:
                    openNodes.append(neighbor)
    return False, closedNodes


# code modified from selfpreserving_monster.py
def getNeighbors(node, endNode, wrld):
    listOfNeighbors = []
    # Go through neighboring cells
    for dx in [-1, 0, 1]:
        # Avoid out-of-bounds access
        if (node.x + dx >= 0) and (node.x + dx < wrld.width()):
            for dy in [-1, 0, 1]:
                # Avoid out-of-bounds access
                if (node.y + dy >= 0) and (node.y + dy < wrld.height()):
                    # add node if it's the end node, useful if calculating distance to monster
                    if endNode.x == node.x + dx and endNode.y == node.y + dy:
                        listOfNeighbors.append(customEntities.Node(node.x + dx, node.y + dy, parent=node))
                    # Is this cell not a wall or an explosion?
                    elif not (wrld.wall_at(node.x + dx, node.y + dy) or
                              wrld.explosion_at(node.x + dx, node.y + dy)):
                        if not (dx == 0 and dy == 0):
                            listOfNeighbors.append(customEntities.Node(node.x + dx, node.y + dy, parent=node))
    # All done
    return listOfNeighbors


# absolute distance between nodes
def absoluteDistanceBetweenNodes(currNode, endNode):
    xDistance = abs(endNode.x - currNode.x)
    yDistance = abs(endNode.y - currNode.y)

    return xDistance + yDistance


# distance between two nodes
def distanceBetweenNodes(currNode, endNode, listOfMonsters, shouldPathAroundMonsters):
    xDistance = abs(endNode.x - currNode.x)
    yDistance = abs(endNode.y - currNode.y)

    # if the node is close to any monster and the endnode is not a monster, try to avoid it

    if shouldPathAroundMonsters:
        for i in range(0, 4):
            for monster in listOfMonsters:
                if monster.type == 'stupid' and i < 3:
                    if (monster.x - i <= currNode.x <= monster.x + i) \
                            and (monster.y - i <= currNode.y <= monster.y + i):
                        return max(xDistance, yDistance) + 300 - i * 100

                else:
                    if (monster.x - i <= currNode.x <= monster.x + i) \
                            and (monster.y - i <= currNode.y <= monster.y + i):
                        return max(xDistance, yDistance) + 300 - i * 100

    # moving diagonally is one move so can combine x and y distance
    return max(xDistance, yDistance)
