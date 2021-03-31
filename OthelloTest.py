import unittest
from config import *
from Othello import *
from unittest.mock import MagicMock

class OthelloTest(unittest.TestCase):

	def compare_Othello_objects(self, oth1, oth2):
		if oth1.player_just_moved == oth2.player_just_moved and oth1.board == oth2.board:
			return True
		print(f'Original and cloned Othello Games are not the same.')
		return False

	def test_clone(self):
		game1 = Othello()
		game1.board[0][0] = game1.board[0][1] = 1
		game1.board[0][2] = 2
		game2 = Othello()
		game2.board[0][0] = game2.board[0][1]= 1
		game2.board[0][2] = 2
		self.assertEqual(self.compare_Othello_objects(game1.clone(), game2), True)

	def test_do_move(self):
		game1 = Othello()
		game2 = Othello()
		game2.board[5][3] = game2.board[4][3] = game2.board[3][3] = 1
		game1.do_move((5, 3))
		self.assertCountEqual(game1.board, game2.board)

	def test_exists_sandwiched_bit_called_once_in_get_moves(self):
		game = Othello()
		game.method = MagicMock(return_value = True)

	def test_get_moves_moves_exist(self):
		game = Othello()
		self.assertCountEqual(game.get_moves(), [(2, 4), (3, 5), (4, 2), (5, 3)])

	def test_get_moves_board_full(self):
		game = Othello()
		game.board = [[2] * OTH_BOARD_SIZE for x in range(OTH_BOARD_SIZE)]
		self.assertCountEqual(game.get_moves(), [])

	def test_get_moves_no_sandwiched_bits_exist(self):
		game = Othello()
		game.board = [[2] * OTH_BOARD_SIZE for x in range(OTH_BOARD_SIZE)]
		game.board[0][0] = 0
		self.assertCountEqual(game.get_moves(), [])

	def test_is_on_board_returns_true(self):
		game = Othello()
		self.assertEqual(game._is_on_board(0, 7), True)

	def test_is_on_board_returns_false(self):
		game = Othello()
		self.assertEqual(game._is_on_board(-1, 1), False)

	def test_is_game_over_returns_true(self):
		game = Othello()
		game.board = [[2] * OTH_BOARD_SIZE for x in range(OTH_BOARD_SIZE)]
		self.assertEqual(game.is_game_over(), True)

	def test_is_game_over_returns_false(self):
		game = Othello()
		self.assertEqual(game.is_game_over(), False)

	def test_adjacent_to_enemy_returns_true(self):
		game = Othello()
		self.assertEqual(game._adjacent_to_enemy(2, 3), True)

	def test_adjacent_to_enemy_returns_false(self):
		game = Othello()
		self.assertEqual(game._adjacent_to_enemy(2, 2), False)

	def test_quit_game_btn_clicked_returns_true(self):
		game = Othello()
		self.assertEqual(game.quit_game_btn_clicked(550, 59), True)

	def test_quit_game_btn_clicked_returns_false(self):
		game = Othello()
		self.assertEqual(game.quit_game_btn_clicked(587, 50), False)

	if __name__ == '__main__':
		unittest.main()