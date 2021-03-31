import unittest
from config import *
from Nim import *

class NimTest(unittest.TestCase):

	def compare_Nim_objects(self, game1, game2):
		print(game1.board == game2.board)
		if game1.player_just_moved == game2.player_just_moved and game1.bubbles == game2.bubbles and list(game1.board) == list(game2.board):
			return True
		print(f'Original and cloned Nim Games are not the same.')
		return False

	def test_clone(self):
		game1 = Nim()
		game1.bubbles = 20
		game1.board = np.ones((game1.bubbles), dtype=int)
		game2 = Nim()
		game2.bubbles = 20
		game2.board = np.ones((game2.bubbles), dtype=int)
		self.assertEqual(self.compare_Nim_objects(game1.clone(), game2), True)

	def test_do_move_moves_exist(self):
		game1 = Nim()
		game1.do_move(3)
		self.assertEqual(game1.bubbles, 18)
		self.assertEqual(game1.player_just_moved, 1)

	def test_do_move_no_moves_left(self):
		game1 = Nim()
		game1.bubbles = 0
		game1.do_move(1)
		self.assertEqual(game1.bubbles, 0)
		self.assertEqual(game1.player_just_moved, 2)

	def test_get_moves_moves_exist(self):
		game = Nim()
		game.bubbles = 5
		self.assertCountEqual(game.get_moves(), [1, 2, 3])

	def test_get_moves_no_moves_left(self):
		game = Nim()
		game.bubbles = 0
		self.assertCountEqual(game.get_moves(), [])

	def test_get_moves_returns_one_move(self):
		game = Nim()
		game.bubbles = 1
		self.assertCountEqual(game.get_moves(), [1])

	def test_get_moves_returns_two_moves(self):
		game = Nim()
		game.bubbles = 2
		self.assertCountEqual(game.get_moves(), [1, 2])

	def test_is_game_over_returns_true(self):
		game = Nim()
		game.bubbles = 0
		self.assertEqual(game.is_game_over(), True)

	def test_is_game_over_returns_true(self):
		game = Nim()
		game.bubbles = 1
		self.assertEqual(game.is_game_over(), False)

	def test_get_result_returns_1(self):
		game = Nim()
		game.bubbles = 0
		self.assertEqual(game.get_result(player_just_moved = 2), 1.0)

	def test_get_cell_clicked_returns_3_bva1(self):
		game = Nim()
		self.assertEqual(game.get_cell_clicked(310, 100), 3)

	def test_get_cell_clicked_returns_5_bva2(self):
		game = Nim()
		self.assertEqual(game.get_cell_clicked(260, 674), 20)

	def test_get_cell_clicked_returns_5_bva3(self):
		game = Nim()
		self.assertEqual(game.get_cell_clicked(340, 675), None)

	def test_quit_game_btn_clicked_returns_true_bva4(self):
		game = Nim()
		self.assertEqual(game.quit_game_btn_clicked(550, 10), True)

	if __name__ == '__main__':
		unittest.main()