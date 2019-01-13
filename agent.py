import board
import random

#####################
# Agent definitions #
#####################



##################
# Abstract agent #
##################

class Agent(object):
    """Abstract agent class"""

    def __init__(self, name):
        """Class constructor"""
        # Agent name
        self.name = name
        # Uninitialized player - will be set upon starting a Game
        self.player = 0

    def go(self, brd):
        """Returns a column between 0 and (brd.w-1). The column must be free in the board."""
        raise NotImplementedError("Please implement this method")



##########################
# Randomly playing agent #
##########################

class RandomAgent(Agent):
    """Randomly playing agent"""

    def go(self, brd):
        return random.choice(brd.free_cols())



#####################
# Interactive Agent #
#####################

class InteractiveAgent(Agent):
    """Interactive player"""

    def go(self, brd):
        return int(input("Which column? "))
