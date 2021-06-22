import pygame as pg
import time
import numpy as np
import random
from config import *
from Game import Game
from GameGUIInterface import GameGUIInterface
from UCT import UCT

class Nim(Game, GameGUIInterface):
	""" A state of the game Nim. In Nim, players alternately take 1,2 or 3 chips with the
		winner being the player to take the last chip.
	"""
	def __init__(self):
		self.player_just_moved = 2 # At the root pretend the player just moved is p2 - p1 has the first move
		self.bubbles = NIM_DEFAULT_NUM_OF_OBJECTS
		self.board = np.ones((self.bubbles), dtype=int)

	def clone(self):
		""" Create a deep clone of this game state.
		"""
		game = Nim()
		game.bubbles = self.bubbles
		game.board = np.ones((game.bubbles), dtype=int)
		game.player_just_moved = self.player_just_moved
		return game

	def do_move(self, move):
		""" Update a state by carrying out the given move.
			Must update playerJustMoved.
		"""
		if move >= 1 and move <= 3 and self.bubbles > 0:
			self.bubbles -= move
			self.player_just_moved = 3 - self.player_just_moved

	def get_moves(self):
		""" Get all possible moves from this state.
			If game is over return empty list
		"""
		return [] if self.is_game_over() else list(range(1, min([4, self.bubbles + 1])))

	def get_result(self, player_just_moved):
		""" Get the game result from the viewpoint of playerjm.
			1.0 means player_just_moved took the last object and has won
			0.0 means player_just_moved's opponent took the last object and has won
		"""
		if self.bubbles == 0:
			return 1.0 if self.player_just_moved == player_just_moved else 0.0

	def __repr__(self):
		""" Returns string representation of Nim
		"""
		return f"Bubbles: {self.bubbles} Just played: {self.player_just_moved}"

	def is_game_over(self):
		""" Check if there are any more objects left to choose from
		"""
		return True if self.bubbles == 0 else False

	def quit_game_btn_clicked(self, x, y):
		return True if x in range (540, 580) and y in range(10,70) else False

	def restart_game_btn_clicked(self, x, y):
		return True if x in range (10, 70) and y in range(10,70) else False

	def _pop_btn_clicked(self, x, y):
		return True if x in range (10, 200) and y in range(650, 685) else False	
	
	def _undo_btn_clicked(self, x, y):
		return True if x in range (397, 587) and y in range(650, 685) else False	

	def board_clicked(self, x, y):
		return True if x in range(10, 590) and y in range(100, 650) else False

	def sound_btn_clicked(self, x, y):
		return True if x in range(70, 130) and y in range(10, 55) else False

	def game_info_btn_clicked(self, x, y):
		return True if x in range(135, 165) and y in range(10, 55) else False

	def close_game_info_btn_clicked(self, x, y):
		return True if x in range(555, 585) and y in range(6, 55) else False

	def get_cell_clicked(self, x, y):
		#row 0
		if x in range(10,90) and y in range(100, 170): return 0
		elif x in range(110,190) and y in range(100, 170): return 1
		elif x in range(210,290) and y in range(100, 170): return 2
		elif x in range(310,390) and y in range(100, 170): return 3
		elif x in range(410,490) and y in range(100, 170): return 4
		elif x in range(510,590) and y in range(100, 170): return 5
		#row 1
		elif x in range(60,140) and y in range(195, 275): return 6
		elif x in range(160,240) and y in range(195, 275): return 7
		elif x in range(260,340) and y in range(195, 275): return 8
		elif x in range(360,440) and y in range(195, 275): return 9
		elif x in range(460,540) and y in range(195, 275): return 10
		#row 2
		elif x in range(110,190) and y in range(295, 375): return 11
		elif x in range(210,290) and y in range(295, 375): return 12
		elif x in range(310,390) and y in range(295, 375): return 13
		elif x in range(410,490) and y in range(295, 375): return 14
		#row 3
		elif x in range(160,240) and y in range(395, 475): return 15
		elif x in range(260,340) and y in range(395, 475): return 16
		elif x in range(360,440) and y in range(395, 475): return 17
		#row 4
		elif x in range(210,290) and y in range(495, 575): return 18
		elif x in range(310,390) and y in range(495, 575): return 19
		#row 5
		elif x in range(260,340) and y in range(595, 675): return 20
		else: return None

	def _get_bubble_coordinates(self, bubble):
		y_row0 = 95
		y_row1 = 191
		y_row2 = 286
		y_row3 = 380
		y_row4 = 475
		y_row5 = 570
		#row 0
		if bubble == 0: xy = (10, y_row0)
		elif bubble == 1: xy = (110, y_row0)
		elif bubble == 2: xy = (210, y_row0)
		elif bubble == 3: xy = (310, y_row0)
		elif bubble == 4: xy = (410, y_row0)
		elif bubble == 5: xy = (510, y_row0)
		#row 1
		elif bubble == 6: xy = (60, y_row1)
		elif bubble == 7: xy = (160, y_row1)
		elif bubble == 8: xy = (260, y_row1)
		elif bubble == 9: xy = (360, y_row1)
		elif bubble == 10: xy = (460, y_row1)
		#row 2
		elif bubble == 11: xy = (110, y_row2)
		elif bubble == 12: xy = (210, y_row2)
		elif bubble == 13: xy = (310, y_row2)
		elif bubble == 14: xy = (410, y_row2)
		#row 3
		elif bubble == 15: xy = (160, y_row3)
		elif bubble == 16: xy = (260, y_row3)
		elif bubble == 17: xy = (360, y_row3)
		#row 4
		elif bubble == 18: xy = (210, y_row4)
		elif bubble == 19: xy = (310, y_row4)
		#row 5
		elif bubble == 20: xy = (260,  y_row5)
		return xy

	def display_winner(self, screen):
		gameResult = self.get_result(self.player_just_moved)
		#if human player won
		if (self.player_just_moved == 1 and gameResult == 1.0) or (self.player_just_moved == 2 and gameResult == 0.0):
			screen.blit(NIM_YOU_WON_LABEL.convert_alpha(), (75, 130))
		else:
			screen.blit(NIM_AI_WON_LABEL.convert_alpha(), (75, 130))
		NIM_WINNING_SOUND.play()
		pg.display.update()

	def display_game_info(self, screen):
		screen.blit(NIM_GAME_INFO.convert_alpha(), (0, 0))
		pg.display.update()

	def set_window_caption(self, game_level):
		caption = f"Nim Easy: Number of simulations: {NIM_SIMS_PER_MOVE_EASY}"
		if game_level == GameLevels.MEDIUM: caption = f"Nim Medium: Number of simulations: {NIM_SIMS_PER_MOVE_MEDIUM}"
		elif game_level == GameLevels.HARD: caption = f"Nim Hard: Number of simulations: {NIM_SIMS_PER_MOVE_HARD}"
		pg.display.set_caption(caption)

	def draw_game_screen(self, screen, game_level, audio_muted, set_caption):        
		#increase screen size and display background image
		screen = pg.display.set_mode((NIM_SCREEN_WIDTH , NIM_SCREEN_HEIGHT))
		screen.blit(NIM_BACKGROUND_IMG.convert_alpha(), [0, 0])
		if set_caption: self.set_window_caption(game_level)
		#draw buttons
		screen.blit(NIM_BACK_BTN.convert_alpha(),(540,10))
		screen.blit(NIM_RESTART_BTN.convert_alpha(), (10,10))
		if audio_muted: screen.blit(NIM_SOUND_OFF_BTN.convert_alpha(), (70, 10))
		else: screen.blit(NIM_SOUND_ON_BTN.convert_alpha(), (70, 10))
		screen.blit(NIM_GAME_INFO_BTN.convert_alpha(), (135,10))
		screen.blit(NIM_POP_BTN.convert_alpha(), [10,650])
		screen.blit(NIM_UNDO_BTN.convert_alpha(), [395,650])
		#draw bubbles
		horizontal_spacing, vertical_spacing = 100, 95
		row_offset = 50
		x, row_start = 10, 10
		y = 95
		original_bubbles, bubbles_count = 6, 6
		row = 1
		count = 0
		np.zeros((5, 5), dtype=int)
		while row != 7:
			while bubbles_count != 0:
				if self.board[count] == 1: screen.blit(NIM_BUBBLE.convert_alpha(), [x, y])
				elif self.board[count] == 2: screen.blit(NIM_BUBBLE_SELECTED.convert_alpha(), [x, y])
				x += horizontal_spacing
				bubbles_count -= 1
				count +=1
			row_start += row_offset
			x = row_start
			bubbles_count = original_bubbles-row
			y += vertical_spacing
			row += 1
		pg.display.update()

	def main_game_loop(self, screen, game_level):
		pg.display.update()
		self.draw_game_screen(screen, game_level, audio_muted = False, set_caption = True)
		#set game difficulty
		sims_per_move = NIM_SIMS_PER_MOVE_EASY
		if game_level == GameLevels.MEDIUM: sims_per_move = NIM_SIMS_PER_MOVE_MEDIUM
		elif game_level == GameLevels.HARD: sims_per_move = NIM_SIMS_PER_MOVE_HARD
		run = True
		clock = pg.time.Clock()
		game_over = False
		game_info_visible = False
		#set volume for background music and sounds
		NIM_BGR_MUSIC.set_volume(0.1)
		CLICK_SOUND.set_volume(0.3)
		NIM_WINNING_SOUND.set_volume(0.4)
		NIM_BUBBLE_POP_SOUND.set_volume(0.4)
		pg.mixer.Channel(0).play(NIM_BGR_MUSIC, -1)
		selected_bubbles = []
		game_over = False
		audio_muted = False
		while run:
			clock.tick(FPS)
			for event in pg.event.get():
				if event.type == pg.MOUSEBUTTONDOWN:
					if not audio_muted: CLICK_SOUND.play()
					x, y = pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]
					if self.board_clicked(x, y) and self.player_just_moved == 2 and not game_over:
						if np.all(self.board==0): bubble = None #if no more bubbles left							
						else: bubble = self.get_cell_clicked(x, y)
						if bubble is not None and len(selected_bubbles) < 3 and bubble not in selected_bubbles:                            
							screen.blit(NIM_BUBBLE_SELECTED.convert_alpha(), self._get_bubble_coordinates(bubble))
							selected_bubbles.append(bubble)
					elif self._undo_btn_clicked(x, y) and not game_over:
						selected_bubbles = []
						self.draw_game_screen(screen, game_level, audio_muted,  set_caption = False)
					#if human player made a move
					elif self._pop_btn_clicked(x, y) and len(selected_bubbles) in range(1, 4) and not game_over:                        
						#remove bubbles from screen
						for i in selected_bubbles:
							NIM_BUBBLE_POP_SOUND.play()
							time.sleep(0.1)
							self.board[i] = 0                        
						self.do_move(len(selected_bubbles))
						selected_bubbles = []
						self.draw_game_screen(screen, game_level, audio_muted, set_caption = False)
						if self.is_game_over():
							self.display_winner(screen)
							game_over = True
						else:							
							pg.mixer.Channel(1).play(NIM_AI_THINKING_SOUND)
							screen.blit(NIM_AI_THINKING_LABEL.convert_alpha(), [225, 650])
							pg.display.update()
							time.sleep(INTERVAL_BETWEEN_MOVES)
							AImove = UCT.uct(self, sims_per_move)
							NIM_AI_THINKING_SOUND.stop()
							#randomly choose n=AImove bubbles on the screen
							all_bubbles = []
							#get all bubbles displayed on screen
							for i in range(len(self.board)):
								if self.board[i] == 1: all_bubbles.append(i)
							while AImove != 0:
								chosen_bubble = random.choice(all_bubbles)
								if chosen_bubble not in selected_bubbles:
									selected_bubbles.append(chosen_bubble)
									AImove -=1  
							#do AI move
							self.do_move(len(selected_bubbles))
							#remove bubbles from screen
							for i in selected_bubbles:
								NIM_BUBBLE_POP_SOUND.play()
								time.sleep(0.1)
								self.board[i] = 0
							selected_bubbles = []
							all_bubbles = []
							self.draw_game_screen(screen, game_level, audio_muted, set_caption = False)
							if self.is_game_over():
								self.draw_game_screen(screen, game_level, audio_muted, set_caption = False)
								self.display_winner(screen)
								game_over = True
					elif self.restart_game_btn_clicked(x, y):
						screen.fill(BLACK)
						self.bubbles = NIM_DEFAULT_NUM_OF_OBJECTS
						self.player_just_moved = 2
						screen.blit(NIM_RESTARTING_GAME_LABEL.convert_alpha(), [160,300])
						pg.display.update()
						time.sleep(0.5)
						self.board = np.ones((self.bubbles), dtype=int)
						self.draw_game_screen(screen, game_level, audio_muted, set_caption = False)
						selected_bubbles = []                        
						game_over = False
					elif self.sound_btn_clicked(x, y):
						if audio_muted:
							audio_muted = False
							pg.mixer.unpause()
							self.draw_game_screen(screen, game_level, audio_muted, set_caption = False)
							screen.blit(NIM_SOUND_ON_BTN.convert_alpha(), (70, 10))           
						else:
							audio_muted = True
							pg.mixer.pause()
							screen.blit(NIM_SOUND_OFF_BTN.convert_alpha(), (70, 10))
					elif self.game_info_btn_clicked(x, y):
						game_info_visible = True
						self.display_game_info(screen)
					elif self.close_game_info_btn_clicked(x, y) and game_info_visible:
						self.draw_game_screen(screen, game_level, audio_muted, set_caption = False)
						game_info_visible = False
					elif self.quit_game_btn_clicked(x, y) and not game_info_visible:						
						NIM_BGR_MUSIC.stop()
						pg.mixer.Channel(0).play(MAIN_MUSIC_THEME, -1)
						#reset game
						self.bubbles = NIM_DEFAULT_NUM_OF_OBJECTS
						self.player_just_moved = 2
						game_over = False
						run = False
						return screen
				elif event.type == pg.QUIT:
					run = False
			pg.display.update()
		return screen
