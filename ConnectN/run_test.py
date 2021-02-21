import random
import game
import agent
import alpha_beta_agent as aba

# Set random seed for reproducibility
random.seed(1)

#
# Random vs. Random
#
# g = game.Game(7, # width
              # 6, # height
              # 4, # tokens in a row to win
              # agent.RandomAgent("random1"),       # player 1
              # agent.RandomAgent("random2"))       # player 2

#
# Human vs. Random
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               agent.RandomAgent("random"))        # player 2

#
#Random vs. AlphaBeta
wins = [0, 0]
n =100
for i in range(n):
    random.seed(i)
    g = game.Game(7, # width
              6, # height
              4, # tokens in a row to win
              agent.RandomAgent("random"),        # player 1
              aba.AlphaBetaAgent("alphabeta", 4)) # player 2
    outcome = g.go()
    wins[outcome-1] += 1
print("Player 1 won %d / %d times", wins[0], n)
print("Player 2 won %d / %d times", wins[1], n)
        
#
# Human vs. AlphaBeta
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               aba.AlphaBetaAgent("alphabeta", 4)) # player 2

#
# Human vs. Human
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human1"),   # player 1
#               agent.InteractiveAgent("human2"))   # player 2

# Execute the game