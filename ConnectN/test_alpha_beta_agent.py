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
        self.assertEqual(False, True)


if __name__ == '__main__':
    unittest.main()