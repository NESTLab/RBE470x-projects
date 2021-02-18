import board
import agent
import time
from pathlib import Path

########
# Game #
########

class Game(object):
    """Game logic class"""

    # Class constructor.
    #
    # PARAM [int]         w:  the board width
    # PARAM [int]         h:  the board height
    # PARAM [int]         n:  the number of tokens to line up to win
    # PARAM [agent.Agent] p1: the agent for Player 1
    # PARAM [agent.Agent] p2: the agent for Player 2
    def __init__(self, w, h, n, p1, p2):
        """Class constructor"""
        # Create board
        self.board = board.Board([[0] * w for i in range(h)], w, h, n)
        # Players
        self.players = [ p1, p2 ]
        p1.player = 1
        p2.player = 2

    # Execute the game.
    #
    # RETURN [int]: The game outcome.
    #               1 for Player 1, 2 for Player 2, and 0 for no winner
    def go(self):
        # Current player
        p = 0
        while self.board.free_cols() and self.board.get_outcome() == 0:
            self.board.print_it()
            # Copy board so player can't modify it
            x = self.players[p].go(self.board.copy())
            print(self.players[p].name, "move:", x)
            if not x in self.board.free_cols():
                print("Illegal move")
                outcome = 1
                if p == 0:
                    outcome = 2
                print(self.players[outcome-1].name, "won!")
                return outcome
            # Legal move, add token there
            self.board.add_token(x)
            # Switch player
            if p == 0:
                p = 1
            else:
                p = 0
        # Print game outcome
        self.board.print_it()
        outcome = self.board.get_outcome()
        print("Game over!")
        if outcome == 0:
            print("It's a tie!")
        else:
            print(self.players[outcome-1].name, "won!")
        return outcome

    # Execute a timed game.
    #
    # In a timed game, if a player takes more than 'limit' seconds to make a
    # move, it loses.
    #
    # PARAM  [int] limit: the time limit in seconds
    # RETURN [int]: The game outcome.
    #               1 for Player 1, 2 for Player 2, and 0 for no winner
    def timed_go(self, limit):
        # Current player
        p = 0
        self.board.print_it()
        while self.board.free_cols() and self.board.get_outcome() == 0:
            # Get start time
            st = time.time()
            # Make move and copy board so player can't modify it
            x = self.players[p].go(self.board.copy())
            # Get elapsed time
            et = time.time() - st
            # Is the move legal and within the time limit?
            if (not x in self.board.free_cols()) or (et > limit):
                outcome = 1
                if p == 0:
                    outcome = 2
                print(self.players[outcome - 1].name, "won!")
                return outcome
            # Legal move, add token there
            self.board.add_token(x)
            self.board.print_it()
            print(self.players[p].name, "move:", x)
            # Switch player
            if p == 0:
                p = 1
            else:
                p = 0
        # Print game outcome
        self.board.print_it()
        outcome = self.board.get_outcome()
        print("Game over!")
        if outcome == 0:
            print("It's a tie!")
        else:
            print(self.players[outcome - 1].name, "won!")
        return self.board.get_outcome()

    # Execute a timed game.
    #
    # In a timed game, if a player takes more than 'limit' seconds to make a
    # move, it loses.
    #
    # PARAM  [int] log_file: the path of the log file
    # PARAM  [int] limit: the time limit in seconds
    # RETURN [int]: The game outcome.
    #               1 for Player 1, 2 for Player 2, and 0 for no winner
    def logged_go(self, log_file, limit):
        with Path(log_file).open("w") as log:
            log.write("{} player1\n".format(self.players[0].name))
            log.write("{} player2\n".format(self.players[1].name))
            # Current player
            p = 0
            while self.board.free_cols() and self.board.get_outcome() == 0:
                # Get start time
                st = time.time()
                # Make move and copy board so player can't modify it
                x = self.players[p].go(self.board.copy())
                # Get elapsed time
                et = time.time() - st
                # Is the move legal and within the time limit?
                if (not x in self.board.free_cols()) or (et > limit):
                    # Illegal/out of time, nothing to log, end of game
                    outcome = 1
                    if p == 0:
                        outcome = 2
                    return outcome
                # Legal move, add token there
                self.board.add_token(x)
                # Log move
                log.write("{} {}\n".format(self.players[p].name, x))
                # Switch player
                if p == 0:
                    p = 1
                else:
                    p = 0
            # Game ended successfully, log the outcome
            if self.board.get_outcome() == 0:
                log.write("- tie\n".format(self.players[0].name))
            else:
                log.write("{} wins\n".format(self.players[self.board.get_outcome()-1].name))
        # Return game outcome
        return self.board.get_outcome()
