import random
import game
import agent
import alpha_beta_agent as aba

######################
# Play a single game #
######################

# Play a single game.
#
# PARAM [int]         w:  the board width
# PARAM [int]         h:  the board height
# PARAM [int]         n:  the number of tokens to line up to win
# PARAM [int]         l:  the time limit for a move in seconds
# PARAM [agent.Agent] p1: the agent for Player 1
# PARAM [agent.Agent] p2: the agent for Player 2
def play_game(w, h, n, l, p1, p2):
    g = game.Game(w,  # width
                  h,  # height
                  n,  # tokens in a row to win
                  p1, # player 1
                  p2) # player 2
    o = g.timed_go(l)
    print("    GAME:", p1.name, "vs.", p2.name, ": ", end='')
    if o == 0:
        print("tie")
    elif o == 1:
        print(p1.name, "won!")
    else:
        print(p2.name, "won!")
    return o

###########################################################
# Play a match between two players                        #
# Two games, with P1 and P2 inverted after the first game #
###########################################################

# Play a match.
#
# PARAM [int]         w:  the board width
# PARAM [int]         h:  the board height
# PARAM [int]         n:  the number of tokens to line up to win
# PARAM [int]         l:  the time limit for a move in seconds
# PARAM [agent.Agent] p1: the agent for Player 1
# PARAM [agent.Agent] p2: the agent for Player 2
def play_match(w, h, n, l, p1, p2):
    print("  MATCH:", p1.name, "vs.", p2.name)
    # Play the games
    o1 = play_game(w, h, n, l, p1, p2)
    o2 = play_game(w, h, n, l, p2, p1)
    # Calculate scores
    s1 = 0
    s2 = 0
    if o1 == 1:
        s1 = s1 + 1
        s2 = s2 - 1
    elif o1 == 2:
        s1 = s1 - 1
        s2 = s2 + 1
    if o2 == 1:
        s1 = s1 - 1
        s2 = s2 + 1
    elif o2 == 2:
        s1 = s1 + 1
        s2 = s2 - 1
    return (s1, s2)

####################################
# Play tournament and print scores #
####################################

# Play a tournament.
#
# PARAM [int]                 w:  the board width
# PARAM [int]                 h:  the board height
# PARAM [int]                 n:  the number of tokens to line up to win
# PARAM [int]                 l:  the time limit for a move in seconds
# PARAM [list of agent.Agent] ps: the agents in the tournament
def play_tournament(w, h, n, l, ps):
    print("TOURNAMENT START")
    # Initialize scores
    scores = {}
    for p in ps:
        scores[p] = 0
    # Play
    for i in range(0, len(ps)-1):
        for j in range(i + 1, len(ps)):
            (s1, s2) = play_match(w, h, n, l, ps[i], ps[j])
            scores[ps[i]] = scores[ps[i]] + s1
            scores[ps[j]] = scores[ps[j]] + s2
    print("TOURNAMENT END")
    # Calculate and print scores
    sscores = sorted( ((v,k.name) for k,v in scores.items()), reverse=True)
    print("\nSCORES:")
    for v,k in sscores:
        print(v,k)

#######################
# Run the tournament! #
#######################

# Set random seed for reproducibility
random.seed(1)

# Construct list of agents in the tournament
agents = [
    # aba.AlphaBetaAgent("aba", 4),
    agent.RandomAgent("random1"),
    agent.RandomAgent("random2"),
    agent.RandomAgent("random3"),
    agent.RandomAgent("random4")
]

# Run!
play_tournament(7,      # board width
                6,      # board height
                4,      # tokens in a row to win
                15,     # time limit in seconds
                agents) # player list
