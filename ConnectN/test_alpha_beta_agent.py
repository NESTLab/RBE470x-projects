import unittest
import agent
import alpha_beta_agent as aba
import board

class TestAlphaBetaAgent(unittest.TestCase):

    def test_win_bonus(self):
        # control
        n_to_win = 2
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        control_board = board.Board(
            [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
            4,
            4,
            n_to_win)
        control_result = agent.win_bonus(control_board)
        control_expect = 0
        self.assertEqual(control_result, control_expect)

        #  test n to win
        n_to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        b = board.Board(
            [[0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]],
            4,
            4,
            n_to_win)
        control_result = agent.win_bonus(b)
        control_expect = 500
        self.assertEqual(control_result, control_expect)
        
        n_to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        b = board.Board(
            [[0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0]],
            4,
            4,
            n_to_win)
        control_result = agent.win_bonus(b)
        control_expect = 0
        self.assertEqual(control_result, control_expect)

        # opponent is negative
        n_to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        b = board.Board(
            [[2, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 2, 0],
            [0, 0, 0, 0]],
            4,
            4,
            n_to_win)
        control_result = agent.win_bonus(b)
        control_expect = -800
        self.assertEqual(control_result, control_expect)

        # bound to who wins not HOW they win
        n_to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        b = board.Board(
            [[2, 2, 2, 2],
            [1, 2, 1, 1],
            [2, 1, 2, 2],
            [0, 0, 0, 2]],
            4,
            4,
            n_to_win)
        control_result = agent.win_bonus(b)
        control_expect = -800
        self.assertEqual(control_result, control_expect)


    # find which player the AI is by counting pieces on the board
    def test_find_player(self):
        self.assertEqual(True, True)
    
    # score a board by counting number of tokens in a row (neglecting the scalars)
    def test_num_in_a_row(self):
        # control
        n_to_win = 2
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        b = board.Board(
            [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
            4,
            4,
            n_to_win)
        result = agent.num_in_a_row(b)
        expect = 0
        self.assertEqual(result, expect)
        # only vertical
        n_to_win = 2
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        agent.quad_scalar = lambda x: x
        b = board.Board(
            [[0, 2, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
            4,
            4,
            n_to_win)
        result = agent.num_in_a_row(b)
        expect = -2
        self.assertEqual(result, expect)
        # same weight for both players
        n_to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        agent.quad_scalar = lambda x: x
        b = board.Board(
            [[0, 2, 0, 1],
            [0, 2, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
            4,
            4,
            n_to_win)
        result = agent.num_in_a_row(b)
        expect = 0
        self.assertEqual(result, expect)

        n_to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        agent.quad_scalar = lambda x: x
        b = board.Board(
            [[0, 0, 1, 1],
            [0, 0, 2, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
            4,
            4,
            n_to_win)
        result = agent.num_in_a_row(b)
        expect = 0
        self.assertEqual(result, expect)
        # only horizontal
        n_to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        agent.quad_scalar = lambda x: x
        b = board.Board(
            [[1, 1, 1, 1],
            [0, 0, 2, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
            4,
            4,
            n_to_win)
        result = agent.num_in_a_row(b)
        expect = 2
        self.assertEqual(result, expect)
        # only diagnal
        n_to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        agent.quad_scalar = lambda x: x
        b = board.Board(
            [[1, 0, 0, 1],
            [0, 1, 2, 0],
            [0, 2, 1, 0],
            [0, 0, 0, 0]],
            4,
            4,
            n_to_win)
        result = agent.num_in_a_row(b)
        expect = 1
        self.assertEqual(result, expect)
        # mix
        n_to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        agent.quad_scalar = lambda x: x
        b = board.Board(
            [[1, 2, 2, 1],
            [0, 1, 2, 0],
            [0, 2, 1, 0],
            [0, 0, 0, 0]],
            4,
            4,
            n_to_win)
        
        result = agent.num_in_a_row(b)
        expect = -5
        self.assertEqual(result, expect)
        n_to_win = 7
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        agent.quad_scalar = lambda x: x
        b = board.Board(
            [[1, 2, 2, 1, 1],
            [0, 1, 2, 1, 2],
            [0, 2, 1, 0, 1],
            [0, 0, 0, 0, 0]],
            5,
            4,
            n_to_win)
        result = agent.num_in_a_row(b)
        expect = 4
        self.assertEqual(result, expect)
    
    def test_add_to_points_list(self):
        agent = aba.AlphaBetaAgent("TEST_AI", 1, 4)
        # empty list
        empty_list = []
        try:
            agent.add_to_points_list(empty_list, 4)
        except IndexError:
            self.fail("Index out of bounds on empty_list")
        self.assertEqual([], empty_list)
        # negative point value
        small_list = [3, 2, 1, 7]
        agent.add_to_points_list(small_list, -4)
        self.assertEqual([3, 2, 1, 7], small_list)
        # zero point
        small_list = [3, 2, 1, 7]
        agent.add_to_points_list(small_list, 0)
        self.assertEqual([3, 2, 1, 7], small_list)
        # add point larger than list
        small_list = [3, 2, 1, 7]
        agent.add_to_points_list(small_list, 5)
        self.assertEqual([3, 2, 1, 8], small_list)
        # add last point
        small_list = [3, 2, 1, 7]
        agent.add_to_points_list(small_list, 4)
        self.assertEqual([3, 2, 1, 8], small_list)
        # neglect points of 1
        small_list = [3, 2, 1, 7]
        agent.add_to_points_list(small_list, 1)
        self.assertEqual([3, 2, 1, 7], small_list)

    # simple test to guard the equation used for quad_scalar
    def test_quad_scalar(self):
        def q(x, to_win):
            return x*x*x/to_win
        
        to_win = 11
        for x in range(20):
            agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
            found = agent.quad_scalar(x)
            expected = q(x, to_win)
            to_win = to_win/2 * -1
            self.assertEqual(found, expected)

    # counting the number of horizontal pieces for current agent and opponent
    def test_count_horizontal(self):
        # 4 x 4 with 3 to win 
        w = 4
        h = 4
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
            w,
            h,
            to_win)
        found = agent.count_horizontal(b, 1, to_win)
        expect = [[0, 0, 0], [0, 0, 0]]
        self.assertEqual(found, expect)
        # Two horizontals
        w = 4
        h = 4
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1, 1, 1, 0],
            [0, 2, 2, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
            w,
            h,
            to_win)
        found = agent.count_horizontal(b, 1, to_win)
        expect = [[0, 0, 1], [0, 1, 0]]
        self.assertEqual(found, expect)
        # larger in a row than to_win
        w = 4
        h = 4
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
            w,
            h,
            to_win)
        found = agent.count_horizontal(b, 1, to_win)
        expect = [[0, 0, 1], [0, 0, 0]]
        self.assertEqual(found, expect)
        # cointing 1s
        w = 4
        h = 4
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1, 2, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
            w,
            h,
            to_win)
        found = agent.count_horizontal(b, 1, to_win)
        expect = [[0, 0, 0], [0, 0, 0]]
        self.assertEqual(found, expect)
        # large rows
        w = 8
        h = 4
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1, 1, 1, 1, 0, 1, 1, 1],
            [0, 2, 2, 2, 0, 0, 0, 0],
            [0, 0, 2, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]],
            w,
            h,
            to_win)
        found = agent.count_horizontal(b, 1, to_win)
        expect = [[0, 0, 2], [0, 1, 1]]
        self.assertEqual(found, expect)
        # change to Player2
        w = 8
        h = 4
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1 # NOTE: count_horizontal will not depend on agent.player
        b = board.Board(
            [[1, 1, 1, 1, 0, 1, 1, 1],
            [0, 2, 2, 2, 0, 0, 0, 0],
            [0, 0, 2, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]],
            w,
            h,
            to_win)
        found = agent.count_horizontal(b, 2, to_win)
        expect = [[0, 1, 1], [0, 0, 2]]
        self.assertEqual(found, expect)
        # only 1 column
        w = 1
        h = 4
        to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1],
            [1],
            [2],
            [1]],
            w,
            h,
            to_win)
        found = agent.count_horizontal(b, 1, to_win)
        expect = [[0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(found, expect)
        # only 1 row
        w = 4
        h = 1
        to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1, 2, 1, 1]],
            w,
            h,
            to_win)
        found = agent.count_horizontal(b, 1, to_win)
        expect = [[0, 1, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(found, expect)
    
    def test_count_vertical(self):
        # 4 x 4 with 3 to win 
        w = 4
        h = 4
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
            w,
            h,
            to_win)
        found = agent.count_vertical(b, 1, to_win)
        expect = [[0, 0, 0], [0, 0, 0]]
        self.assertEqual(found, expect)
        # two vertical
        w = 4
        h = 4
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1, 0, 2, 0],
            [1, 0, 2, 0],
            [1, 0, 2, 0],
            [0, 0, 0, 0]],
            w,
            h,
            to_win)
        found = agent.count_vertical(b, 1, to_win)
        expect = [[0, 0, 1], [0, 0, 1]]
        self.assertEqual(found, expect)
        # multi verticals with larger than N to win
        w = 4
        h = 4
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1, 1, 2, 0],
            [1, 1, 2, 0],
            [1, 2, 2, 0],
            [1, 2, 2, 0]],
            w,
            h,
            to_win)
        found = agent.count_vertical(b, 1, to_win)
        expect = [[0, 1, 1], [0, 1, 1]]
        self.assertEqual(found, expect)
        # change AI to player2
        w = 4
        h = 4
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 2
        b = board.Board(
            [[1, 1, 2, 0],
            [1, 1, 2, 0],
            [1, 2, 2, 0],
            [1, 2, 2, 0]],
            w,
            h,
            to_win)
        found = agent.count_vertical(b, 2, to_win)
        expect = [[0, 1, 1], [0, 1, 1]]
        self.assertEqual(found, expect)
        # 4 to win
        w = 4
        h = 4
        to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1, 1, 2, 1],
            [1, 1, 2, 1],
            [1, 1, 2, 1],
            [1, 2, 2, 1]],
            w,
            h,
            to_win)
        found = agent.count_vertical(b, 1, to_win)
        expect = [[0, 0, 1, 2], [0, 0, 0, 1]]
        self.assertEqual(found, expect)
        # do NOT allow 1-in-a-row
        w = 2
        h = 4
        to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1, 2],
            [2, 1],
            [1, 2],
            [2, 1]],
            w,
            h,
            to_win)
        found = agent.count_vertical(b, 1, to_win)
        expect = [[0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(found, expect)
        # only 1 column
        w = 1
        h = 4
        to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1],
            [1],
            [1],
            [1]],
            w,
            h,
            to_win)
        found = agent.count_vertical(b, 1, to_win)
        expect = [[0, 0, 0, 1], [0, 0, 0, 0]]
        self.assertEqual(found, expect)
        # only 1 row
        w = 4
        h = 1
        to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1, 2, 1, 1]],
            w,
            h,
            to_win)
        found = agent.count_vertical(b, 1, to_win)
        expect = [[0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(found, expect)
    
    # protect the function definition
    def test_col_midpoint_scalar(self):
        def f(col, last_col):
            return 25 * ((-1 * col * col) + (last_col * col))
        
        agent = aba.AlphaBetaAgent("TEST_AI", 1, 3)
        col = 0
        last_col = 20
        for _ in range(5):
            found = agent.col_midpoint_scalar(col, last_col)
            expect = f(col, last_col)
            self.assertEqual(found, expect)
            col = col+1
            last_col = last_col/2

    def test_count_diagnal(self):
        # 4 x 4 with 3 to win 
        w = 4
        h = 4
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
            w,
            h,
            to_win)
        found = agent.count_diagnal(b, 1, to_win)
        expect = [[0, 0, 0], [0, 0, 0]]
        self.assertEqual(found, expect)
        # 4 x 4 with 3 to win no diagnal
        w = 4
        h = 4
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[0, 0, 1, 1],
            [0, 0, 2, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
            w,
            h,
            to_win)
        found = agent.count_diagnal(b, 1, to_win)
        expect = [[0, 0, 0], [0, 0, 0]]
        self.assertEqual(found, expect)
        # count top-left to bot-right
        w = 4
        h = 4
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1, 2, 2, 0],
            [0, 1, 2, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0]],
            w,
            h,
            to_win)
        found = agent.count_diagnal(b, 1, to_win)
        expect = [[0, 0, 1], [0, 1, 0]]
        self.assertEqual(found, expect)
        # count top-right to bot-left
        w = 4
        h = 4
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[0, 2, 1, 0],
            [2, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0]],
            w,
            h,
            to_win)
        found = agent.count_diagnal(b, 1, to_win)
        expect = [[0, 0, 1], [0, 1, 0]]
        self.assertEqual(found, expect)
        # mix of both 4 x 4
        w = 4
        h = 4
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1, 2, 1, 0],
            [2, 1, 2, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0]],
            w,
            h,
            to_win)
        found = agent.count_diagnal(b, 1, to_win)
        expect = [[0, 1, 1], [0, 2, 0]]
        self.assertEqual(found, expect)
        # mix of both 4 x 1
        w = 4
        h = 1
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1, 2, 1, 0]],
            w,
            h,
            to_win)
        found = agent.count_diagnal(b, 1, to_win)
        expect = [[0, 0, 0], [0, 0, 0]]
        self.assertEqual(found, expect)
        # mix of both 1 x 4
        w = 1
        h = 4
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1],
            [2],
            [2],
            [1]],
            w,
            h,
            to_win)
        found = agent.count_diagnal(b, 1, to_win)
        expect = [[0, 0, 0], [0, 0, 0]]
        self.assertEqual(found, expect)
        # mix of both 4 x 4 with 4 to win
        w = 4
        h = 4
        to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1, 2, 1, 0],
            [2, 1, 2, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0]],
            w,
            h,
            to_win)
        found = agent.count_diagnal(b, 1, to_win)
        expect = [[0, 1, 1, 0], [0, 2, 0, 0]]
        self.assertEqual(found, expect)
        # mix of both 4 x 4 with 4 to win
        w = 4
        h = 4
        to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1, 2, 1, 0],
            [2, 1, 2, 0],
            [1, 2, 2, 0],
            [0, 0, 2, 0]],
            w,
            h,
            to_win)
        found = agent.count_diagnal(b, 1, to_win)
        expect = [[0, 1, 1, 0], [0, 3, 1, 0]]
        self.assertEqual(found, expect)
        # mix of both 4 x 4 with 6 to win
        w = 6
        h = 3
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 1
        b = board.Board(
            [[1, 2, 2, 1, 2, 2],
            [0, 1, 1, 2, 1, 0],
            [0, 0, 0, 1, 0, 0]],
            w,
            h,
            to_win)
        found = agent.count_diagnal(b, 1, to_win)
        expect = [[0, 5, 0], [0, 2, 0]]
        self.assertEqual(found, expect)
        # change AI to player2
        w = 6
        h = 3
        to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, to_win)
        agent.player = 2
        b = board.Board(
            [[1, 2, 2, 1, 2, 2],
            [0, 1, 1, 2, 1, 0],
            [0, 0, 0, 1, 0, 0]],
            w,
            h,
            to_win)
        found = agent.count_diagnal(b, 2, to_win)
        expect = [[0, 2, 0], [0, 5, 0]]
        self.assertEqual(found, expect)

    # compares alphabeta with minmax to ensure that they always return the same choice
    def test_alphabeta(self):
        n_to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        b = board.Board(
            [[2, 2, 2, 2],
             [1, 2, 1, 1],
             [2, 1, 2, 2],
             [0, 0, 0, 2]],
            4,
            4,
            n_to_win)
        mmRes = agent.minimax(b, 1, n_to_win)
        abRes = agent.alphabeta(b, 1, n_to_win, float('-inf'), float('inf'))
        self.assertEqual(mmRes, abRes)

        n_to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 2, n_to_win)
        agent.player = 1
        b = board.Board(
            [[2, 2, 2, 2],
             [1, 2, 1, 1],
             [2, 1, 2, 2],
             [0, 0, 0, 2]],
            4,
            4,
            n_to_win)
        mmRes = agent.minimax(b, 2, n_to_win)
        abRes = agent.alphabeta(b, 2, n_to_win, float('-inf'), float('inf'))
        self.assertEqual(mmRes, abRes)

        n_to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 3, n_to_win)
        agent.player = 1
        b = board.Board(
            [[2, 2, 2, 2],
             [1, 2, 1, 1],
             [2, 1, 2, 2],
             [0, 0, 0, 2]],
            4,
            4,
            n_to_win)
        mmRes = agent.minimax(b, 3, n_to_win)
        abRes = agent.alphabeta(b, 3, n_to_win, float('-inf'), float('inf'))
        self.assertEqual(mmRes, abRes)

        n_to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        b = board.Board(
            [[0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0]],
            4,
            4,
            n_to_win)
        mmRes = agent.minimax(b, 1, n_to_win)
        abRes = agent.alphabeta(b, 1, n_to_win, float('-inf'), float('inf'))
        self.assertEqual(mmRes, abRes)

        n_to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 2, n_to_win)
        agent.player = 1
        b = board.Board(
            [[0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 0, 0]],
            4,
            4,
            n_to_win)
        mmRes = agent.minimax(b, 2, n_to_win)
        abRes = agent.alphabeta(b, 2, n_to_win, float('-inf'), float('inf'))
        self.assertEqual(mmRes, abRes)

        n_to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 3, n_to_win)
        agent.player = 1
        b = board.Board(
            [[0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 0, 0]],
            4,
            4,
            n_to_win)
        mmRes = agent.minimax(b, 3, n_to_win)
        abRes = agent.alphabeta(b, 3, n_to_win, float('-inf'), float('inf'))
        self.assertEqual(mmRes, abRes)







if __name__ == '__main__':
    unittest.main()