import time
import game
import agent
import alpha_beta_agent as aba

#
# Random vs. Random
#
g = game.Game(7, # width
              6, # height
              4, # tokens in a row to win
              agent.RandomAgent("random1"),       # player 1
              agent.RandomAgent("random2"),       # player 2
              time.time_ns()) # random seed

#
# Human vs. Random
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               agent.RandomAgent("random"),        # player 2
#               time.time_ns()) # random seed

#
# Random vs. AlphaBeta
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.RandomAgent("random"),        # player 1
#               aba.AlphaBetaAgent("alphabeta", 4), # player 2
#               1) # random seed

#
# Human vs. AlphaBeta
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               aba.AlphaBetaAgent("alphabeta", 4), # player 2
#               1) # random seed

# Execute the game
g.go()
