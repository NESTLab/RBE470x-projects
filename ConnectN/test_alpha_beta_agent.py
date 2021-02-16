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
        control_board = board.Board(
            [[0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]],
            4,
            4,
            n_to_win)
        control_result = agent.win_bonus(control_board)
        control_expect = 200
        self.assertEqual(control_result, control_expect)
        
        n_to_win = 4
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        control_board = board.Board(
            [[0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]],
            4,
            4,
            n_to_win)
        control_result = agent.win_bonus(control_board)
        control_expect = 0
        self.assertEqual(control_result, control_expect)

        # opponent is negative
        n_to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        control_board = board.Board(
            [[0, 0, 0, 0],
            [2, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 2, 0]],
            4,
            4,
            n_to_win)
        control_result = agent.win_bonus(control_board)
        control_expect = -200
        self.assertEqual(control_result, control_expect)

        # bound to who wins not HOW they win
        n_to_win = 3
        agent = aba.AlphaBetaAgent("TEST_AI", 1, n_to_win)
        agent.player = 1
        control_board = board.Board(
            [[0, 0, 0, 2],
            [2, 2, 2, 2],
            [1, 2, 1, 1],
            [2, 1, 2, 2]],
            4,
            4,
            n_to_win)
        control_result = agent.win_bonus(control_board)
        control_expect = -200
        self.assertEqual(control_result, control_expect)


    # find which player the AI is by counting pieces on the board
    def test_find_player(self):
        self.assertEqual(True, True)
    
    # score a board by counting number of tokens in a row
    # UNFINISHED
    def test_num_in_a_row(self):
        self.assertEqual(True, True)
    
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
        self.assertEqual([3, 2, 1, 7], small_list)
        # add last point
        small_list = [3, 2, 1, 7]
        agent.add_to_points_list(small_list, 4)
        self.assertEqual([3, 2, 1, 8], small_list)

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


        

if __name__ == '__main__':
    unittest.main()