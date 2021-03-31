import pygame as pg
import time
from config import *
from Game import Game
from GameGUIInterface import GameGUIInterface
from UCT import UCT


class Othello(Game, GameGUIInterface):
	""" A state of the game of Othello, i.e. the game board.
		The board is a 2D array where 0 = empty, 1 = player 1, 2 = player 2.
		In Othello players alternately place pieces on a square board - each piece played
		has to sandwich opponent pieces between the piece played and pieces already on the
		board. Sandwiched pieces are flipped.
		This implementation modifies the rules to terminate the game as soon as the player
		about to move cannot make a move (whereas the standard game allows for a pass move).
	"""
	def __init__(self):
		self.player_just_moved = 2 # At the root pretend the player just moved is p2 - p1 has the first move
		self.board = [[0] * OTH_BOARD_SIZE for x in range(OTH_BOARD_SIZE)]
		# Populate 4 central cells in checkered manner: 0 = empty, 1 = player 1, 2 = player 2
		self.board[OTH_BOARD_SIZE//2][OTH_BOARD_SIZE//2] = self.board[OTH_BOARD_SIZE//2-1][OTH_BOARD_SIZE//2-1] = 1
		self.board[OTH_BOARD_SIZE//2][OTH_BOARD_SIZE//2-1] = self.board[OTH_BOARD_SIZE//2-1][OTH_BOARD_SIZE//2] = 2

	def clone(self):
		""" Create a deep clone of this game state.
		"""
		game = Othello()
		game.player_just_moved = self.player_just_moved
		game.board = [self.board[i][:] for i in range(OTH_BOARD_SIZE)]
		return game

	def do_move(self, move):
		""" Update a state by carrying out the given move.
			Must update playerJustMoved.
		"""
		(x,y)=(move[0],move[1])
		if self._is_on_board(x,y) and self.board[x][y] == 0:
			sandw_bits = self._get_all_sandwiched_bits(x,y)
			self.player_just_moved = 3 - self.player_just_moved
			self.board[x][y] = self.player_just_moved
			for (a,b) in sandw_bits:
				self.board[a][b] = self.player_just_moved

	def get_moves(self):
		""" Get all possible moves from this state.
		"""
		return [(x,y) for x in range(OTH_BOARD_SIZE) for y in range(OTH_BOARD_SIZE) if self.board[x][y] == 0 and self._exists_sandwiched_bit(x,y)]

	def _adjacent_to_enemy(self, x, y):
		""" Speeds up get_moves by only considering squares which are adjacent to an enemy-occupied square.
		"""
		for (dx,dy) in [(0,+1),(+1,+1),(+1,0),(+1,-1),(0,-1),(-1,-1),(-1,0),(-1,+1)]:
			if self._is_on_board(x+dx,y+dy) and self.board[x+dx][y+dy] == self.player_just_moved:
				return True
		return False

	def _get_adjacent_enemy_directions(self, x, y):
		""" Speeds up get_moves by only considering squares which are adjacent to an enemy-occupied square.
		"""
		adj_en_dirs = []
		for (dx,dy) in [(0,+1),(+1,+1),(+1,0),(+1,-1),(0,-1),(-1,-1),(-1,0),(-1,+1)]:
			if self._is_on_board(x+dx,y+dy) and self.board[x+dx][y+dy] == self.player_just_moved:
				adj_en_dirs.append((dx,dy))
		return adj_en_dirs

	def _exists_sandwiched_bit(self, x, y):
		""" Does there exist at least one counter which would be flipped if my counter was placed at (x,y)?
		"""
		for (dx,dy) in self._get_adjacent_enemy_directions(x,y):
			if len(self._get_sandwiched_bits_locations(x,y,dx,dy)) > 0:
				return True
		return False

	def _get_all_sandwiched_bits(self, x, y):
		""" Is (x,y) a possible move (i.e. opponent bits are sandwiched between (x,y) and my bits in some direction)?
		"""
		sandwiched = []
		for (dx,dy) in self._get_adjacent_enemy_directions(x,y):
			sandwiched.extend(self._get_sandwiched_bits_locations(x,y,dx,dy))
		return sandwiched

	def _get_sandwiched_bits_locations(self, x, y, dx, dy):
		""" Return the coordinates of all opponent bits sandwiched between (x,y) and my counter.
		"""
		x += dx
		y += dy
		sandwiched = []
		while self._is_on_board(x,y) and self.board[x][y] == self.player_just_moved:
			sandwiched.append((x,y))
			x += dx
			y += dy
		if self._is_on_board(x,y) and self.board[x][y] == 3 - self.player_just_moved: return sandwiched
		else: return [] # nothing sandwiched

	def _is_on_board(self, x, y):
		return x >= 0 and x < OTH_BOARD_SIZE and y >= 0 and y < OTH_BOARD_SIZE

	def get_result(self, player_just_moved):
		""" Get the game result from the viewpoint of playerjm.
		"""
		player_just_moved_count = len([(x,y) for x in range(OTH_BOARD_SIZE) for y in range(OTH_BOARD_SIZE) if self.board[x][y] == player_just_moved])        
		not_player_just_moved_count = len([(x,y) for x in range(OTH_BOARD_SIZE) for y in range(OTH_BOARD_SIZE) if self.board[x][y] == 3 - player_just_moved])
		if player_just_moved_count > not_player_just_moved_count: return 1.0
		elif not_player_just_moved_count > player_just_moved_count: return 0.0
		else: return 0.5 #it's a draw

	def __repr__(self):        
		b = self.board
		return f"""
		| {b[0][0]} | {b[0][1]} | {b[0][2]} | {b[0][3]} | {b[0][4]} | {b[0][5]} | {b[0][6]} | {b[0][7]} |
		| {b[1][0]} | {b[1][1]} | {b[1][2]} | {b[1][3]} | {b[1][4]} | {b[1][5]} | {b[1][6]} | {b[1][7]} |
		| {b[2][0]} | {b[2][1]} | {b[2][2]} | {b[2][3]} | {b[2][4]} | {b[2][5]} | {b[2][6]} | {b[2][7]} |
		| {b[3][0]} | {b[3][1]} | {b[3][2]} | {b[3][3]} | {b[3][4]} | {b[3][5]} | {b[3][6]} | {b[3][7]} |
		| {b[4][0]} | {b[4][1]} | {b[4][2]} | {b[4][3]} | {b[4][4]} | {b[4][5]} | {b[4][6]} | {b[4][7]} |
		| {b[5][0]} | {b[5][1]} | {b[5][2]} | {b[5][3]} | {b[5][4]} | {b[5][5]} | {b[5][6]} | {b[5][7]} |
		| {b[6][0]} | {b[6][1]} | {b[6][2]} | {b[6][3]} | {b[6][4]} | {b[6][5]} | {b[6][6]} | {b[6][7]} |
		| {b[7][0]} | {b[7][1]} | {b[7][2]} | {b[7][3]} | {b[7][4]} | {b[7][5]} | {b[7][6]} | {b[7][7]} |
		---------------------------------
		"""

	def is_game_over(self):
		return True if self.get_moves() == [] else False

	def quit_game_btn_clicked(self, x, y):
		return True if x in range (550, 587) and y in range(10,60) else False

	def board_clicked(self, x, y):
		return True if x in range (65, 540) and y in range(274,749) else False

	def restart_game_btn_clicked(self, x, y):
		return True if x in range (10, 275) and y in range(277, 325) else False

	def sound_btn_clicked(self, x, y):
		return True if x in range(5, 55) and y in range(340, 385) else False

	def game_info_btn_clicked(self, x, y):
		return True if x in range(5, 47) and y in range(404, 450) else False

	def close_game_info_btn_clicked(self, x, y):
		return True if x in range(549, 579) and y in range(22, 73) else False

	def _display_bit(self, screen, cell, bit_type):
		coords = self._get_top_left_cell_coords(cell)
		if coords is not None:
			if bit_type == 1: screen.blit(OTH_GREEN_BIT, coords)
			else: screen.blit(OTH_YELLOW_BIT, coords)
			pg.display.update()

	def display_winner(self, screen, game_result):        
		screen.blit(OTH_WINNER_STARS.convert_alpha(), (0, 0))
		if game_result == 0.5:
			pg.mixer.Channel(1).play(OTH_ITS_A_DRAW_SOUND, 2)
			screen.blit(OTH_ITS_A_DRAW_LABEL.convert_alpha(), (200, 90))
		elif (self.player_just_moved == 1 and game_result == 1.0) or (self.player_just_moved == 2 and game_result == 0):
			pg.mixer.Channel(1).play(OTH_WINNING_SOUND)
			screen.blit(OTH_YOU_WON_LABEL.convert_alpha(), (220, 90))
			screen.blit(OTH_HUMAN_PLAYER_WINNER_AVATAR.convert_alpha(), (14, 2))
			screen.blit(OTH_AI_PLAYER_LOSER_AVATAR.convert_alpha(), (416,49))
		elif (self.player_just_moved == 2 and game_result == 1.0) or (self.player_just_moved == 1 and game_result == 0):
			pg.mixer.Channel(1).play(OTH_WINNING_SOUND)
			screen.blit(OTH_AI_WON_LABEL.convert_alpha(), (225, 90))        
			screen.blit(pg.transform.flip(OTH_AI_PLAYER_AVATAR.convert_alpha(), True, False), (71,50))
			screen.blit(OTH_HUMAN_PLAYER_LOSER_AVATAR.convert_alpha(), (69,49))
			screen.blit(OTH_AI_PLAYER_WINNER_AVATAR.convert_alpha(), (370,5))
		pg.display.update()

	def display_game_info(self, screen):
		screen.blit(OTH_GAME_INFO.convert_alpha(), (0, 0))
		pg.display.update()

	def _get_top_left_cell_coords(self, cell):
		x_col0, y_row0 = 65, 275
		x_col1, y_row1 = 125, 335
		x_col2, y_row2 = 185, 395
		x_col3, y_row3 = 245, 455
		x_col4, y_row4 = 305, 515
		x_col5, y_row5 = 365, 575
		x_col6, y_row6 = 425, 635
		x_col7, y_row7 = 485, 695
		#row 0
		if cell == (0, 0): return (x_col0, y_row0)
		elif cell == (0, 1): return (x_col1, y_row0)
		elif cell == (0, 2): return (x_col2, y_row0)
		elif cell == (0, 3): return (x_col3, y_row0)
		elif cell == (0, 4): return (x_col4, y_row0)
		elif cell == (0, 5): return (x_col5, y_row0)
		elif cell == (0, 6): return (x_col6, y_row0)
		elif cell == (0, 7): return (x_col7, y_row0)
		#row 1
		elif cell == (1, 0): return (x_col0, y_row1)
		elif cell == (1, 1): return (x_col1, y_row1)
		elif cell == (1, 2): return (x_col2, y_row1)
		elif cell == (1, 3): return (x_col3, y_row1)
		elif cell == (1, 4): return (x_col4, y_row1)
		elif cell == (1, 5): return (x_col5, y_row1)
		elif cell == (1, 6): return (x_col6, y_row1)
		elif cell == (1, 7): return (x_col7, y_row1)
		#row 2
		elif cell == (2, 0): return (x_col0, y_row2)
		elif cell == (2, 1): return (x_col1, y_row2)
		elif cell == (2, 2): return (x_col2, y_row2)
		elif cell == (2, 3): return (x_col3, y_row2)
		elif cell == (2, 4): return (x_col4, y_row2)
		elif cell == (2, 5): return (x_col5, y_row2)
		elif cell == (2, 6): return (x_col6, y_row2)
		elif cell == (2, 7): return (x_col7, y_row2)
		#row 3
		elif cell == (3, 0): return (x_col0, y_row3)
		elif cell == (3, 1): return (x_col1, y_row3)
		elif cell == (3, 2): return (x_col2, y_row3)
		elif cell == (3, 3): return (x_col3, y_row3)
		elif cell == (3, 4): return (x_col4, y_row3)
		elif cell == (3, 5): return (x_col5, y_row3)
		elif cell == (3, 6): return (x_col6, y_row3)
		elif cell == (3, 7): return (x_col7, y_row3)
		#row 4
		elif cell == (4, 0): return (x_col0, y_row4)
		elif cell == (4, 1): return (x_col1, y_row4)
		elif cell == (4, 2): return (x_col2, y_row4)
		elif cell == (4, 3): return (x_col3, y_row4)
		elif cell == (4, 4): return (x_col4, y_row4)
		elif cell == (4, 5): return (x_col5, y_row4)
		elif cell == (4, 6): return (x_col6, y_row4)
		elif cell == (4, 7): return (x_col7, y_row4)
		#row 5
		elif cell == (5, 0): return (x_col0, y_row5)
		elif cell == (5, 1): return (x_col1, y_row5)
		elif cell == (5, 2): return (x_col2, y_row5)
		elif cell == (5, 3): return (x_col3, y_row5)
		elif cell == (5, 4): return (x_col4, y_row5)
		elif cell == (5, 5): return (x_col5, y_row5)
		elif cell == (5, 6): return (x_col6, y_row5)
		elif cell == (5, 7): return (x_col7, y_row5)
		#row 6
		elif cell == (6, 0): return (x_col0, y_row6)
		elif cell == (6, 1): return (x_col1, y_row6)
		elif cell == (6, 2): return (x_col2, y_row6)
		elif cell == (6, 3): return (x_col3, y_row6)
		elif cell == (6, 4): return (x_col4, y_row6)
		elif cell == (6, 5): return (x_col5, y_row6)
		elif cell == (6, 6): return (x_col6, y_row6)
		elif cell == (6, 7): return (x_col7, y_row6)
		#row 7
		elif cell == (7, 0): return (x_col0, y_row7)
		elif cell == (7, 1): return (x_col1, y_row7)
		elif cell == (7, 2): return (x_col2, y_row7)
		elif cell == (7, 3): return (x_col3, y_row7)
		elif cell == (7, 4): return (x_col4, y_row7)
		elif cell == (7, 5): return (x_col5, y_row7)
		elif cell == (7, 6): return (x_col6, y_row7)
		elif cell == (7, 7): return (x_col7, y_row7)
		return None


	def get_cell_clicked(self, x, y):
		cell = None
		#row 0
		if x in range(65, 121) and y in range(275, 330) and self.board[0][0] == 0:
			cell = (0,0)
		elif x in range(125, 180) and y in range(275, 330) and self.board[0][1] == 0:
		   cell = (0,1)
		elif x in range(185, 240) and y in range(275, 330) and self.board[0][2] == 0:
			cell = (0,2)
		elif x in range(245, 300) and y in range(275, 330) and self.board[0][3] == 0:
			cell = (0,3)
		elif x in range(305, 360) and y in range(275, 330) and self.board[0][4] == 0:
			cell = (0,4)
		elif x in range(365, 420) and y in range(275, 330) and self.board[0][5] == 0:
			cell = (0,5)
		elif x in range(425, 480) and y in range(275, 330) and self.board[0][6] == 0:
			cell = (0,6)
		elif x in range(485, 540) and y in range(275, 330) and self.board[0][7] == 0:
			cell = (0,7)
		#row 1
		elif x in range(65, 121) and y in range(335, 390) and self.board[1][0] == 0:
			cell = (1,0)
		elif x in range(125, 180) and y in range(335, 390) and self.board[1][1] == 0:
			cell = (1,1)
		elif x in range(185, 240) and y in range(335, 390) and self.board[1][2] == 0:
			cell = (1,2)
		elif x in range(245, 300) and y in range(335, 390) and self.board[1][3] == 0:
			cell = (1,3)
		elif x in range(305, 360) and y in range(335, 390) and self.board[1][4] == 0:
			cell = (1,4)
		elif x in range(365, 420) and y in range(335, 390) and self.board[1][5] == 0:
			cell = (1,5)
		elif x in range(425, 480) and y in range(335, 390) and self.board[1][6] == 0:
			cell = (1,6)
		elif x in range(485, 540) and y in range(335, 390) and self.board[1][7] == 0:
			cell = (1,7)
		#row 2
		elif x in range(65, 121) and y in range(395, 450) and self.board[2][0] == 0:
			cell = (2,0)
		elif x in range(125, 180) and y in range(395, 450) and self.board[2][1] == 0:
			cell = (2,1)
		elif x in range(185, 240) and y in range(395, 450) and self.board[2][2] == 0:
			cell = (2,2)
		elif x in range(245, 300) and y in range(395, 450) and self.board[2][3] == 0:
			cell = (2,3)
		elif x in range(305, 360) and y in range(395, 450) and self.board[2][4] == 0:
			cell = (2,4)
		elif x in range(365, 420) and y in range(395, 450) and self.board[2][5] == 0:
			cell = (2,5)
		elif x in range(425, 480) and y in range(395, 450) and self.board[2][6] == 0:
			cell = (2,6)
		elif x in range(485, 540) and y in range(395, 450) and self.board[2][7] == 0:
			cell = (2,7)
		#row 3
		elif x in range(65, 121) and y in range(455, 510) and self.board[3][0] == 0:
			cell = (3,0)
		elif x in range(125, 180) and y in range(455, 510) and self.board[3][1] == 0:
			cell = (3,1)
		elif x in range(185, 240) and y in range(455, 510) and self.board[3][2] == 0:
			cell = (3,2)
		elif x in range(245, 300) and y in range(455, 510) and self.board[3][3] == 0:
			cell = (3,3)
		elif x in range(305, 360) and y in range(455, 510) and self.board[3][4] == 0:
			cell = (3,4)
		elif x in range(365, 420) and y in range(455, 510) and self.board[3][5] == 0:
			cell = (3,5)
		elif x in range(425, 480) and y in range(455, 510) and self.board[3][6] == 0:
			cell = (3,6)
		elif x in range(485, 540) and y in range(455, 510) and self.board[3][7] == 0:
			cell = (3,7)
		#row 4
		elif x in range(65, 121) and y in range(515, 570) and self.board[4][0] == 0:
			cell = (4,0)
		elif x in range(125, 180) and y in range(515, 570) and self.board[4][1] == 0:
			cell = (4,1)
		elif x in range(185, 240) and y in range(515, 570) and self.board[4][2] == 0:
			cell = (4,2)
		elif x in range(245, 300) and y in range(515, 570) and self.board[4][3] == 0:
			cell = (4,3)
		elif x in range(305, 360) and y in range(515, 570) and self.board[4][4] == 0:
			cell = (4,4)
		elif x in range(365, 420) and y in range(515, 570) and self.board[4][5] == 0:
			cell = (4,5)
		elif x in range(425, 480) and y in range(515, 570) and self.board[4][6] == 0:
			cell = (4,6)
		elif x in range(485, 540) and y in range(515, 570) and self.board[4][7] == 0:
			cell = (4,7)
		#row 5
		elif x in range(65, 121) and y in range(575, 630) and self.board[5][0] == 0:
			cell = (5,0)
		elif x in range(125, 180) and y in range(575, 630) and self.board[5][1] == 0:
			cell = (5,1)
		elif x in range(185, 240) and y in range(575, 630) and self.board[5][2] == 0:
			cell = (5,2)
		elif x in range(245, 300) and y in range(575, 630) and self.board[5][3] == 0:
			cell = (5,3)
		elif x in range(305, 360) and y in range(575, 630) and self.board[5][4] == 0:
			cell = (5,4)
		elif x in range(365, 420) and y in range(575, 630) and self.board[5][5] == 0:
			cell = (5,5)
		elif x in range(425, 480) and y in range(575, 630) and self.board[5][6] == 0:
			cell = (5,6)
		elif x in range(485, 540) and y in range(575, 630) and self.board[5][7] == 0:
			cell = (5,7)
		#row 6
		elif x in range(65, 121) and y in range(635, 690) and self.board[6][0] == 0:
			cell = (6,0)
		elif x in range(125, 180) and y in range(635, 690) and self.board[6][1] == 0:
			cell = (6,1)
		elif x in range(185, 240) and y in range(635, 690) and self.board[6][2] == 0:
			cell = (6,2)
		elif x in range(245, 300) and y in range(635, 690) and self.board[6][3] == 0:
			cell = (6,3)
		elif x in range(305, 360) and y in range(635, 690) and self.board[6][4] == 0:
			cell = (6,4)
		elif x in range(365, 420) and y in range(635, 690) and self.board[6][5] == 0:
			cell = (6,5)
		elif x in range(425, 480) and y in range(635, 690) and self.board[6][6] == 0:
			cell = (6,6)
		elif x in range(485, 540) and y in range(635, 690) and self.board[6][7] == 0:
			cell = (6,7)
		#row 7
		elif x in range(65, 121) and y in range(695, 750) and self.board[7][0] == 0:
			cell = (7,0)
		elif x in range(125, 180) and y in range(695, 750) and self.board[7][1] == 0:
			cell = (7,1)
		elif x in range(185, 240) and y in range(695, 750) and self.board[7][2] == 0:
			cell = (7,2)
		elif x in range(245, 300) and y in range(695, 750) and self.board[7][3] == 0:
			cell = (7,3)
		elif x in range(305, 360) and y in range(695, 750) and self.board[7][4] == 0:
			cell = (7,4)
		elif x in range(365, 420) and y in range(695, 750) and self.board[7][5] == 0:
			cell = (7,5)
		elif x in range(425, 480) and y in range(695, 750) and self.board[7][6] == 0:
			cell = (7,6)
		elif x in range(485, 540) and y in range(695, 750) and self.board[7][7] == 0:
			cell = (7,7)
		return cell

	def _display_board_updates(self, screen):
		for row in range(0, OTH_BOARD_SIZE):
			for col in range(0, OTH_BOARD_SIZE):
				if self.board[row][col] == 1:
					self._display_bit(screen, (row, col), 1)
				elif self.board[row][col] == 2:
					self._display_bit(screen, (row, col), 2)
		pg.display.update()

	def draw_game_screen(self, screen, game_level, audio_muted, set_caption):
		#game screen settings
		screen = pg.display.set_mode((OTH_SCREEN_WIDTH , OTH_SCREEN_HEIGHT))        
		screen.blit(OTH_BACKGROUND_IMG.convert_alpha(), [0, 0])
		if set_caption:
			caption = f"Othello Easy Level: Number of simulations: {OTH_SIMS_PER_MOVE_EASY}"
			if game_level == GameLevels.MEDIUM: caption = f"Othello Medium Level: Number of simulations: {OTH_SIMS_PER_MOVE_MEDIUM}"
			elif game_level == GameLevels.HARD: caption = f"Othello Hard Level: Number of simulations: {OTH_SIMS_PER_MOVE_HARD}"
			pg.display.set_caption(caption)
		#display players labels     
		screen.blit(OTH_HUMAN_PLAYER_LABEL.convert_alpha(), (67, 180))
		screen.blit(OTH_AI_PLAYER_LABEL.convert_alpha(), (472, 180))
		#display player avatars
		screen.blit(OTH_HUMAN_PLAYER_AVATAR.convert_alpha(), [70, 50])
		screen.blit(OTH_AI_PLAYER_AVATAR.convert_alpha(), [415, 50])      
		#display buttons
		screen.blit(OTH_RESTART_BTN.convert_alpha(), (5, 275))
		if audio_muted:
			screen.blit(OTH_SOUND_OFF_BTN.convert_alpha(), (5, 340))
		else:
			screen.blit(OTH_SOUND_ON_BTN.convert_alpha(), (5, 340))
		screen.blit(OTH_GAME_INFO_BTN.convert_alpha(), (10, 403))
		screen.blit(OTH_BACK_BTN.convert_alpha(), (550, 10))
		#draw 8X8 board        
		for row in range(8):
			for col in range(8):
				pg.draw.rect(screen, DTEAL, (row*OTH_SQUARE_SIZE+63, col*OTH_SQUARE_SIZE+272, OTH_SQUARE_SIZE, OTH_SQUARE_SIZE), 3)
		pg.display.update()
		self._display_board_updates(screen)
		pg.display.update()

	def main_game_loop(self, screen, game_level):
		#set game audio
		OTH_BGR_MUSIC.set_volume(0.3)
		OTH_AI_THINKING_SOUND.set_volume(0.1)
		CLICK_SOUND.set_volume(0.5)
		pg.mixer.Channel(0).play(OTH_BGR_MUSIC, -1)
		self.draw_game_screen(screen, game_level, audio_muted = False, set_caption = True)
		#set game difficulty: use lower values or the GUI version will take too long to make a move
		sims_per_move = OTH_SIMS_PER_MOVE_EASY
		if game_level == GameLevels.MEDIUM: sims_per_move = OTH_SIMS_PER_MOVE_MEDIUM
		elif game_level == GameLevels.HARD: sims_per_move = OTH_SIMS_PER_MOVE_HARD
		run = True
		clock = pg.time.Clock()
		game_over = False
		ai_move = True
		audio_muted = False
		game_info_visible = False
		while run:
			clock.tick(FPS)				
			for event in pg.event.get():                
				if event.type == pg.MOUSEBUTTONDOWN:
					if not audio_muted: CLICK_SOUND.play()
					x, y = pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]
					if self.board_clicked(x, y) and self.player_just_moved == 2 and not game_over:
						move = self.get_cell_clicked(x, y)
						if move is not None and self._exists_sandwiched_bit(move[0], move[1]):
							self.do_move(move)
							self.draw_game_screen(screen, game_level, audio_muted, set_caption = False)
							if self.is_game_over():
								game_result = self.get_result(self.player_just_moved)
								self.display_winner(screen, game_result)
								game_over = True
								break
							screen.blit(OTH_AI_PLAYER_THINKING_AVATAR.convert_alpha(),(415, 50))
							screen.blit(OTH_AI_THINKING_LABEL.convert_alpha(),(437, 199))
							pg.display.update()
							if not audio_muted: pg.mixer.Channel(1).play(OTH_AI_THINKING_SOUND, -1)
							# do AI move
							ai_move = UCT.uct(self, sims_per_move)
							self.do_move(ai_move)
							self.draw_game_screen(screen, game_level, audio_muted, set_caption = False)
							if not audio_muted: OTH_AI_THINKING_SOUND.stop()
							if self.is_game_over():
								game_result = self.get_result(self.player_just_moved)
								self.display_winner(screen, game_result)
								game_over = True
								break

					elif self.restart_game_btn_clicked(x, y):
						#reset game
						self.board = []
						for y in range(OTH_BOARD_SIZE):
							self.board.append([0]*OTH_BOARD_SIZE)
						self.board[OTH_BOARD_SIZE//2][OTH_BOARD_SIZE//2] = self.board[OTH_BOARD_SIZE//2-1][OTH_BOARD_SIZE//2-1] = 1
						self.board[OTH_BOARD_SIZE//2][OTH_BOARD_SIZE//2-1] = self.board[OTH_BOARD_SIZE//2-1][OTH_BOARD_SIZE//2] = 2
						self.player_just_moved = 2
						screen.fill(BLACK)
						screen.blit(RESTARTING_GAME_LABEL.convert_alpha(), [160, 300])
						pg.display.update()
						time.sleep(1)
						self.draw_game_screen(screen, game_level, audio_muted, set_caption = False)
						game_over = False

					elif self.sound_btn_clicked(x, y):
						if audio_muted:
							audio_muted = False
							pg.mixer.unpause()
							self.draw_game_screen(screen, game_level, audio_muted, set_caption = False)
							screen.blit(OTH_SOUND_ON_BTN.convert_alpha(), (5, 340))
						else:
							audio_muted = True
							pg.mixer.pause()
							screen.blit(OTH_SOUND_OFF_BTN.convert_alpha(), (5, 339))
						pg.display.update()

					elif self.game_info_btn_clicked(x, y):
						game_info_visible = True
						self.display_game_info(screen)
						pg.display.update()

					elif self.close_game_info_btn_clicked(x, y) and game_info_visible:
						self.draw_game_screen(screen, game_level, audio_muted, set_caption = False)
						game_info_visible = False

					elif self.quit_game_btn_clicked(x, y) and not game_info_visible:
						run = False
						OTH_BGR_MUSIC.stop()
						pg.mixer.Channel(0).play(MAIN_MUSIC_THEME, -1)
						#reset game
						self.board = []
						for y in range(OTH_BOARD_SIZE):
							self.board.append([0] * OTH_BOARD_SIZE)
						self.board[OTH_BOARD_SIZE//2][OTH_BOARD_SIZE//2] = self.board[OTH_BOARD_SIZE//2-1][OTH_BOARD_SIZE//2-1] = 1
						self.board[OTH_BOARD_SIZE//2][OTH_BOARD_SIZE//2-1] = self.board[OTH_BOARD_SIZE//2-1][OTH_BOARD_SIZE//2] = 2
						self.player_just_moved = 2
						game_over = False
						return screen
		return screen