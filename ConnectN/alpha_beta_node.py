class AlphaBetaNode(object):
    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, board, col, evaluation):
        # Board used in node
        self.board = board
        # column where last token was added
        self.col = col
        # evaluation value given by the alphaBetaAgent evaluation function
        self.evaluation = evaluation
        # empty array of children
        self.children = []
