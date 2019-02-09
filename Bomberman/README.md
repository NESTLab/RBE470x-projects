# Required software #

To run Bomberman, you'll need Python 3 with the `colorama` package. To install it, type either

    pip install colorama
    
if Python 3 is your default version, or

    pip3 install colorama
    
if you have both Python 2 and Python 3 installed on your system.

# Running Bomberman #

# Map Format #

You can modify the maps to change their configuration. The standard maps that
are given to you are those that define the goals of your work, but if you want
to play around other maps for testinf purposes, the format is as follows.

The first four lines must be in format `param value`, where `value` is a
positive integer. For example:

    max_time 100
    bomb_time 2
    expl_duration 3
    expl_range 4

This configures the game as follows:
- The maximum time to complete the scenario is 100 steps
- The time a bomb takes to explode is 2 steps
- An explosion stays in the map for 3 steps
- The explosion range around the bomb is 4 cells

These four lines are followed by the grid configuration. For example:

    +----------+
    |          |
    |WWWWW     |
    |       WWW|
    +----------+

- The grid must be composed of a top line `+---+` with as many `-` as
wanted. The number of `-` of the first line defines the width of the world.
- Every subsequent line must start and end with `|`, with as many characters in
between to match the width defined by the first line.
- The last line must be identical to the first line.
- The allowed characters between the top and bottom lines are spaces (for
  walkable cells), `W` for walls, and `E` for the exit cell. Only one exit cell
  is allowed in any map. Maps can also have no exit cells.

Any character or monster must be added in a Python file that runs the scenario.

