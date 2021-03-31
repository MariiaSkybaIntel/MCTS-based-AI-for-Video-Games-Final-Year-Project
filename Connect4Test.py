import unittest
import numpy as np
from config import *
from Connect4 import *

class Connect4Test(unittest.TestCase):

	def compare_Connect4_objects(self, cf1, cf2):
		comparison = cf1.board == cf2.board
		boards_the_same = comparison.all()
		if cf1.player_just_moved == cf2.player_just_moved and boards_the_same:
			return True
		print(f'Original and cloned Connect4 Games are not the same.')
		return False

	def test_clone(self):
		game1 = Connect4()
		game1.board[0][0] = game1.board[0][1] = 1
		game1.board[0][2] = 2
		game2 = Connect4()
		game2.board[0][0] = game2.board[0][1]= 1
		game2.board[0][2] = 2
		self.assertEqual(self.compare_Connect4_objects(game1.clone(), game2), True)

	def test_do_move_column_fully_empty(self):
		game1 = Connect4()
		game2 = Connect4()
		game2.board[5][0] = 1
		game1.do_move(0)
		comparison = game1.board == game2.board
		boards_the_same = comparison.all()
		self.assertEqual(boards_the_same, True)

	def test_do_move_column_full(self):
		game1 = Connect4()
		game2 = Connect4()
		game2.board[0][6] = game1.board[0][6] = 1
		game1.do_move(6)
		comparison = game1.board == game2.board
		boards_the_same = comparison.all()
		self.assertEqual(boards_the_same, True)

	def test_get_moves_moves_exist(self):
		game = Connect4()
		game.board[0][6] = game.board[0][5] = game.board[0][4] = 1
		self.assertCountEqual(game.get_moves(), [0, 1, 2, 3])

	def test_get_moves_board_full(self):
		game = Connect4()
		game.board = np.ones((C4_ROWS, C4_COLS), dtype=int)
		self.assertCountEqual(game.get_moves(), [])

	def test_is_game_over_with_winning_line_returns_true(self):
		game = Connect4()
		game.board[4][2] = game.board[3][3] = game.board[2][4] = game.board[1][5] = 2
		self.assertEqual(game.is_game_over(), True)

	def test_is_game_over_with_full_board_returns_true(self):
		game = Connect4()
		game.board = np.ones((C4_ROWS, C4_COLS), dtype=int)
		self.assertEqual(game.is_game_over(), True)

	def test_is_game_over_returns_false(self):
		game = Connect4()
		game.board[0][2] = game.board[0][3] = game.board[2][4] = game.board[1][5] = 2
		self.assertEqual(game.is_game_over(), False)

	def test_get_result_returns_1(self):
		game = Connect4()
		game.board[4][2] = game.board[3][3] = game.board[2][4] = game.board[1][5] = 2
		self.assertEqual(game.get_result(player_just_moved = 2), 1.0)

	def test_get_result_returns_0(self):
		game = Connect4()
		game.board[4][2] = game.board[3][3] = game.board[2][4] = game.board[1][5] = 1
		self.assertEqual(game.get_result(player_just_moved = 2), 0.0)

	def test_get_cell_clicked_returns_1_bva1(self):
		game = Connect4()
		self.assertEqual(game.get_cell_clicked(191, 193), 1)

	def test_get_cell_clicked_returns_5_bva2(self):
		game = Connect4()
		self.assertEqual(game.get_cell_clicked(407, 251), 5)

	def test_get_cell_clicked_returns_5_bva3(self):
		game = Connect4()
		self.assertEqual(game.get_cell_clicked(407, 252), None)

	def test_quit_game_btn_clicked_returns_true_bva4(self):
		game = Connect4()
		self.assertEqual(game.quit_game_btn_clicked(550, 10), True)

	def test_quit_game_btn_clicked_returns_falsebva5(self):
		game = Connect4()
		self.assertEqual(game.quit_game_btn_clicked(550, 60), False)

	if __name__ == '__main__':
		unittest.main()