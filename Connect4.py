import pygame as pg
import time
import numpy as np
import copy
from config import *
from Game import Game
from GameGUIInterface import GameGUIInterface
from UCT import UCT


class Connect4(Game, GameGUIInterface):
	""" Connect4 is played on 6x7 board arranges as below

	 row: col:0  1  2  3  4  5  6
           0   [[ 0  0  0  0  0  0  0]
	   1    [ 0  0  0  0  0  0  0]
	   2    [ 0  0  0  0  0  0  0]
	   3    [ 0  0  0  0  0  0  0]
	   4    [ 0  0  0  0  0  0  0]
	   5    [ 0  0  0  0  0  0  0]]
		where 0 = empty, 1 = player 1 (Red), 2 = player 2 (Yellow)
	"""
	def __init__(self):
		self.player_just_moved = 2 # At the root pretend the player just moved is p2 - p1 has the first move
		self.board = np.zeros((C4_ROWS, C4_COLS), dtype=int)

	def clone(self):
		""" Create a deep clone of this game state.
		"""
		state = Connect4()
		state.player_just_moved = self.player_just_moved
		state.board = copy.deepcopy(self.board)
		return state

	def do_move(self, column):
		""" Update a state by carrying out the given move.
			Must update player_just_moved.
		"""        
		if column >=0 and column <=6 and self.board[0][column] == 0:
			row = self._get_lowest_row_with_free_cell(column)
			self.player_just_moved = 3 - self.player_just_moved
			self.board[row][column] = self.player_just_moved

	def __repr__(self):
		""" Return a string representation of the board.
		"""
		b = self.board
		return f"""
		| {b[0][0]} | {b[0][1]} | {b[0][2]} | {b[0][3]} | {b[0][4]} | {b[0][5]} | {b[0][6]} |
		| {b[1][0]} | {b[1][1]} | {b[1][2]} | {b[1][3]} | {b[1][4]} | {b[1][5]} | {b[1][6]} |
		| {b[2][0]} | {b[2][1]} | {b[2][2]} | {b[2][3]} | {b[2][4]} | {b[2][5]} | {b[2][6]} |
		| {b[3][0]} | {b[3][1]} | {b[3][2]} | {b[3][3]} | {b[3][4]} | {b[3][5]} | {b[3][6]} |
		| {b[4][0]} | {b[4][1]} | {b[4][2]} | {b[4][3]} | {b[4][4]} | {b[4][5]} | {b[4][6]} |
		| {b[5][0]} | {b[5][1]} | {b[5][2]} | {b[5][3]} | {b[5][4]} | {b[5][5]} | {b[5][6]} |
		-----------------------------
		"""

	def is_game_over(self):
		""" Returns True if all cells are taken or if a player formed a line of four bits.
		    This is a changed version of the code taken from https://github.com/KeithGalli/Connect4-Python/blob/master/connect4.py
		"""
		#check if all slots are taken
		all_cells_taken = (self.board != 0).all()
		if all_cells_taken:
			return True
		# Check horizontal locations for win
		for c in range(C4_COLS-3):
			for r in range(C4_ROWS):
				if self.board[r][c] == self.board[r][c+1] == self.board[r][c+2] == self.board[r][c+3] != 0:	return True
		# Check vertical locations for win
		for c in range(C4_COLS):
			for r in range(C4_ROWS-3):
				if self.board[r][c] == self.board[r+1][c] == self.board[r+2][c] == self.board[r+3][c] != 0: return True
		# Check positively sloped diagonals
		for c in range(C4_COLS-3):
			for r in range(C4_ROWS-3):
				if self.board[r][c] == self.board[r+1][c+1] == self.board[r+2][c+2] == self.board[r+3][c+3] != 0: return True
		# Check negatively sloped diagonals
		for c in range(C4_COLS-3):
			for r in range(3, C4_ROWS):
				if self.board[r][c] == self.board[r-1][c+1] == self.board[r-2][c+2] == self.board[r-3][c+3] != 0: return True
		return False

	def get_moves(self):
		""" Get all possible moves from this state.
		"""
		if self.is_game_over(): return []
		valid_moves = []
		for i in range(0, C4_COLS): #check if the top cell of each column is empty
			if self.board[0][i] == 0: valid_moves.append(i)
		return valid_moves

	def get_result(self, player_just_moved):
		""" Get the game result from the viewpoint of player_just_moved
		    Code for checking lines is a modification of code taken from
		    https://github.com/KeithGalli/Connect4-Python/blob/master/connect4.py
		"""
		# Check horizontal locations for win
		for c in range(C4_COLS-3):
			for r in range(C4_ROWS):
				if self.board[r][c] == self.board[r][c+1] == self.board[r][c+2] == self.board[r][c+3] == player_just_moved:
					return 1.0
				elif self.board[r][c] == self.board[r][c+1] == self.board[r][c+2] == self.board[r][c+3] == 3 - player_just_moved:
					return 0.0
		# Check vertical locations for win
		for c in range(C4_COLS):
			for r in range(C4_ROWS-3):
				if self.board[r][c] == self.board[r+1][c] == self.board[r+2][c] == self.board[r+3][c] == player_just_moved:
					return 1.0
				elif self.board[r][c] == self.board[r+1][c] == self.board[r+2][c] == self.board[r+3][c] == 3 - player_just_moved:
					return 0.0
		# Check positively sloped diagonals
		for c in range(C4_COLS-3):
			for r in range(C4_ROWS-3):
				if self.board[r][c] == self.board[r+1][c+1] == self.board[r+2][c+2] == self.board[r+3][c+3] == player_just_moved:
					return 1.0
				elif self.board[r][c] == self.board[r+1][c+1] == self.board[r+2][c+2] == self.board[r+3][c+3] == 3 - player_just_moved:
					return 0.0
		# Check negatively sloped diagonals
		for c in range(C4_COLS-3):
			for r in range(3, C4_ROWS):
				if self.board[r][c] == self.board[r-1][c+1] == self.board[r-2][c+2] == self.board[r-3][c+3] == player_just_moved:
					return 1.0
				elif self.board[r][c] == self.board[r-1][c+1] == self.board[r-2][c+2] == self.board[r-3][c+3] == 3 -player_just_moved:
					return 0.0

		#if all slots are taken - then it's a draw
		all_cells_taken = (self.board != 0).all()
		if all_cells_taken:	return 0.5
		#if the move was not a winning one - return None
		return None
	
	def _action_arrow_clicked(self, x, y):
		return True if x in range (85, 520) and y in range(218,574) else False

	def quit_game_btn_clicked(self, x, y):
		return True if x in range (550, 586) and y in range(10,60) else False

	def restart_game_btn_clicked(self, x, y):
		return True if x in range (5, 60) and y in range(5,60) else False

	def sound_btn_clicked(self, x, y):
		return True if x in range(5, 55) and y in range(65, 110) else False

	def game_info_btn_clicked(self, x, y):
		return True if x in range(15, 45) and y in range(120, 170) else False

	def close_game_info_btn_clicked(self, x, y):
		return True if x in range(540, 590) and y in range(5, 65) else False

	def get_cell_clicked(self, x, y):
		""" Returns the column selected by user
		"""
		if x in range(69, 129) and y in range(193, 252): return 0
		elif x in range(141, 192) and y in range(193, 252): return 1
		elif x in range(209, 262) and y in range(193, 252): return 2
		elif x in range(277, 324) and y in range(193, 252): return 3
		elif x in range(341, 388) and y in range(193, 252): return 4
		elif x in range(407, 451) and y in range(193, 252): return 5
		elif x in range(467, 519) and y in range(193, 252): return 6
		return None

	def _get_top_left_cell_coords(self, cell):
		x_col0 = 73
		x_col1 = 139
		x_col2 = 205
		x_col3 = 271
		x_col4 = 336
		x_col5 = 401
		x_col6 = 466
		y_row0 = 254
		y_row1 = 317
		y_row2 = 380
		y_row3 = 442
		y_row4 = 504
		y_row5 = 567
		#ROW 0
		if cell == 0: return [x_col0, y_row0]
		elif cell == 1: return [x_col1, y_row0]
		elif cell == 2: return [x_col2, y_row0]
		elif cell == 3: return [x_col3, y_row0]
		elif cell == 4: return [x_col4, y_row0]
		elif cell == 5: return [x_col5, y_row0]
		elif cell == 6: return [x_col6, y_row0]
		#ROW 1
		elif cell == 10: return [x_col0, y_row1]
		elif cell == 11: return [x_col1, y_row1]
		elif cell == 12: return [x_col2, y_row1]
		elif cell == 13: return [x_col3, y_row1]
		elif cell == 14: return [x_col4, y_row1]
		elif cell == 15: return [x_col5, y_row1]
		elif cell == 16: return [x_col6, y_row1]
		#ROW 2
		elif cell == 20: return [x_col0, y_row2]
		elif cell == 21: return [x_col1, y_row2]
		elif cell == 22: return [x_col2, y_row2]
		elif cell == 23: return [x_col3, y_row2]
		elif cell == 24: return [x_col4, y_row2]
		elif cell == 25: return [x_col5, y_row2]
		elif cell == 26: return [x_col6, y_row2]
		 #ROW 3
		elif cell == 30: return [x_col0, y_row3]
		elif cell == 31: return [x_col1, y_row3]
		elif cell == 32: return [x_col2, y_row3]
		elif cell == 33: return [x_col3, y_row3]
		elif cell == 34: return [x_col4, y_row3]
		elif cell == 35: return [x_col5, y_row3]
		elif cell == 36: return [x_col6, y_row3]
		 #ROW 4
		elif cell == 40: return [x_col0, y_row4]
		elif cell == 41: return [x_col1, y_row4]
		elif cell == 42: return [x_col2, y_row4]
		elif cell == 43: return [x_col3, y_row4]
		elif cell == 44: return [x_col4, y_row4]
		elif cell == 45: return [x_col5, y_row4]
		elif cell == 46: return [x_col6, y_row4]
		 #ROW 5
		elif cell == 50: return [x_col0, y_row5]
		elif cell == 51: return [x_col1, y_row5]
		elif cell == 52: return [x_col2, y_row5]
		elif cell == 53: return [x_col3, y_row5]
		elif cell == 54: return [x_col4, y_row5]
		elif cell == 55: return [x_col5, y_row5]
		elif cell == 56: return [x_col6, y_row5]
		else: return None

	def _get_lowest_row_with_free_cell(self, column):
		column_values = self.board[:,column]
		for i in range(0, len(column_values)-1):
			if column_values[i+1] != 0:
				return i
		return len(column_values)-1

	def _display_move(self, screen, bit, column=None):
		assert column is not None
		lowestFreeRow = (str)(self._get_lowest_row_with_free_cell(column))
		if lowestFreeRow == 0: lowestFreeRow = ''
		cell = (int)(lowestFreeRow+((str)(column)))
		topLeftCellCoords = self._get_top_left_cell_coords(cell)
		screen.blit(bit, topLeftCellCoords)
		return True

	def display_game_info(self, screen):
		screen.blit(C4_GAME_INFO.convert_alpha(), (0, 0))
		pg.display.update()

	def display_winner(self, screen, gameResult):
		C4_WIN_SOUND.play()
		if gameResult == 0.5:
			screen.blit(ITS_A_DRAW_LABEL.convert_alpha(),(215,100))
			return
		#rescale avatars to display winner and loser
		humanWinner = pg.transform.scale(C4_HUMAN_WINNER_AVATAR, (AVATAR_SIZE+40, AVATAR_SIZE+40))
		humanLoser = pg.transform.scale(C4_HUMAN_LOSER_AVATAR, (AVATAR_SIZE, AVATAR_SIZE))
		AIWinner = pg.transform.scale(C4_AI_WINNER_AVATAR, (AVATAR_SIZE+80, AVATAR_SIZE+80))
		AILoser = pg.transform.scale(C4_AI_LOSER_AVATAR, (AVATAR_SIZE+2, AVATAR_SIZE+2))
		#if human player won
		if (self.player_just_moved == 1 and gameResult == 1.0) or (self.player_just_moved == 2 and gameResult == 0.0):    
			screen.blit(humanWinner.convert_alpha(), (60, 45))
			screen.blit(AILoser.convert_alpha(), (414, 50))
			screen.blit(YOU_WON_LABEL.convert_alpha(),(240,30))
		else:
			screen.blit(AIWinner.convert_alpha(), (370, 30))
			screen.blit(humanLoser.convert_alpha(), (80, 50))
			screen.blit(AI_WON_LABEL.convert_alpha(),(232,30))
			
	def _display_board_updates(self, screen):
		cell = 0
		for row in range(0, C4_ROWS):
			for col in range(0, C4_COLS):				
				if self.board[row][col] == 1:
					screen.blit(C4_RED_MOON_BIT, self._get_top_left_cell_coords(cell))
				elif self.board[row][col] == 2:
					screen.blit(C4_YELLOW_MOON_BIT, self._get_top_left_cell_coords(cell))
				cell += 1
			cell = 0
			cell = cell+(row+1)*10 #go to next row
		pg.display.update()

	def draw_game_screen(self, screen, gameLevel, audio_muted, set_caption):
		#increase screen size and display background image
		screen = pg.display.set_mode((C4_SCREEN_WIDTH , C4_SCREEN_HEIGHT))
		screen.blit(C4_BACKGROUND_IMG.convert_alpha(), [0, 0])
		if set_caption:
			caption = f"Connect4: Easy - Number of simulations: {C4_SIMS_PER_MOVE_EASY}"
			if gameLevel == GameLevels.MEDIUM: caption = f"Connect4: Medium - Number of simulations: {C4_SIMS_PER_MOVE_MEDIUM}"
			elif gameLevel == GameLevels.HARD: caption = f"Connect4: Hard - Number of simulations: {C4_SIMS_PER_MOVE_HARD}"
			pg.display.set_caption(caption)
		#display players avatars
		screen.blit(C4_HUMAN_PLAYER_AVATAR.convert_alpha(), [80,50])
		screen.blit(C4_AI_PLAYER_AVATAR.convert_alpha(), [415,50])
		#display players labels and game buttons
		screen.blit(C4_HUMAN_PLAYER_LABEL.convert_alpha(),(85,25))
		screen.blit(C4_AI_PLAYER_LABEL.convert_alpha(),(456,25))        
		screen.blit(C4_RESTART_BTN.convert_alpha(), (5,5))
		if audio_muted: screen.blit(C4_SOUND_OFF_BTN.convert_alpha(), (5,65))
		else: screen.blit(C4_SOUND_ON_BTN.convert_alpha(), (5,65))
		screen.blit(C4_GAME_INFO_BTN.convert_alpha(), (15,120))
		screen.blit(C4_BACK_BTN.convert_alpha(),(550,10))
		pg.display.update()

	def main_game_loop(self, screen, gameLevel):
		pg.display.update()
		self.draw_game_screen(screen, gameLevel, audio_muted = False, set_caption = True)
		#set volume for background music and sounds
		C4_BGR_MUSIC.set_volume(0.3)
		C4_AI_THINKING_SOUND.set_volume(0.8)
		pg.mixer.Channel(0).play(C4_BGR_MUSIC, -1)
		#set game difficulty
		sims_per_move = C4_SIMS_PER_MOVE_EASY
		if gameLevel == GameLevels.MEDIUM: sims_per_move = C4_SIMS_PER_MOVE_MEDIUM
		elif gameLevel == GameLevels.HARD: sims_per_move = C4_SIMS_PER_MOVE_HARD
		run = True
		clock = pg.time.Clock()
		gameOver=False
		audio_muted = False
		game_info_visible = False
		while run:
			clock.tick(FPS)
			if self.player_just_moved == 1 and not gameOver and self.get_moves() != []:
				#display thinking AI avatar and label
				screen.blit(C4_AI_PLAYER_THINKING_AVATAR.convert_alpha(),(415,50))
				screen.blit(AI_THINKING_LABEL.convert_alpha(),(430,100))
				pg.display.update()
				if not audio_muted: pg.mixer.Channel(1).play(C4_AI_THINKING_SOUND)
				#get AI move
				AImove = UCT.uct(self, sims_per_move)
				if not audio_muted:	C4_AI_THINKING_SOUND.stop()
				#display the normal AI avatar
				screen.blit(C4_AI_PLAYER_AVATAR, [415,50])
				pg.display.update()
				self._display_move(screen, C4_YELLOW_MOON_BIT.convert_alpha(), AImove)
				#do AI move
				self.do_move(AImove)
				#check if it was the winning move
				gameResult = self.get_result(self.player_just_moved)
				if gameResult is not None:
					self.display_winner(screen, gameResult)
					gameOver = True
			for event in pg.event.get():
				if event.type == pg.MOUSEBUTTONDOWN:
					if not audio_muted:	CLICK_SOUND.play()
					x, y = pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]
					#if its human player's turn
					if self._action_arrow_clicked(x, y) and self.player_just_moved == 2 and not gameOver:
						move = self.get_cell_clicked(x, y)
						#if move is valid and the column is not full
						if move is not None and self.board[0][move] == 0:
							self._display_move(screen, C4_RED_MOON_BIT.convert_alpha(), move)
							self.do_move(move)
							#check if it was the winning move
							gameResult = self.get_result(self.player_just_moved)
							if gameResult is not None:
								self.display_winner(screen, gameResult)
								gameOver = True
								break
					elif self.quit_game_btn_clicked(x, y) and not game_info_visible:
						run = False
						gameOver = False
						C4_BGR_MUSIC.stop()
						if not audio_muted:	pg.mixer.Channel(0).play(MAIN_MUSIC_THEME, -1)
						self.board = np.zeros((C4_ROWS, C4_COLS), dtype=int)
						self.player_just_moved = 2
						return screen						
					elif self.restart_game_btn_clicked(x, y):
						self.board = np.zeros((C4_ROWS, C4_COLS), dtype=int)
						self.player_just_moved = 2
						screen.fill(BLACK)
						screen.blit(RESTARTING_GAME_LABEL, [160,300])
						pg.display.update()
						time.sleep(1)
						self.draw_game_screen(screen, gameLevel, audio_muted, set_caption = False)
						gameOver = False
					elif self.sound_btn_clicked(x, y):
						if audio_muted:
							audio_muted = False
							pg.mixer.unpause()
							self.draw_game_screen(screen, gameLevel, audio_muted, set_caption = False)
							screen.blit(C4_SOUND_ON_BTN, (5,65))                            
						else:
							audio_muted = True
							pg.mixer.pause()
							screen.blit(C4_SOUND_OFF_BTN, (5,65))							
					elif self.game_info_btn_clicked(x, y):
						game_info_visible = True
						self.display_game_info(screen)
					elif self.close_game_info_btn_clicked(x, y):
						game_info_visible = False
						self.draw_game_screen(screen, gameLevel, audio_muted, set_caption = False)
						self._display_board_updates(screen)
				elif event.type == pg.QUIT:	run = False
			pg.display.update()
		return screen
