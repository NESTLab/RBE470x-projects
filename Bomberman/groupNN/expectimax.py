


def expectimax_search(grid):

    return expVal

def expVal():

def find_player(grid):



def find_actions(state, x, y):
    actions = []

    width = state.width()
    height = state.height()

    for i in range(3):

        i -= 1

        for j in range(3):

            j -= 1

            if not (x + i >= width or x + i <= 0 or y + j >= height or y + j <= 0):

                if not state.wall_at(x + i, y + j):

                    actions.append([[x + i, y + j], 0])

                    # TODO Implement method to check for our own bomb
                    # TODO Check for our own bomb using the entity
                    # actions.append([[x + i, y + j], 1])

    return actions

# Input: current board state, character x, character y
# Return: All possible world grids
def find_board_states(cur_state, type, x, y):

    # Possible board states for a player
    if type == 0:

        actions = find_actions(cur_state, x, y)







def look_for_empty_cell(self, wrld):
    # List of empty cells
    cells = []
    # Go through neighboring cells
    for dx in [-1, 0, 1]:
        # Avoid out-of-bounds access
        if ((self.x + dx >= 0) and (self.x + dx < wrld.width())):
            for dy in [-1, 0, 1]:
                # Avoid out-of-bounds access
                if ((self.y + dy >= 0) and (self.y + dy < wrld.height())):
                    # Is this cell walkable?
                    if not wrld.wall_at(self.x + dx, self.y + dy):
                        cells.append((dx, dy))
    # All done
    return cells

def eval_function(state):
    pass