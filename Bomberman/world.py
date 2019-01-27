import sys
import entity
import cell

#########
# World #
#########

class World:
    """Game grid world"""

    def __init__(self, width, height, max_time):
        """Class constructor"""
        # Grid width
        self.width = width
        # Grid height
        self.height = height
        # Time left
        self.time = max_time
        # Grid data, initially empty
        self.data = [[cell.EmptyCell()] * height for i in range(width)]

    def at(self, x, y):
        return self.data[x][y]

    def place_empty(self, x, y):
        """Place an empty cell into the world"""
        self.data[x][y] = cell.EmptyCell()

    def place_exit(self, x, y):
        """Place the exit cell into the world"""
        self.data[x][y] = cell.ExitCell()

    def place_wall(self, x, y):
        """Place a wall cell into the world"""
        self.data[x][y] = cell.WallCell()

    def place_monster(self, monster):
        """Place a monster into the world"""
        self.data[monster.x][monster.y] = cell.MonsterCell(monster)

    def place_character(self, character):
        """Place a character into the world"""
        self.data[character.x][character.y] = cell.CharacterCell(character)

    def place_bomb(self, bomb):
        """Place a bomb into the world"""
        self.data[bomb.x][bomb.y] = cell.BombCell(bomb)

    def place_explosion(self, explosion, x, y):
        """Place an explosion into the world"""
        self.data[x][y] = cell.ExplosionCell(explosion)

    def move_entity(self, e):
        """Moves a movable entity in the world"""
        # Get the current cell data
        c = self.data[e.x][e.y]
        # Get the desired next position of the entity
        (nx, ny) = c.data.nextpos()
        # Make sure the position is within the bounds
        nx = max(0, min(self.width - 1, nx))
        ny = max(0, min(self.height - 1, ny))
        # Make sure the new position is different from the current one
        if((nx != e.x) or (ny != e.y)):
            # Make sure the new position can be occupied
            nc = self.data[nx][ny]
            if nc.tpe in [cell.Cell.WALL, cell.Cell.BOMB]:
                # Can't move, nothing to do
                return
            # Update grid cells
            # Prevent dynamic objects from being deleted
            if self.at(e.x, e.y).data == e:
                self.place_empty(e.x, e.y)
            # Update new cell
            self.data[nx][ny] = c
            # Save new entity position
            e.x = nx
            e.y = ny

    def draw(self):
        """Draws the current state of the world"""
        border = "+" + "-" * self.width + "+\n"
        print("\nTIME LEFT: ", self.time)
        sys.stdout.write(border)
        for y in range(self.height):
            sys.stdout.write("|")
            for x in range(self.width):
                self.data[x][y].draw()
            sys.stdout.write("|\n")
        sys.stdout.write(border)
        sys.stdout.flush()
