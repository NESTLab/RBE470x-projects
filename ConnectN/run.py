import random
import game
import agent
import alpha_beta_agent as aba

# Set random seed for reproducibility
# random.seed(1)

games = []
games.append(game.Game(7, 6, 4, aba.AlphaBetaAgent("alphabeta"), agent.RandomAgent("random")))
games.append(game.Game(7, 6, 5, aba.AlphaBetaAgent("alphabeta"), agent.RandomAgent("random")))
games.append(game.Game(10, 8, 4, aba.AlphaBetaAgent("alphabeta"), agent.RandomAgent("random")))
games.append(game.Game(10, 8, 5, aba.AlphaBetaAgent("alphabeta"), agent.RandomAgent("random")))
for i in range(96):
    width = random.randint(7, 10)
    height = random.randint(6, 8)
    token = random.randint(4, 5)
    randomPlayer = random.randint(1, 2)
    if randomPlayer == 1:
        games.append(game.Game(width, height, token, agent.RandomAgent("random"), aba.AlphaBetaAgent("alphabeta")))
    else:
        games.append(game.Game(width, height, token, aba.AlphaBetaAgent("alphabeta"), agent.RandomAgent("random")))
# Execute the game
wins = 0
ties = 0
game_num = 0
for game in games:
    game_num += 1
    print("We are playing game " + str(game_num))
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
print("We won " + str(wins) + " out of " + str(game_num) + " games")
print("We tied " + str(ties) + " times")

