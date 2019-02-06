import world

class SensedWorld(world.World):
    """The world state as seen by a monster or a robot"""

    def next(self):
        """Returns a new world state, along with the events that occurred"""
        new = WorldState.from_state(this)
        new.time = new.time - 1
        new.update_explosions()
        ev = new.update_bombs()
        return (new,ev)

