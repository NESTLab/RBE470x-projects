# this version of monster is used to determine the type of monster when it is supposed to be hidden (see readme)
class Monster:
    def __init__(self, x, y):
        self.prevX = x
        self.prevY = y
        self.x = x
        self.y = y
        self.velocityX = None
        self.velocityY = None

        self.timesIActedSmart = 0
        self.type = None
        self.path = []

    def getPath(self, wrld):
        self.checkVelocity(wrld)
        path = [Node(self.x, self.y)]
        isOutOfBounds = False
        i = 1
        while not isOutOfBounds:
            (nx, ny) = (self.prevX + self.velocityX*i, self.prevY + self.velocityY*i)
            # If next pos is out of bounds, must change direction
            if ((nx < 0) or (nx >= wrld.width()) or
                    (ny < 0) or (ny >= wrld.height())):
                isOutOfBounds = True
            else:
                path.append(Node(self.x + self.velocityX*i, self.y + self.velocityY*i))
                i += 1
        return path

    def checkVelocity(self, wrld):
        currVelocityX = self.x - self.prevX
        currVelocityY = self.y - self.prevY
        if self.velocityX is None or self.must_change_direction(wrld):
            self.velocityX = currVelocityX
            self.velocityY = currVelocityY
            self.prevX = self.x
            self.prevY = self.y

        elif self.velocityX == currVelocityX and self.velocityY == currVelocityY and self.type != "stupid":
            self.timesIActedSmart += 1
            self.prevX = self.x
            self.prevY = self.y

            # if moved in a manner consistent to self-preserving monster, then it's smart
            if self.timesIActedSmart > 2:
                self.type = "smart"
        elif self.timesIActedSmart < 8:
            self.type = "stupid"
        return

    # stolen from Self Preserving Monster
    def must_change_direction(self, wrld):
        # Get next desired position
        (nx, ny) = (self.prevX + self.velocityX, self.prevY + self.velocityY)
        # If next pos is out of bounds, must change direction
        if ((nx < 0) or (nx >= wrld.width()) or
                (ny < 0) or (ny >= wrld.height())):
            return True
        # If these cells are an explosion, a wall, or a monster, go away
        # return (wrld.explosion_at(self.x, self.y) or
        return (wrld.wall_at(nx, ny) or
                wrld.exit_at(nx, ny))


class Node():
    def __init__(self, x, y, hval=0, gval=0, parent=None):
        self.x = x
        self.y = y
        self.hval = hval
        self.gval = gval
        self.fval = hval + gval
        self.parent = parent

    # def __eq__(self, other):
    #    return self.position == other.position


