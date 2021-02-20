class AlphaBetaNode(object):
    # Class constructor.
    #
    # PARAM [board.Board] brd: the board state
    # PARAM [int]         col: column where last token was added
    # PARAM [int]         evaluation: The evaluation score.
    def __init__(self, board, col, evaluation):
        # Board used in node
        self.board = board
        # column where last token was added
        self.col = col
        # evaluation value given by the alphaBetaAgent evaluation function
        self.evaluation = evaluation
