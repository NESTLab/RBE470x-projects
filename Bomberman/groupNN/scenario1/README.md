# Your goal #

In this scenario, you must plan the route of your agent from the top-left
corner to the exit.

## Variant 1: Alone in the world ##

In the first variant of this scenario, the world is deterministic and your agent
is alone in the environment.

## Variant 2: Stupid monster ##

In the second variant of this scenario, a stupid monster is present. The monster
chooses its next cell uniformly at random among the possible reachable cells.

## Variant 3: Self-preserving monster ##

In the third variant of this scenario, a smarter monster is present:
- The monster goes straight until it has reached an obstacle
- When it reaches an obstacle, it changes direction at random among the cells
  that are walkable and are not an explosion (if an agent, monster or character,
  touches an explosion, it dies)
- If the 8-distance of your agent to the monster is 1, the monster attacks your
  agent immediately and kills it

## Variant 4: Aggressive monster ##

In the fourth variant of this scenario, an aggressive monster is present:
- The monster goes straight until it has reached an obstacle
- When it reaches an obstacle, it changes direction at random among the cells
  that are walkable and are not an explosion (if an agent, monster or character,
  touches an explosion, it dies)
- If the 8-distance of your agent to the monster is 2, the monster moves towards
  your agent and attempts to kill it

## Variant 5: Stupid and Aggressive monsters together ##

In the fifth variant of this scenario, two monsters are present: an aggressive
one and a stupid one.
