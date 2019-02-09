# Required Software #

To run Bomberman, you'll need Python 3 with the `colorama` package. To install it, type either

    pip install colorama
    
if Python 3 is your default version, or

    pip3 install colorama
    
if you have both Python 2 and Python 3 installed on your system.

# Running Bomberman #

Go into the folder `scenario1/` or `scenario2/`:

    $ cd scenario1

Both folders contain five Python files called `variant1.py`, `variant2.py`,
`variant3.py`, `variant4.py`, and `variant5.py`. To run a specific variant, type
one of these two commands, depending on whether your Python executable defaults
to Python 3 or not:

    $ python variant1.py
    $ python3 variant1.py

# Game Rules #

The game can be played in two modalities: escape mode and last-man-standing
mode.

## Escape Mode ##

Your character must escape the world through the exit cell. The game ends when
either of these conditions is true:

1. The maximum number of steps (`max_time`) has expired.
2. The character reaches the exit cell.
3. The character is killed by a monster. This occurs when a monster occupies the
   same cell as the character.
4. The character is killed by the explosion of a bomb.

Multiple players can be added to the world. In this case, the game ends when the
last character exits the world or is killed.

## Last-Man-Standing Mode ##

In this modality there is no exit cell. The only way for a game to end is when a
single character is left, or the maximum time has expired. This modality makes
sense when the game starts with multiple players.

## Scores ##

Each character has a score calculated as follows:
1. The score starts at `-max_time` points
2. For each step the character is still alive, the score is increased by one point
3. Every wall destroyed awards 10 extra points
4. Every monster killed awards 50 extra points
5. Every character killed awards 100 extra points
6. If your character escapes the world, it gets `2 * time` extra points, where `time` is the time left

# Coding Your Agent #

## Relevant Definitions ##

Refer to the [example skeleton
code](https://github.com/NESTLab/CS4341-projects/blob/master/Bomberman/groupNN/testcharacter.py),
also reported here:

    # This is necessary to find the main code
    import sys
    sys.path.insert(0, '../bomberman')
    # Import necessary stuff
    from entity import CharacterEntity
    from colorama import Fore, Back
    
    class TestCharacter(CharacterEntity):
    
        def do(self, wrld):
            pass

This is the minimal amount of code to have a still character in the
environment. The method `CharacterEntity.do(self, wrld)` is the only one that
you have to implement to have your character do useful stuff.

The parameter `wrld` has type `SensedWorld` (definition
[here](https://github.com/NESTLab/CS4341-projects/blob/master/Bomberman/bomberman/sensed_world.py)),
which in turn is a subclass of `World` (definition
[here](https://github.com/NESTLab/CS4341-projects/blob/master/Bomberman/bomberman/world.py)).

The most useful methods and attributes in this class are the following:
- `wrld.width()`: returns the width of the world
- `wrld.height()`: returns the height of the world
- `wrld.empty_at(x, y)`: returns `True` if the cell `(x,y)` is empty
- `wrld.exit_at(x, y)`: returns `True` if the cell `(x,y)` is the exit
- `wrld.wall_at(x, y)`: returns `True` if the cell `(x,y)` is a wall
- `wrld.bomb_at(x, y)`: returns a `BombEntity` object if the cell `(x,y)` is occupied by a bomb; `None` otherwise
- `wrld.explosion_at(x, y)`: returns an `ExplosionEntity` object if the cell `(x,y)` is occupied by an explosion; `None` otherwise
- `wrld.monsters_at(x, y)`: returns a list of `MonsterEntity` objects if the cell `(x,y)` is occupied by monsters; the empty list `[]` otherwise
- `wrld.characters_at(x, y)`: returns a list of `CharacterEntity` objects if the cell `(x,y)` is occupied by characters; the empty list `[]` otherwise
- `wrld.printit()`: prints the current state of the world
- `wrld.me()`: returns the object in the world that refers to the state of the current character
- `wrld.scores` is a dictionary `{ character_name : score }` that contains the score of every character.

## Available Actions ##

Your character can perform two basic actions: moving and placing a bomb.

To move, use the method `CharacterEntity.move(dx,dy)`. This method sets the
direction of motion to `(dx,dy)`. The values of `dx` and `dy` can be `-1`, `0`,
or `1`. Any other value is clamped to those three values, so agents can only
move by at most one cell per step. 8-neighborhood motion is allowed. Example:

    class TestCharacter(CharacterEntity):
        def do(self, wrld):
            # Moves one cell to the right
            self.move(1,0)

Once you set a direction for the agent, that direction is kept in subsequent
steps until you change it. To stop the agent, you must explicitly call
`self.move(0,0)`.

To place a bomb, call `CharacterEntity.place_bomb()`. The bomb is placed at the
current position of the character. The bomb will start ticking and eventually
will explode when the timer expires. When a bomb explodes, it creates a number
of explosion cells. If a wall, a character, or a monster are touched by an
explosion cell, they are removed from the board. Bombs, exit cells, and other
explosions are immune to explosion cells. A character can have only one bomb
ticking at any given time. Any attempt to place a bomb when another one has been
placed by the same character is ignored. The action of placing a bomb is reset
at each time step, whether or not the action was successful.

## Searching through World Configurations ##

In your code you might need to search through several world states. You have two
methods to do this:
- `SensedWorld.from_world(w)` takes a `World` object (either `RealWorld` or
  `SensedWorld`) and clones it. All the data about characters, monsters, bombs,
  explosions, etc is cloned into new objects. This means that you can modify the
  returned world without affecting other existing world instances. An important
  aspect of this operation is that characters and monsters are not cloned.
  Rather, each character in the real world is cloned into a dummy
  `CharacterEntity` object, and each monster is cloned into a dummy
  `MonsterEntity`. This is to prevent your code from modifying or peeking other
  agents' private information.
- `SensedWorld.next()` returns a tuple `(new_world, events)`. The first element
  of the tuple is a clone created by `SensedWorld.from_world()` advanced by one
  step. In `new_world` time has decreased by one, bombs whose timer expired have
  exploded, explosions have disappeared, etc. according to the logic of the
  game. If you modified the actions of the agents (e.g, you called `move()` on a
  monster), `SensedWorld.next()` will take care of that, too. The second element
  in the tuple, `events`, is a list of events that occurred in that world
  configuration. Refer to
  [events.py](https://github.com/NESTLab/CS4341-projects/blob/master/Bomberman/bomberman/events.py)
  for a list of possible events.

## Visual Debugging ##

The game offers a simple way to mark the cells for debugging purposes. This
could be useful, for instance, to visually mark the path A* has found. To mark a
cell, use `CharacterEntity.set_cell_color(x,y,color)`:

    # Import color definitions
    from colorama import Fore, Back
    
    class TestCharacter(CharacterEntity):
        def do(self, wrld):
            # ... some code
            # Color cell (2,3)
            self.set_cell_color(2, 3, Fore.RED + Back.GREEN)
            # ... more code

Refer to the [documentation of Colorama](https://pypi.org/project/colorama/) for
a list of available colors.

For example, this code marks the entire top row of the world:

    # Import color definitions
    from colorama import Fore, Back
    
    class TestCharacter(CharacterEntity):
        def do(self, wrld):
            for x in range(wrld.width()):
                self.set_cell_color(x, 0, Fore.RED + Back.GREEN)

Notice that the marked cells are overwritten by walls, bombs, explosions,
monsters, and characters.

# Map Format #

You can modify the maps to change their configuration. The standard maps that
are given to you are those that define the goals of your work, but if you want
to play around other maps for testing purposes, the format is as follows.

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
    |         E|
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
  is allowed in any map. Maps can also have no exit cells, and that corresponds
  to the Last-Man-Standing mode.

Any character or monster must be added in a Python file that runs the scenario.

