import random
import game
import agent
import alpha_beta_agent as aba

# Set random seed for reproducibility
# random.seed(1)

games = []
# for i in range(10):
#     width = random.randint(5, 10)
#     height = random.randint(5, 10)
#     token = random.randint(4, 5)
#     randomPlayer = random.randint(1, 2)
#     if randomPlayer == 1:
#         games.append(game.Game(width, height, token, agent.RandomAgent("random"), aba.AlphaBetaAgent("alphabeta", 5)))
#     else:
#         games.append(game.Game(width, height, token, aba.AlphaBetaAgent("alphabeta", 5), agent.RandomAgent("random")))

games.append(game.Game(7, 6, 4, aba.AlphaBetaAgent("alphabeta", 4), agent.RandomAgent("random")))
games.append(game.Game(7, 6, 5, aba.AlphaBetaAgent("alphabeta", 4), agent.RandomAgent("random")))
games.append(game.Game(10, 8, 4, aba.AlphaBetaAgent("alphabeta", 4), agent.RandomAgent("random")))
games.append(game.Game(10, 8, 5, aba.AlphaBetaAgent("alphabeta", 4), agent.RandomAgent("random")))
# Execute the game
wins = 0
ties = 0
for game in games:
    player = 0
    if game.players[0].name == "alphabeta":
        player = 1
    else:
        player = 2
    outcome = game.go()
    if outcome == player:
        wins += 1
    elif outcome == 0:
        ties += 1
print("We won " + str(wins) + " out of " + str(len(games)) + " games")
print("We tied " + str(ties) + " times")
