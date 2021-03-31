import unittest
from config import *
from OXO import *

class TestOXOMethods(unittest.TestCase):

	def test_get_moves_no_moves_left(self):
		game = OXO()
		game.board = [2,1,2,1,2,1,2,1,1]
		self.assertCountEqual(game.get_moves(), [])

	def test_get_moves(self):
		game = OXO()
		game.board = [0,0,0,1,0,2,1,0,0]
		self.assertCountEqual(game.get_moves(), [0,1,2,4,7,8])

	def test_is_game_over_returns_False(self):
		game = OXO()
		game.board = [0,0,0,1,0,2,1,0,0]
		self.assertEqual(game.is_game_over(), False)

	def test_is_game_over_returns_True(self):
		game = OXO()
		game.board = [1,2,0,1,0,2,1,0,0]
		self.assertEqual(game.is_game_over(), True)

	def compare_OXO_objects(self, oxo1, oxo2):
		if oxo1.player_just_moved == oxo2.player_just_moved and oxo1.board == oxo2.board:
			return True
		print(f'Original and cloned OXO Games are not the same.')
		return False

	def test_clone(self):
		game1 = OXO()
		game1.board = [2,1,0,0,1,0,0,0,1]
		game2 = OXO()
		game2.board = [2,1,0,0,1,0,0,0,1]
		self.assertEqual(self.compare_OXO_objects(game1.clone(), game2), True)

	def test_do_move(self):
		game = OXO()
		game.do_move(4)
		self.assertCountEqual(game.board, [0,0,0,0,1,0,0,0,0])

	def test_horizontal_win_line1(self):
		game = OXO()
		game.board = [1,1,1,0,0,0,0,0,0]
		self.assertEqual(game._get_win_line(), OXOWinLine.HORIZONTAL1)

	def test_horizontal_win_line2(self):
		game = OXO()
		game.board = [0,0,0,2,2,2,0,0,0]
		self.assertEqual(game._get_win_line(), OXOWinLine.HORIZONTAL2)

	def test_horizontal_win_line3(self):
		game = OXO()
		game.board = [1,2,1,2,1,2,2,2,2]
		self.assertEqual(game._get_win_line(), OXOWinLine.HORIZONTAL3)

	def test_vertical_win_line1(self):
		game = OXO()
		game.board = [1,2,0,1,0,2,1,0,0]
		self.assertEqual(game._get_win_line(), OXOWinLine.VERTICAL1)

	def test_vertical_win_line2(self):
		game = OXO()
		game.board = [1,2,1,0,2,2,0,2,1]
		self.assertEqual(game._get_win_line(), OXOWinLine.VERTICAL2)

	def test_vertical_win_line3(self):
		game = OXO()
		game.board = [1,2,1,2,1,1,2,2,1]
		self.assertEqual(game._get_win_line(), OXOWinLine.VERTICAL3)

	def test_diagonal_win_line1(self):
		game = OXO()
		game.board = [1,2,0,0,1,2,0,0,1]
		self.assertEqual(game._get_win_line(), OXOWinLine.DIAGONAL1)

	def test_diagonal_win_line2(self):
		game = OXO()
		game.board = [0,1,2,0,2,1,2,0,1]
		self.assertEqual(game._get_win_line(), OXOWinLine.DIAGONAL2)

	def test_get_result_playerjm_won(self):
		game = OXO()
		game.board = [1,1,1,0,0,0,0,0,0]
		self.assertEqual(game.get_result(1), 1.0)

	def test_get_result_playerjm_lost(self):
		game = OXO()
		game.board = [0,0,0,2,2,2,0,0,0]
		self.assertEqual(game.get_result(1), 0.0)

	def test_do_move_bva1(self):
		game = OXO()
		game.do_move(8)
		self.assertCountEqual(game.board, [0,0,0,0,0,0,0,0,1])

	def test_do_move_bva2(self):
		game = OXO()
		game.do_move(0)
		self.assertCountEqual(game.board, [1,0,0,0,0,0,0,0,0])

	def test_do_move_out_of_board_range(self):
		game = OXO()
		game.do_move(10)
		self.assertCountEqual(game.board, [0,0,0,0,0,0,0,0,0])

	if __name__ == '__main__':
		unittest.main()