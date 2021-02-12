class AlphaBetaNode(object):
    # Class constructor.
    #
    # PARAM [board.Board] brd: the board state
    # PARAM [int]         col: column where last token was added
    # PARAM [int]         evaluation: The likely hood of either player winning.
    #
    # Note: Evaluation is from 0-1; 1 meaning AI will win and 0 meaning the other player will win
    def __init__(self, board, col, evaluation):
        # Board used in node
        self.board = board
        # column where last token was added
        self.col = col
        # evaluation value given by the alphaBetaAgent evaluation function
        self.evaluation = evaluation
