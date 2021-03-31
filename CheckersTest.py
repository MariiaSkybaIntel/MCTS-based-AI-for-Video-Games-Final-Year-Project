import unittest
from config import *
from Checkers import *
from UCT import UCT


class CheckersMethodsTest(unittest.TestCase):

	def test_get_moves_north_in_start_state(self):
		game = Checkers()
		expected_moves = [[(5, 0), (4, 1)], [(5, 2), (4, 1)], [(5, 2), (4, 3)], [(5, 4), (4, 3)], [(5, 4), (4, 5)], [(5, 6), (4, 5)], [(5, 6), (4, 7)]]		
		self.assertCountEqual(game.get_moves(), expected_moves)

	def test_get_moves_south_in_start_state(self):
		game = Checkers()
		game.player_just_moved = 1
		expected_moves = [[(2, 1), (3, 0)], [(2, 1), (3, 2)], [(2, 3), (3, 2)], [(2, 3), (3, 4)], [(2, 5), (3, 4)], [(2, 5), (3, 6)], [(2, 7), (3, 6)]]
		self.assertCountEqual(game.get_moves(), expected_moves)

	def test_get_moves_south_with_one_king(self):
		game = Checkers()
		game.player_just_moved = 1
		game.board[1][0] = 0
		game.board[0][1] = 0
		game.board[1][2] = 0
		game.board[1][0] = 0
		game.board[0][3] = 0
		game.board[2][3] = 0
		game.board[2][1] = 20
		expected_moves = [[(2, 1), (1, 0)], [(2, 1), (1, 2)], [(2, 1), (3, 0)], [(2, 1), (3, 2)], [(1, 4), (2, 3)], [(2, 5), (3, 4)], [(2, 5), (3, 6)], [(2, 7), (3, 6)]]
		self.assertCountEqual(game.get_moves(), expected_moves)

	def test_get_moves_north_with_one_king(self):
		game = Checkers()
		game.board = [[0] * CHECKERS_BOARD_SIZE for x in range(CHECKERS_BOARD_SIZE)]
		game.board[5][4] = 10
		expected_moves = [[(5, 4), (4, 3)], [(5, 4), (4, 5)], [(5, 4), (6, 3)], [(5, 4), (6, 5)]]
		self.assertCountEqual(game.get_moves(), expected_moves)

	def test_get_moves_north_with_one_king_and_capturing_move(self):
		game = Checkers()
		game.board[5][2] = 0
		game.board[5][6] = 0
		game.board[6][3] = 0
		game.board[6][5] = 0		
		game.board[7][2] = 0
		game.board[7][4] = 0
		game.board[7][6] = 0		
		game.board[4][5] = 2
		game.board[5][4] = 10
		expected_moves = [[(5, 4), (3, 6)]]
		self.assertCountEqual(game.get_moves(), expected_moves)

	def test_one_subsequent_move(self):
		game = Checkers()
		game.board = [[0] * CHECKERS_BOARD_SIZE for x in range(CHECKERS_BOARD_SIZE)]
		game.board[5][4] = 1
		game.board[4][5] = 2
		game.board[2][5] = 2
		expected_board_state = [[0] * CHECKERS_BOARD_SIZE for x in range(CHECKERS_BOARD_SIZE)]
		expected_board_state[1][4] = 1
		game.do_move([(5, 4), (3, 6)])
		self.assertEqual(game.board, expected_board_state)

	if __name__ == '__main__':
		unittest.main()