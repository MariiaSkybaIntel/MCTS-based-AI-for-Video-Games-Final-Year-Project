import pygame as pg
import time
from config import *
from Game import Game
from GameGUIInterface import GameGUIInterface
from UCT import UCT


class OXO(Game, GameGUIInterface):
	""" A state of the game, i.e. the game board.
		Squares in the board are in this arrangement
		012
		345
		678
		where 0 = empty, 1 = player 1 (X), 2 = player 2 (O)
	"""
	def __init__(self):
		self.player_just_moved = 2 # At the root pretend the player just moved is p2 - p1 has the first move
		self.board = [0,0,0,0,0,0,0,0,0]

	def clone(self):
		""" Create a deep clone of this game state.
		"""
		state = OXO()
		state.player_just_moved = self.player_just_moved
		state.board = self.board[:]
		return state

	def do_move(self, move):
		""" Update a state by carrying out the given move.
			Must update playerJustMoved.
		"""
		if move >= 0 and move <= 8 and move == int(move) and self.board[move] == 0:
			self.player_just_moved = 3 - self.player_just_moved
			self.board[move] = self.player_just_moved

	def is_game_over(self):
		""" Returns True if all cells are taken or one of the players made a line
		"""
		if all(self.board):	return True # if all cells are taken
		for (x,y,z) in [(3,4,5),(0,1,2),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
			if self.board[x] == self.board[y] == self.board[z] and self.board[x] != 0:
				return True
		return False

	def get_moves(self):
		""" Get all possible moves from this state.
		"""
		return [] if self.is_game_over() else [i for i in range(9) if self.board[i] == 0]

	def get_result(self, player_just_moved):
		""" Get the game result from the viewpoint of playerjm.
		"""
		for (x,y,z) in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
			if self.board[x] == self.board[y] == self.board[z] !=0:
				return 1.0 if self.board[x] == player_just_moved else 0.0
		if self.get_moves() == []: return 0.5 # draw

	def __repr__(self):
		s= ""
		for i in range(9):
			s += ".XO"[self.board[i]]
			if i % 3 == 2: s += "\n"
		return s

	def quit_game_btn_clicked(self, x, y):
		return True if x in range (8, 40) and y in range(10, 56) else False

	def restart_game_btn_clicked(self, x, y):
		return True if x in range (312, 350) and y in range(5, 45) else False

	def board_clicked(self, x, y):
		return True if x in range (50, 350) and y in range(250,550)else  False

	def sound_btn_clicked(self, x, y):
		return True if x in range (205, 298) and y in range(5, 45) else False	

	def _start_ai_game_btn_clicked(self, x, y):
		return True if x in range (155, 255) and y in range(200, 250) else False

	def game_info_btn_clicked(self, x, y):
		return True if x in range (365, 395) and y in range(5, 45) else False

	def close_game_info_btn_clicked(self, x, y):
	   return True if x in range (363, 395) and y in range(0, 45) else False

	def display_game_info(self, screen, game_mode):
		game_info = OXO_HUM_VS_HUM_GAME_INFO
		if game_mode == GameModes.HUMANvsAI: game_info = OXO_HUM_VS_AI_GAME_INFO
		elif game_mode == GameModes.AIvsAI: game_info = OXO_AI_VS_AI_GAME_INFO
		screen.blit(game_info.convert_alpha(), (0, 0))
		pg.display.update()

	def _get_win_line(self):
		""" Get the winning line
		"""
		if self.board[0] == self.board[1] == self.board[2] !=0:
			return OXOWinLine.HORIZONTAL1
		elif self.board[3] == self.board[4] == self.board[5] !=0:
			return OXOWinLine.HORIZONTAL2
		elif self.board[6] == self.board[7] == self.board[8] !=0:
			return OXOWinLine.HORIZONTAL3
		elif self.board[0] == self.board[3] == self.board[6] !=0:
			return OXOWinLine.VERTICAL1
		elif self.board[1] == self.board[4] == self.board[7] !=0:
			return OXOWinLine.VERTICAL2
		elif self.board[2] == self.board[5] == self.board[8] !=0:
			return OXOWinLine.VERTICAL3
		elif self.board[0] == self.board[4] == self.board[8] !=0:
			return OXOWinLine.DIAGONAL1
		elif self.board[2] == self.board[4] == self.board[6] !=0:
			return OXOWinLine.DIAGONAL2
		else: return None #else - it's a draw

	def _display_win_line(self, screen, win_line):
		if win_line is not None:
			if win_line == OXOWinLine.HORIZONTAL1:
				screen.blit(OXO_BLACK_LINE.convert_alpha(), (55, 290))
			elif win_line == OXOWinLine.HORIZONTAL2:
				screen.blit(OXO_BLACK_LINE.convert_alpha(), (55, 390))
			elif win_line == OXOWinLine.HORIZONTAL3:
				screen.blit(OXO_BLACK_LINE.convert_alpha(), (55, 490))
			elif win_line == OXOWinLine.VERTICAL1:
				screen.blit(pg.transform.rotate(OXO_BLACK_LINE.convert_alpha(), 90), (90, 260))
			elif win_line == OXOWinLine.VERTICAL2:
				screen.blit(pg.transform.rotate(OXO_BLACK_LINE.convert_alpha(), 90), (190, 260))
			elif win_line == OXOWinLine.VERTICAL3:
				screen.blit(pg.transform.rotate(OXO_BLACK_LINE.convert_alpha(), 90), (290, 260))
			elif win_line == OXOWinLine.DIAGONAL1:
				screen.blit(pg.transform.rotate(pg.transform.scale(OXO_BLACK_LINE.convert_alpha(), (420, 15)), -45), (60, 255))
			elif win_line == OXOWinLine.DIAGONAL2:
				screen.blit(pg.transform.rotate(pg.transform.scale(OXO_BLACK_LINE.convert_alpha(), (420, 15)), 45), (45, 245))
			pg.display.update()

	def _display_move(self, screen, x, y, symbol, move=None):
		assert move is not None
		if x in range(52, 147) and y in range(253, 348) or move == 0:
			x, y = 54, 255
		elif x in range(153, 248) and y in range(252, 348) or move == 1:
			x, y = 155, 255
		elif x in range(253, 348) and y in range(253, 348) or move == 2:
			x, y = 254, 255
		elif x in range(52, 148) and y in range(354, 447) or move == 3:
			x, y = 54, 356
		elif x in range(153, 248) and y in range(354, 447) or move == 4:
			x, y = 155, 356
		elif x in range(253, 348) and y in range(354, 447) or move == 5:
			x, y = 255, 356
		elif x in range(52, 148) and y in range(455, 547) or move == 6:
			x, y = 54, 456
		elif x in range(153, 248) and y in range(455, 547) or move == 7:
			x, y = 155, 456
		elif x in range(253, 348) and y in range(455, 547) or move == 8:
			x, y = 255, 456        
		screen.blit(symbol, [x, y])
		pg.display.update()		

	def display_winner(self, screen, game_mode, audio_muted):
		OXO_WIN_SOUND.set_volume(0.1)
		OXO_WIN_SOUND.play()
		win_line = self._get_win_line()
		#display game results depending on the game mode
		game_screen = None
		game_result_image = OXO_ITS_A_DRAW
		if game_mode == GameModes.HUMANvsHUMAN:
			if win_line is None:	game_screen = OXO_HUM_VS_HUM_START_SCREEN
			elif self.player_just_moved == 1:
				game_screen = OXO_HUM_VS_HUM_PLAYER1_TURN
				game_result_image = OXO_HUM_VS_HUM_PLAYER1_WON
			else:
				game_screen = OXO_HUM_VS_HUM_PLAYER2_TURN
				game_result_image = OXO_HUM_VS_HUM_PLAYER2_WON
		elif game_mode == GameModes.HUMANvsAI:
			if win_line is None:	game_screen = OXO_HUM_VS_AI_START_SCREEN
			elif self.player_just_moved == 1:
				game_screen = OXO_HUM_VS_AI_HUMAN_TURN
				game_result_image = OXO_HUM_VS_AI_HUMAN_WON
			else:
				game_screen = OXO_HUM_VS_AI_AI_TURN
				game_result_image = OXO_AI_WON
		else:
			if win_line is None:	game_screen = OXO_AI_VS_AI_START_SCREEN
			else:
				if self.player_just_moved == 1:	game_screen = OXO_AI_VS_AI_AI1_TURN
				else: game_screen = OXO_AI_VS_AI_AI2_TURN
				game_result_image = OXO_AI_WON
		dark_mode = True
		self.draw_game_screen(screen, game_screen, game_mode, audio_muted, dark_mode, start_of_game = False)
		self._display_win_line(screen, win_line)
		screen.blit(game_result_image.convert_alpha(), (0, 0))
		self._display_sound_btn(screen, audio_muted, dark_mode)
		pg.display.update()

	def get_cell_clicked(self, screen, x, y):
		cell = None
		if x in range(52, 147) and y in range(253, 348) and self.board[0] == 0: cell = 0
		elif x in range(153, 248) and y in range(252, 348) and self.board[1] == 0: cell = 1
		elif x in range(253, 348) and y in range(253, 348) and self.board[2] == 0: cell = 2
		elif x in range(52, 148) and y in range(354, 447) and self.board[3] == 0: cell = 3
		elif x in range(153, 248) and y in range(354, 447) and self.board[4] == 0: cell = 4
		elif x in range(253, 348) and y in range(354, 447) and self.board[5] == 0: cell = 5
		elif x in range(52, 148) and y in range(455, 547) and self.board[6] == 0: cell = 6
		elif x in range(153, 248) and y in range(455, 547) and self.board[7] == 0: cell = 7
		elif x in range(253, 348) and y in range(455, 547) and self.board[8] == 0: cell = 8
		return cell

	def _display_sound_btn(self, screen, audio_muted, dark_mode):
		if not audio_muted:
			if not dark_mode: screen.blit(OXO_SOUND_ON_BTN.convert_alpha(), (OXO_SOUND_BTN_LOC_X, OXO_SOUND_BTN_LOC_Y))
			else: screen.blit(OXO_SOUND_ON_BTN.convert_alpha(), (OXO_SOUND_BTN_LOC_X, OXO_SOUND_BTN_LOC_Y))
		else:
			if not dark_mode: screen.blit(OXO_SOUND_OFF_BTN.convert_alpha(), (OXO_SOUND_BTN_LOC_X, OXO_SOUND_BTN_LOC_Y))
			else: screen.blit(OXO_SOUND_OFF_BTN.convert_alpha(), (OXO_SOUND_BTN_LOC_X, OXO_SOUND_BTN_LOC_Y+1))
		pg.display.update()

	def draw_oxo_board(self, screen):
		#draw 3x3 board        
		for row in range(3):
			for col in range(3):
				pg.draw.rect(screen, TEAL, (row*OXO_SQUARE_SIZE+50, col*OXO_SQUARE_SIZE+250, OXO_SQUARE_SIZE, OXO_SQUARE_SIZE), 3)
		#populate the board
		for i in range(0, len(self.board)):
			if self.board[i] == 1:
				self._display_move(screen, -1, -1, OXO_X_SYMBOL, move=i)
			elif self.board[i] == 2:
				self._display_move(screen, -1, -1, OXO_O_SYMBOL, move=i)
		pg.display.update()

	def draw_game_screen(self, screen, bgr_image, game_mode, audio_muted, dark_mode, start_of_game):
		if game_mode == GameModes.HUMANvsHUMAN:
			if start_of_game or bgr_image == None: 
				pg.display.set_caption('OXO: Human vs Human')
				bgr_image = OXO_HUM_VS_HUM_PLAYER1_TURN
		elif game_mode == GameModes.HUMANvsAI:
			if start_of_game or bgr_image == None:
				pg.display.set_caption(f'OXO: Human vs AI. Simulations: {OXO_DEFAULT_SIMS_PER_MOVE}')
				bgr_image = OXO_HUM_VS_AI_HUMAN_TURN
		else:
			if start_of_game or bgr_image == None: 
				pg.display.set_caption(f'OXO: AI vs AI. Simulations: {OXO_DEFAULT_SIMS_PER_MOVE}')
				bgr_image = OXO_AI_VS_AI_START_SCREEN
		screen.blit(bgr_image.convert_alpha(), (0, 0))
		self.draw_oxo_board(screen)
		self._display_sound_btn(screen, audio_muted, dark_mode)
		pg.display.update()

	def main_game_loop(self, screen, game_mode):
		audio_muted = False
		dark_mode = False
		current_bgr_image = OXO_HUM_VS_HUM_PLAYER1_TURN
		if game_mode == GameModes.HUMANvsAI:
			current_bgr_image = OXO_HUM_VS_AI_HUMAN_TURN
		elif game_mode == GameModes.AIvsAI:
			current_bgr_image = OXO_AI_VS_AI_START_SCREEN
		self.draw_game_screen(screen, current_bgr_image, game_mode, audio_muted, dark_mode, start_of_game = True)
		#set game audio
		OXO_BGR_MUSIC.set_volume(0.1)
		OXO_AI_THINKING_SOUND.set_volume(0.05)
		if not audio_muted: pg.mixer.Channel(0).play(OXO_BGR_MUSIC, -1)
		clock = pg.time.Clock()
		run = True		
		game_info_visible = False
		game_over = False
		start_ai_vs_ai_game_clicked = False
		
		while run:
			clock.tick(FPS)
			if game_mode == GameModes.AIvsAI and not game_over and run and start_ai_vs_ai_game_clicked:
				if self.player_just_moved == 2: current_bgr_image = OXO_AI_VS_AI_AI1_TURN
				else: current_bgr_image = OXO_AI_VS_AI_AI2_TURN
				self.draw_game_screen(screen, current_bgr_image, game_mode, audio_muted, dark_mode, start_of_game = False)
				pg.mixer.Channel(1).play(OXO_AI_THINKING_SOUND)
				ai_move = UCT.uct(root_state = self, sims_per_move = OXO_DEFAULT_SIMS_PER_MOVE)
				self.do_move(ai_move)
				if self.player_just_moved == 1: self._display_move(screen, -1, -1, OXO_X_SYMBOL.convert_alpha(), ai_move)
				else: self._display_move(screen, -1, -1, OXO_O_SYMBOL.convert_alpha(), ai_move)
				OXO_AI_THINKING_SOUND.stop()
				if self.is_game_over():
					game_over = True
					dark_mode = True
					self.display_winner(screen, game_mode, audio_muted)
				else: time.sleep(INTERVAL_BETWEEN_MOVES) # Pause between moves so the user is able observe the game

			for event in pg.event.get():
				if event.type == pg.MOUSEBUTTONDOWN:
					CLICK_SOUND.play()
					x, y = pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]
					if self.board_clicked(x, y) and not game_over and not game_info_visible:
						move = self.get_cell_clicked(screen, x, y)
						if move is not None:
							if game_mode == GameModes.HUMANvsHUMAN and not game_over:					
								self.do_move(move)
								if self.player_just_moved == 1: current_bgr_image = OXO_HUM_VS_HUM_PLAYER2_TURN								
								else: current_bgr_image = OXO_HUM_VS_HUM_PLAYER1_TURN
								self.draw_game_screen(screen, current_bgr_image, game_mode, audio_muted, dark_mode, start_of_game = False)
								if self.is_game_over():
									game_over = True
									dark_mode = True
									self.display_winner(screen, game_mode, audio_muted)						
							elif game_mode == GameModes.HUMANvsAI and not game_over:
								self.do_move(move)
								self._display_move(screen, x, y, OXO_X_SYMBOL.convert_alpha(), move)								
								if self.is_game_over():
									game_over = True
									dark_mode = True
									self.display_winner(screen, game_mode, audio_muted)
								if not game_over:
									current_bgr_image = OXO_HUM_VS_AI_AI_TURN
									self.draw_game_screen(screen, current_bgr_image, game_mode, audio_muted, dark_mode, start_of_game = False)
									pg.mixer.Channel(1).play(OXO_AI_THINKING_SOUND)
									ai_move = UCT.uct(root_state = self, sims_per_move = OXO_DEFAULT_SIMS_PER_MOVE)
									OXO_AI_THINKING_SOUND.stop()
									self.do_move(ai_move)
									self._display_move(screen, -1, -1, OXO_O_SYMBOL.convert_alpha(), ai_move)
									if self.is_game_over():
										game_over = True
										dark_mode = True
										self.display_winner(screen, game_mode, audio_muted)
										break
									current_bgr_image = OXO_HUM_VS_AI_HUMAN_TURN
									self.draw_game_screen(screen, current_bgr_image, game_mode, audio_muted, dark_mode, start_of_game = False)

					elif self.quit_game_btn_clicked(x, y) and not game_info_visible:
						self.board = [0,0,0,0,0,0,0,0,0]
						self.player_just_moved = 2
						run = False
						OXO_BGR_MUSIC.stop()
						pg.mixer.Channel(0).play(MAIN_MUSIC_THEME, -1)
						start_ai_vs_ai_game_clicked = False
						game_over = False
						return screen

					elif self.restart_game_btn_clicked(x, y):
						self.board = [0,0,0,0,0,0,0,0,0]
						self.player_just_moved = 2
						screen.blit(OXO_RESTARTING_GAME.convert_alpha(), (0, 0))
						pg.display.update()
						time.sleep(0.5)
						self.draw_game_screen(screen, None, game_mode, audio_muted, dark_mode, start_of_game = True)
						start_ai_vs_ai_game_clicked = False
						game_over = False

					elif self.sound_btn_clicked(x, y):
						if audio_muted:
							audio_muted = False
							pg.mixer.unpause()
							#pg.mixer.Channel(0).play(OXO_BGR_MUSIC, -1)
							#pg.mixer.unpause()
							if dark_mode: screen.blit(OXO_SOUND_ON_BTN_DARK, (OXO_SOUND_BTN_LOC_X, OXO_SOUND_BTN_LOC_Y))
							else:
								#self.draw_oxo_screen(screen, current_bgr_image, game_mode, audio_muted, dark_mode, start_of_game = False)
								screen.blit(OXO_SOUND_ON_BTN, (OXO_SOUND_BTN_LOC_X, OXO_SOUND_BTN_LOC_Y))
						else:
							audio_muted = True
							pg.mixer.pause()
							if dark_mode: screen.blit(OXO_SOUND_OFF_BTN_DARK, (OXO_SOUND_BTN_LOC_X, OXO_SOUND_BTN_LOC_Y))
							else: screen.blit(OXO_SOUND_OFF_BTN, (OXO_SOUND_BTN_LOC_X, OXO_SOUND_BTN_LOC_Y))

					elif self.game_info_btn_clicked(x, y) and not game_info_visible:
						if not game_info_visible:
							dark_mode = True
							self.display_game_info(screen, game_mode)
							game_info_visible = True

					elif self.close_game_info_btn_clicked(x, y) and game_info_visible:
						dark_mode = False
						self.draw_game_screen(screen, current_bgr_image, game_mode, audio_muted, dark_mode, start_of_game = False)
						game_info_visible = False
						

					elif self._start_ai_game_btn_clicked(x, y):
						start_ai_vs_ai_game_clicked = True

				elif event.type == pg.QUIT:
					run = False
			pg.display.update()
		return screen