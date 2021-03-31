import pygame as pg
import time
import os
from config import *
from Game import Game
from GameGUIInterface import GameGUIInterface
from UCT import UCT


class Checkers(Game, GameGUIInterface):
	""" A state of the game of Checkers, i.e. the game board.
		The board is a 2D array where 0 = empty, 1 = player 1, 2 = player 2, 10 = player's 1 King, 20 = player's 2 King.
	"""
	def __init__(self):
		self.human_player_pieces = [1, 10]
		self.ai_player_pieces = [2, 20]
		self.player_just_moved = 2 #at the root pretend the player just moved is player 2
		self.human_player_pieces_count = 12
		self.ai_player_pieces_count = 12
		self.board = [[0] * CHECKERS_BOARD_SIZE for x in range(CHECKERS_BOARD_SIZE)]
		#populate the board:  0 = empty, 1 = player 1, 2 = player 2
		for row in range(CHECKERS_BOARD_SIZE):
			start = 0
			if row in [0, 2, 6]:
				start +=1            
			for col in range(start, CHECKERS_BOARD_SIZE, 2):
				if row in [3, 4]: # Skip 2 middle rows
					continue
				elif row < 4:
					self.board[row][col] = self.player_just_moved
				else: 
					self.board[row][col] = 3 - self.player_just_moved

	def clone(self):
		""" Create a deep clone of this game state.
		"""
		game = Checkers()
		game.player_just_moved = self.player_just_moved
		game.board = [self.board[i][:] for i in range(CHECKERS_BOARD_SIZE)]
		return game

	def _get_moves_south(self, row, col, get_west_moves = True, get_east_moves = True):
		""" Gets moves advancing down the board.
		"""
		moves = []
		south = row + 1
		west = col - 1
		east = col + 1
		if south < CHECKERS_BOARD_SIZE:
			if west >= 0 and get_west_moves:
				if self.board[south][west] == 0 or self.board[row][col] == self.player_just_moved:
					moves.append([(row, col), (south, west)])
				else:
					if south+1 < CHECKERS_BOARD_SIZE and west-1 >= 0:
						if self.board[south][west] in [self.player_just_moved, self.player_just_moved*10] and self.board[south+1][west-1] == 0:
							moves.append([(row, col), (south+1, west-1)])
			if east < CHECKERS_BOARD_SIZE and get_east_moves:
				if self.board[south][east] == 0 or self.board[row][col] == self.player_just_moved:
					moves.append([(row, col), (south, east)])
				else:
					if south+1 < CHECKERS_BOARD_SIZE and east+1 < CHECKERS_BOARD_SIZE:
						if self.board[south][east] in [self.player_just_moved, self.player_just_moved*10] and self.board[south+1][east+1] == 0:
							moves.append([(row, col), (south+1, east+1)])
		return moves

	def _get_moves_north(self, row, col, get_west_moves = True, get_east_moves = True):
		""" Gets moves advancing up the board.
		"""
		moves = []
		north = row - 1
		west = col - 1
		east = col + 1
		if north >= 0:
			if west >= 0 and get_west_moves:
				if self.board[north][west] == 0 or self.board[row][col] == self.player_just_moved:
					moves.append([(row, col), (north, west)])
				else:
					if north-1 >= 0 and west-1 >= 0:
						if self.board[north][west] in [self.player_just_moved, self.player_just_moved*10] and self.board[north-1][west-1] == 0:
							moves.append([(row, col), (north-1, west-1)])
			if east < CHECKERS_BOARD_SIZE and get_east_moves:
				if self.board[north][east] == 0 or self.board[row][col] == self.player_just_moved:
					moves.append([(row, col), (north, east)])
				else:
					if north-1 >=0 and east+1 < CHECKERS_BOARD_SIZE:
						if self.board[north][east] in [self.player_just_moved, self.player_just_moved*10] and self.board[north-1][east+1] == 0:
							moves.append([(row, col), (north-1, east+1)])
		return moves

	def _move_is_capturing(self, move):
		""" Checks whether the move is capturing. Returns boolean.
		"""
		origin = move[0]
		target = move[1]
		delta_x = abs(origin[0] - target[0])
		delta_y = abs(origin[1] - target[1])
		if delta_x> 1 and delta_y > 1:
			return True
		return False

	def _contains_capturing_moves(self, moves):
		""" Checks whether legal moves contain capturing moves. 
			Returns boolean.
		"""
		for move in moves:
			if self._move_is_capturing(move):
				return True
		return False

	def _get_capturing_moves_only(self, moves):
		""" Filters out capturing moves only.
		"""
		capturing_moves_only = []
		for move in moves:
			if self._move_is_capturing(move):
				capturing_moves_only.append(move)
		return capturing_moves_only

	def get_moves(self):
		""" Get all possible moves from this state.
		"""		
		moves = []
		for row in range(CHECKERS_BOARD_SIZE):
			col = 0
			first_piece_found = False
			while col < CHECKERS_BOARD_SIZE:
				# For Kings check moves to both north and south
				# Check pieces that move south and Kings
				if ((self.board[row][col] in self.ai_player_pieces) and self._its_ai_turn()):
					moves_of_current_position = self._get_moves_south(row, col)
					#if it's a king - check for backwards moves too
					if self.board[row][col] == 20:
						moves_of_current_position += self._get_moves_north(row, col)
					if moves_of_current_position != []:
						moves += moves_of_current_position
						first_piece_found = True
				# Check pieces that move north and Kings
				elif ((self.board[row][col] in self.human_player_pieces) and self._its_human_turn()):
					moves_of_current_position = self._get_moves_north(row, col)
					#if it's a king - check for backwards moves too
					if self.board[row][col] == 10:
						moves_of_current_position += self._get_moves_south(row, col)
					if moves_of_current_position != []:
						moves += moves_of_current_position
						first_piece_found = True
				if first_piece_found:
						col += 2
				else: col +=1
		if self._contains_capturing_moves(moves):
			moves = self._get_capturing_moves_only(moves)
		return moves

	def _get_move_direction(self, origin_move, target_move):
		""" Returns Enum with move direction.
		"""
		delta_x = origin_move[0] - target_move[0]
		delta_y = origin_move[1] - target_move[1]
		if delta_x >= 0 and delta_y >= 0:
			return MoveDirection.NORTHWEST
		elif delta_x >= 0 and delta_y < 0:
			return MoveDirection.NORTHEAST
		elif delta_x < 0 and delta_y >= 0:
			return MoveDirection.SOUTHWEST
		elif delta_x < 0 and delta_y < 0:
			return MoveDirection.SOUTHEAST

	def _is_within_range(self, x):
		return True if x >= 0 and x < CHECKERS_BOARD_SIZE else False

	def _get_subsequent_move(self, current_cell):
		""" Returns a subsequent move (a tuple)
		"""
		x = current_cell[0]
		y = current_cell[1]
		directions = [(-2, -2), (-2, +2), (+2, +2), (+2, -2)] #if a piece is a King - check cells in all 4 directions
		if self.player_just_moved == 2 and self.board[x][y] != self.player_just_moved*10: 
			directions = [(+2, +2), (+2, -2)] #if it's AI's piece - check south directions only
		elif self.player_just_moved == 1 and self.board[x][y] != self.player_just_moved*10:
			directions = [(-2, -2), (-2, +2)] #if it's human's piece - check north directions only
		for (dx, dy) in directions:
			if self._is_within_range(x+dx) and self._is_within_range(y+dy):
				if self.board[x+dx][y+dy] == 0:
					if (dx, dy) == (-2, -2):
						if self.board[x-1][y-1] in (3 - self.player_just_moved, (3 - self.player_just_moved*10)):
							return (x+dx,y+dy)
					elif (dx, dy) == (-2, +2):
						if self.board[x-1][y+1] in (3 - self.player_just_moved, (3 - self.player_just_moved)*10):
							return (x+dx, y+dy)
					elif (dx, dy) == (+2, +2):
						if self.board[x+1][y+1] in (3 - self.player_just_moved, (3 - self.player_just_moved)*10):
							return (x+dx, y+dy)
					elif (dx, dy) == (+2, -2):
						if self.board[x+1][y-1] in (3 - self.player_just_moved, (3 - self.player_just_moved)*10):
							return (x+dx, y+dy)
		return None

	def do_move(self, move, move_is_subsequent = False):
		""" Update game board by carrying out the given move.
			If it is not a subsequent move - must update playerJustMoved.
		"""
		piece_became_a_king = False
		origin, target = move[0], move[1]
		if not move_is_subsequent:
			self.player_just_moved = 3 - self.player_just_moved
		piece_is_a_king = self._is_a_king(self.board[origin[0]][origin[1]])
		#if human player piece reached the top of the board - make it a King
		if (self.player_just_moved == 1 and target[0] == 0) or (self.player_just_moved == 2 and target[0] == CHECKERS_BOARD_SIZE-1) or piece_is_a_king:
			self.board[target[0]][target[1]] = self.player_just_moved*10
			piece_became_a_king = True
		else:
			self.board[target[0]][target[1]] = self.player_just_moved
		#update piece count if a move was capturing
		if self._move_is_capturing(move):
			if self.player_just_moved in self.human_player_pieces:
				self.ai_player_pieces_count -=1
			elif self.player_just_moved in self.ai_player_pieces:
				self.human_player_pieces_count -=1
		#remove captured piece
		if move_is_subsequent == True or self._move_is_capturing(move):
			move_direction = self._get_move_direction(origin, target)
			if move_direction == MoveDirection.NORTHWEST:
				self.board[origin[0]-1][origin[1]-1] = 0

			elif move_direction == MoveDirection.NORTHEAST:
				self.board[origin[0]-1][origin[1]+1] = 0

			elif move_direction == MoveDirection.SOUTHWEST:
				self.board[origin[0]+1][origin[1]-1] = 0

			elif move_direction == MoveDirection.SOUTHEAST:
				self.board[origin[0]+1][origin[1]+1] = 0
		#remove piece at old location
		self.board[origin[0]][origin[1]] = 0
		#check if subsequent move is possible
		if self._move_is_capturing(move) and not piece_became_a_king:
			self.board[origin[0]][origin[1]] = 0
			subsequent_move = self._get_subsequent_move(target)
			if subsequent_move is not None:
				self.do_move((target, subsequent_move), move_is_subsequent = True)

	def get_result(self, player_just_moved):
		""" Get the game result from the viewpoint of player who just moved.
		"""
		pjm_pieces = self.human_player_pieces
		opponent_pieces = self.ai_player_pieces
		if self.player_just_moved == 2:
			pjm_pieces = self.ai_player_pieces
			opponent_pieces = self.human_player_pieces
		player_just_moved_count = len([(x,y) for x in range(CHECKERS_BOARD_SIZE) for y in range(CHECKERS_BOARD_SIZE) if self.board[x][y] in pjm_pieces])        
		not_player_just_moved_count = len([(x,y) for x in range(CHECKERS_BOARD_SIZE) for y in range(CHECKERS_BOARD_SIZE) if self.board[x][y] in opponent_pieces])
		if player_just_moved_count > not_player_just_moved_count: return 1.0
		elif player_just_moved_count < not_player_just_moved_count: return 0.0
		else: return 0.5

	def __repr__(self):       
		b = self.board
		s = f"""
			 0   1   2   3   4   5   6   7
		------------------------------------
		0  | {b[0][0]} | {b[0][1]} | {b[0][2]} | {b[0][3]} | {b[0][4]} | {b[0][5]} | {b[0][6]} | {b[0][7]} |
		1  | {b[1][0]} | {b[1][1]} | {b[1][2]} | {b[1][3]} | {b[1][4]} | {b[1][5]} | {b[1][6]} | {b[1][7]} |
		2  | {b[2][0]} | {b[2][1]} | {b[2][2]} | {b[2][3]} | {b[2][4]} | {b[2][5]} | {b[2][6]} | {b[2][7]} |
		3  | {b[3][0]} | {b[3][1]} | {b[3][2]} | {b[3][3]} | {b[3][4]} | {b[3][5]} | {b[3][6]} | {b[3][7]} |
		4  | {b[4][0]} | {b[4][1]} | {b[4][2]} | {b[4][3]} | {b[4][4]} | {b[4][5]} | {b[4][6]} | {b[4][7]} |
		5  | {b[5][0]} | {b[5][1]} | {b[5][2]} | {b[5][3]} | {b[5][4]} | {b[5][5]} | {b[5][6]} | {b[5][7]} |
		6  | {b[6][0]} | {b[6][1]} | {b[6][2]} | {b[6][3]} | {b[6][4]} | {b[6][5]} | {b[6][6]} | {b[6][7]} |
		7  | {b[7][0]} | {b[7][1]} | {b[7][2]} | {b[7][3]} | {b[7][4]} | {b[7][5]} | {b[7][6]} | {b[7][7]} |
		------------------------------------
		"""
		return s

	def back_btn_clicked(self, x, y):
		return True if x in range (340, 377) and y in range(10, 60) else False

	def quit_game_btn_clicked(self, x, y):
		return True if x in range (23, 70) and y in range(10, 90) else False

	def restart_game_btn_clicked(self, x, y):
		return True if x in range (903, 983) and y in range(10, 90) else False

	def sound_btn_clicked(self, x, y):
		return True if x in range(685, 802) and y in range(15, 90) else False

	def game_info_btn_clicked(self, x, y):
		return True if x in range(828, 860) and y in range(10, 90) else False

	def close_game_info_btn_clicked(self, x, y):
		return True if x in range(945, 980) and y in range(15, 80) else False

	def _board_clicked(self, x, y):
		return True if x in range (165, 836) and y in range(121, 800) else False

	def is_game_over(self):
		""" Returns True if there are no more legal moves left or if one of the players lost all pieces.
		"""
		if self.get_moves() == [] or self.ai_player_pieces_count == 0 or self.human_player_pieces_count == 0: return True
		else: return False

	def _is_a_king(self, piece):
		""" Returns True if piece == 10 or 20.
		"""
		return True if piece == (self.player_just_moved * 10) else False

	def _its_ai_turn(self):
		return True if self.player_just_moved == 1 else False

	def _its_human_turn(self):
		return True if self.player_just_moved == 2 else False

	def display_winner(self, screen, game_result, audio_muted):
		""" Displays game winner on screen or a draw. 
		"""
		if not audio_muted:
			CHECKERS_WIN_SOUND.set_volume(0.07)
		pg.mixer.Channel(1).play(CHECKERS_WIN_SOUND)
		if game_result == 0.5:
			screen.blit(CHECKERS_ITS_A_DRAW.convert_alpha(), (0, 0))
		elif (self.player_just_moved == 1 and game_result == 1.0) or (self.player_just_moved == 2 and game_result == 0.0):
			screen.blit(CHECKERS_HUMAN_WON.convert_alpha(), (0, 0))
		elif (self.player_just_moved == 2 and game_result == 1.0) or (self.player_just_moved == 1 and game_result == 0.0):
			screen.blit(CHECKERS_AI_WON.convert_alpha(), (0, 0))
		pg.display.update()

	def display_game_info(self, screen):
		""" Displays information about the game on screen.
		"""
		screen.blit(CHECKERS_GAME_INFO.convert_alpha(), (0, 0))
		pg.display.update()

	def _highlight_available_pieces(self, screen, av_moves):
		""" Highlights pieces that have legal moves
		"""
		if av_moves is not None and av_moves != []:
			cell_width = 83
			offset = 8
			for move in av_moves:
				top_left_coords = self._get_top_left_cell_coords((move[0][0], move[0][1]))
				if self.board[move[0][0]][move[0][1]] == 1:
					screen.blit(CHECKERS_HUMAN_PIECE_ACTIVE.convert_alpha(), top_left_coords)
				elif self.board[move[0][0]][move[0][1]] == 2:
					screen.blit(CHECKERS_AI_PIECE_ACTIVE.convert_alpha(), top_left_coords)
				elif self.board[move[0][0]][move[0][1]] == 10:
					screen.blit(CHECKERS_HUMAN_KING_ACTIVE.convert_alpha(), top_left_coords)
				elif self.board[move[0][0]][move[0][1]] == 20:
					screen.blit(CHECKERS_AI_KING_ACTIVE.convert_alpha(), top_left_coords)
			pg.display.update()

	def _highlight_selected_piece(self, screen, cell):
		""" Highlights the piece on the board which was selected by human player. 
		"""
		if cell is not None:
			cell_width = 83
			offset = 8
			top_left_coords = self._get_top_left_cell_coords((cell[0], cell[1]))
			if self.board[cell[0]][cell[1]] == 1:
				screen.blit(CHECKERS_HUMAN_PIECE_ACTIVE, top_left_coords)
			elif self.board[cell[0]][cell[1]] == 2:
				screen.blit(CHECKERS_AI_PIECE_ACTIVE, top_left_coords)
			elif self.board[cell[0]][cell[1]] == 10:
				screen.blit(CHECKERS_HUMAN_KING_ACTIVE.convert_alpha(), top_left_coords)
			elif self.board[cell[0]][cell[1]] == 20:
				screen.blit(CHECKERS_AI_KING_ACTIVE.convert_alpha(), top_left_coords)
			pg.display.update()

	def _highlight_available_moves(self, screen, piece_selected, moves):
		""" Draws a dot in the middle of a square where the selected piece can move.
		"""
		if piece_selected is not None and moves is not None:
			cell_width = 83
			offset = 8
			for move in moves:
				if move[0] == piece_selected:
					top_left_coords = self._get_top_left_cell_coords((move[1][0], move[1][1]))
					cell_centre = (top_left_coords[0] + cell_width // 2 - offset, top_left_coords[1] + cell_width // 2 - offset)
					screen.blit(CHECKERS_AVAILABLE_MOVE.convert_alpha(), cell_centre)
			pg.display.update()

	def _refresh_sound_btn(self, screen, audio_muted):
		""" Toggles sound on/ sound off button image depending on audio_muted
		"""
		if not audio_muted:
			screen.blit(CHECKERS_SOUND_ON_BTN.convert_alpha(), (SOUND_BTN_LOC_X, SOUND_BTN_LOC_Y))
		else:
			screen.blit(CHECKERS_SOUND_OFF_BTN.convert_alpha(), (SOUND_BTN_LOC_X, SOUND_BTN_LOC_Y))
		pg.display.update()

	def _get_top_left_cell_coords(self, cell):
		x0, y0 = 169, 122
		x1, y1 = 254, 205
		x2, y2 = 338, 289
		x3, y3 = 422, 372
		x4, y4 = 506, 457
		x5, y5 = 590, 541
		x6, y6 = 674, 625
		x7, y7 = 758, 710
		#+82
		#row0: odd
		if cell == (0,1): return (x1, y0)
		elif cell == (0,3): return (x3, y0)
		elif cell == (0,5): return (x5, y0)
		elif cell == (0,7): return (x7, y0)
		#row1: even
		elif cell == (1,0): return (x0, y1)
		elif cell == (1,2): return (x2, y1)
		elif cell == (1,4): return (x4, y1)
		elif cell == (1,6): return (x6, y1)
		#row2
		elif cell == (2,1): return (x1, y2)
		elif cell == (2,3): return (x3, y2)
		elif cell == (2,5): return (x5, y2)
		elif cell == (2,7): return (x7, y2)
		#row3
		elif cell == (3,0): return (x0, y3)
		elif cell == (3,2): return (x2, y3)
		elif cell == (3,4): return (x4, y3)
		elif cell == (3,6): return (x6, y3)
		#row4
		elif cell == (4,1): return (x1, y4)
		elif cell == (4,3): return (x3, y4)
		elif cell == (4,5): return (x5, y4)
		elif cell == (4,7): return (x7, y4)
		#row5
		elif cell == (5,0): return (x0, y5)
		elif cell == (5,2): return (x2, y5)
		elif cell == (5,4): return (x4, y5)
		elif cell == (5,6): return (x6, y5)
		#row6
		elif cell == (6,1): return (x1, y6)
		elif cell == (6,3): return (x3, y6)
		elif cell == (6,5): return (x5, y6)
		elif cell == (6,7): return (x7, y6)
		#row7
		elif cell == (7,0): return (x0, y7)
		elif cell == (7,2): return (x2, y7)
		elif cell == (7,4): return (x4, y7)
		elif cell == (7,6): return (x6, y7)		

	def get_cell_clicked(self, x, y):
		cell = None
		cell_width = 83
		x0, y0 = 168, 120
		x1, y1 = 250, 202
		x2, y2 = 335, 286
		x3, y3 = 418, 370
		x4, y4 = 503, 454
		x5, y5 = 587, 539
		x6, y6 = 671, 623
		x7, y7 = 755, 707
		#row 0
		if x in range(x1, x1+cell_width) and y in range(y0, y0+cell_width):
		   cell = (0,1)
		elif x in range(x3, x3+cell_width) and y in range(y0, y0+cell_width):
			cell = (0,3)
		elif x in range(x5, x5+cell_width) and y in range(y0, y0+cell_width):
			cell = (0,5)
		elif x in range(x7, x7+cell_width) and y in range(y0, y0+cell_width):
			cell = (0,7)
		#row 1
		elif x in range(x0, x0+cell_width) and y in range(y1, y1+cell_width):
			cell = (1,0)
		elif x in range(x2, x2+cell_width) and y in range(y1, y1+cell_width):
			cell = (1,2)
		elif x in range(x4, x4+cell_width) and y in range(y1, y1+cell_width):
			cell = (1,4)
		elif x in range(x6, x6+cell_width) and y in range(y1, y1+cell_width):
			cell = (1,6)
		#row 2
		elif x in range(x1, x1+cell_width) and y in range(y2, y2+cell_width):
			cell = (2,1)
		elif x in range(x3, x3+cell_width) and y in range(y2, y2+cell_width):
			cell = (2,3)
		elif x in range(x5, x5+cell_width) and y in range(y2, y2+cell_width):
			cell = (2,5)
		elif x in range(x7, x7+cell_width) and y in range(y2, y2+cell_width):
			cell = (2,7)
		#row 3
		elif x in range(x0, x0+cell_width) and y in range(y3, y3+cell_width):
			cell = (3,0)
		elif x in range(x2, x2+cell_width) and y in range(y3, y3+cell_width):
			cell = (3,2)
		elif x in range(x4, x4+cell_width) and y in range(y3, y3+cell_width):
			cell = (3,4)
		elif x in range(x6, x6+cell_width) and y in range(y3, y3+cell_width):
			cell = (3,6)
		#row 4
		elif x in range(x1, x1+cell_width) and y in range(y4, y4+cell_width):
			cell = (4,1)
		elif x in range(x3, x3+cell_width) and y in range(y4, y4+cell_width):
			cell = (4,3)
		elif x in range(x5, x5+cell_width) and y in range(y4, y4+cell_width):
			cell = (4,5)
		elif x in range(x7, x7+cell_width) and y in range(y4, y4+cell_width):
			cell = (4,7)
		#row 5
		elif x in range(x0, x0+cell_width) and y in range(y5, y5+cell_width):
			cell = (5,0)
		elif x in range(x2, x2+cell_width) and y in range(y5, y5+cell_width):
			cell = (5,2)
		elif x in range(x4, x4+cell_width) and y in range(y5, y5+cell_width):
			cell = (5,4)
		elif x in range(x6, x6+cell_width) and y in range(y5, y5+cell_width):
			cell = (5,6)
		#row 6
		elif x in range(x1, x1+cell_width) and y in range(y6, y6+cell_width):
			cell = (6,1)
		elif x in range(x3, x3+cell_width) and y in range(y6, y6+cell_width):
			cell = (6,3)
		elif x in range(x5, x5+cell_width) and y in range(y6, y6+cell_width):
			cell = (6,5)
		elif x in range(x7, x7+cell_width) and y in range(y6, y6+cell_width):
			cell = (6,7)
		#row 7
		elif x in range(x0, x0+cell_width) and y in range(y7, y7+cell_width):
			cell = (7,0)
		elif x in range(x2, x2+cell_width) and y in range(y7, y7+cell_width):
			cell = (7,2)
		elif x in range(x4, x4+cell_width) and y in range(y7, y7+cell_width):
			cell = (7,4)
		elif x in range(x6, x6+cell_width) and y in range(y7, y7+cell_width):
			cell = (7,6)
		return cell

	def _display_board_updates(self, screen):
		""" Goes through all pieces on the board and 
			displays the corresponding images on the screen.
		"""
		for row in range(0, CHECKERS_BOARD_SIZE):
			for col in range(0, CHECKERS_BOARD_SIZE):
				coords = self._get_top_left_cell_coords((row, col))
				if coords is not None:
					if self.board[row][col] == 1:
						screen.blit(CHECKERS_HUMAN_PIECE, coords)
					elif self.board[row][col] == 10:
						screen.blit(CHECKERS_HUMAN_KING, coords)
					elif self.board[row][col] == 2:
						screen.blit(CHECKERS_AI_PIECE, coords)
					elif self.board[row][col] == 20:
						screen.blit(CHECKERS_AI_KING, coords)
		pg.display.update()

	def draw_game_screen(self, screen, bgr_img, game_level, audio_muted, set_caption):
		""" Draws Checkers screen and displays board updates.
		"""
		screen = pg.display.set_mode((CHECKERS_SCREEN_WIDTH , CHECKERS_SCREEN_HEIGHT))		
		screen.blit(bgr_img.convert_alpha(), (0, 0))
		if set_caption and game_level is not None:
			caption = f"Checkers Easy: Number of simulations: {CHECKERS_SIMS_PER_MOVE_EASY}"
			if game_level == GameLevels.MEDIUM: caption = f"Checkers Medium: Number of simulations: {CHECKERS_SIMS_PER_MOVE_MEDIUM}"
			elif game_level == GameLevels.HARD: caption = f"Checkers Hard: Number of simulations: {CHECKERS_SIMS_PER_MOVE_HARD}"
			pg.display.set_caption(caption)
		sound_btn = CHECKERS_SOUND_ON_BTN
		if audio_muted: sound_btn = CHECKERS_SOUND_OFF_BTN
		screen.blit(sound_btn.convert_alpha(), (SOUND_BTN_LOC_X, SOUND_BTN_LOC_Y))
		self._display_board_updates(screen)
		screen.blit(eval(f"CHECKERS_{self.human_player_pieces_count}"), (HUM_PIECE_COUNT_LOC_X, PIECE_COUNT_LOC_Y))
		screen.blit(eval(f"CHECKERS_{self.ai_player_pieces_count}"), (AI_PIECE_COUNT_LOC_X, PIECE_COUNT_LOC_Y))
		pg.display.update()

	def main_game_loop(self, screen, game_level):
		#set game audio
		CHECKERS_BGR_MUSIC.set_volume(0.02)
		CHECKERS_AI_THINKING_SOUND.set_volume(0.05)
		CLICK_SOUND.set_volume(0.5)
		pg.mixer.Channel(0).play(CHECKERS_BGR_MUSIC, -1)
		self.draw_game_screen(screen, CHECKERS_HUMAN_TURN, game_level, audio_muted = False, set_caption = True)
		if self.player_just_moved == 2: self._highlight_available_pieces(screen, self.get_moves())
		#set game difficulty
		sims_per_move = CHECKERS_SIMS_PER_MOVE_EASY
		if game_level == GameLevels.MEDIUM: sims_per_move = CHECKERS_SIMS_PER_MOVE_MEDIUM
		elif game_level == GameLevels.HARD: sims_per_move = CHECKERS_SIMS_PER_MOVE_HARD
		run = True
		game_over = False
		clock = pg.time.Clock()
		audio_muted = False
		game_info_visible = False
		piece_selected = None
		current_bgr = CHECKERS_START_SCREEN
		while run:
			clock.tick(FPS)
			for event in pg.event.get():
				if event.type == pg.MOUSEBUTTONDOWN:
					if not audio_muted:	CLICK_SOUND.play()
					mouse_pos = pg.mouse.get_pos()
					x, y = mouse_pos[0], mouse_pos[1]
					if self._board_clicked(x, y) and self.player_just_moved == 2 and not game_over:						
						cell = self.get_cell_clicked(x, y)
						if piece_selected is None:
							moves = self.get_moves()
							for move in moves:
								if cell == move[0]:
									#highlight only selected piece
									self._display_board_updates(screen)
									piece_selected = move[0]
									self._highlight_selected_piece(screen, piece_selected)
									self._highlight_available_moves(screen, piece_selected, moves)
									break
						else:
							if cell == piece_selected:
								#unselect piece
								piece_selected = None
								self.draw_game_screen(screen, current_bgr, game_level, audio_muted, set_caption = False)
								self._highlight_available_pieces(screen, self.get_moves())
								self._highlight_available_moves(screen, piece_selected, moves)
							for move in moves:
								if cell == move[1] and piece_selected is not None:
									# do human move
									self.do_move((piece_selected, cell))
									current_bgr = CHECKERS_AI_TURN
									self.draw_game_screen(screen, current_bgr, game_level, audio_muted, set_caption = False)
									if self.is_game_over():
										self.display_winner(screen, self.get_result(self.player_just_moved), audio_muted)
										self._refresh_sound_btn(screen, audio_muted)
										game_over = True
										break
									piece_selected = None
									if not audio_muted: pg.mixer.Channel(1).play(CHECKERS_AI_THINKING_SOUND)
									#do AI move
									move = UCT.uct(self, sims_per_move)
									self._highlight_available_moves(screen, move[0], [move])
									self._highlight_selected_piece(screen, move[0])
									time.sleep(1)
									self.do_move(move)
									CHECKERS_AI_THINKING_SOUND.stop()
									self.draw_game_screen(screen, current_bgr, game_level, audio_muted, set_caption = False)
									if self.is_game_over():
										self.display_winner(screen, self.get_result(self.player_just_moved), audio_muted)
										self._refresh_sound_btn(screen, audio_muted)
										game_over = True
										break
									else:
										current_bgr = CHECKERS_HUMAN_TURN
										self.draw_game_screen(screen, current_bgr, game_level, audio_muted, set_caption = False)
							if not game_over:
								moves = self.get_moves()
								self._highlight_available_pieces(screen, moves)
								if len(moves) == 1:
									piece_selected = moves[0][0]
									self._highlight_available_moves(screen, piece_selected, moves)
						

					elif self.quit_game_btn_clicked(x, y):
						run = False
						CHECKERS_BGR_MUSIC.stop()
						pg.mixer.Channel(0).play(MAIN_MUSIC_THEME, -1)
						#reset game
						self.board = [[0] * CHECKERS_BOARD_SIZE for x in range(CHECKERS_BOARD_SIZE)]
						for row in range(CHECKERS_BOARD_SIZE):
							start = 0
							if row in [0, 2, 6]: start +=1            
							for col in range(start, CHECKERS_BOARD_SIZE, 2):
								if row in [3, 4]: continue
								elif row < 4: self.board[row][col] = self.player_just_moved
								else: self.board[row][col] = 3 - self.player_just_moved
						self.player_just_moved = 2
						game_over = False
						drew_once = False
						return screen

					elif self.restart_game_btn_clicked(x, y) and not game_info_visible:
						#reset game
						self.board = [[0] * CHECKERS_BOARD_SIZE for x in range(CHECKERS_BOARD_SIZE)]
						for row in range(CHECKERS_BOARD_SIZE):
							start = 0
							if row in [0, 2, 6]: start +=1            
							for col in range(start, CHECKERS_BOARD_SIZE, 2):
								if row in [3, 4]: continue
								elif row < 4: self.board[row][col] = self.player_just_moved
								else: self.board[row][col] = 3 - self.player_just_moved
						self.player_just_moved = 2
						screen.blit(CHECKERS_RESTARTING_GAME.convert_alpha(), (0, 0))
						pg.display.update()
						time.sleep(1)
						self.human_player_pieces_count = 12
						self.ai_player_pieces_count = 12
						self.draw_game_screen(screen, CHECKERS_HUMAN_TURN, game_level, audio_muted, set_caption = False)
						game_info_visible = False
						piece_selected = None
						game_over = False					
						self._highlight_available_pieces(screen, self.get_moves())

					elif self.sound_btn_clicked(x, y):
						if audio_muted:
							audio_muted = False
							pg.mixer.unpause()
						else:
							audio_muted = True
							pg.mixer.pause()
						self._refresh_sound_btn(screen, audio_muted)
						pg.display.update()

					elif self.game_info_btn_clicked(x, y):
						game_info_visible = True
						self.display_game_info(screen)

					elif self.close_game_info_btn_clicked(x, y) and game_info_visible:
						self.draw_game_screen(screen, current_bgr, game_level, audio_muted, set_caption = False)
						if self.player_just_moved == 2: self._highlight_available_pieces(screen, self.get_moves())
						game_info_visible = False
		return screen