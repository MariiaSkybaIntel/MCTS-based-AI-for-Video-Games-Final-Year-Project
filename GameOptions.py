import pygame as pg
from  MCTSTest import *
from config import *
from Checkers import Checkers
from OXOTest import *
from CheckersTest import *
import os

class GameOptions():
	def get_game_mode_selected(x, y):
		if x in range(OXO_GAME_MODES_BTN_MARGIN_LEFT, OXO_GAME_MODES_BTN_MARGIN_RIGHT):
			if y in range(180, 230): return GameModes.HUMANvsHUMAN
			elif y in range(280, 322): return GameModes.HUMANvsAI
			elif y in range(383, 432): return GameModes.AIvsAI
		return None

	def get_game_level_selected(x, y):
		if x in range(GAME_BTNS_MARGIN_LEFT, GAME_BTNS_MARGIN_RIGHT):
			if y in range(180, 230): return GameLevels.EASY
			elif y in range(275, 325): return GameLevels.MEDIUM
			elif y in range(370, 420): return GameLevels.HARD
		return None

	def back_btn_clicked(x, y):
		return True if x in range(10, 45) and y in range(0, 60) else False

	def draw_game_options_screen(screen, game):
		""" Draws game options screen. If game is OXO - will draw game modes.
			For any other games will draw game levels.
		"""
		#define window size and display background
		screen = pg.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))
		caption = "Choose Game Level"
		bgr = GAMES_LEVELS
		if game == Games.OXO:
			bgr = OXO_GAME_MODES
			caption = "Choose Game Mode"
		pg.display.set_caption(caption)
		screen.blit(bgr.convert_alpha(), (0, 0))
		pg.display.update()

	def game_options_main(screen, game):
		assert game is not None
		GameOptions.draw_game_options_screen(screen, game)
		clock = pg.time.Clock()
		run = True
		while run:
			clock.tick(FPS)        
			for event in pg.event.get():
				if event.type == pg.QUIT: run = False
				elif event.type == pg.MOUSEBUTTONDOWN:
					CLICK_SOUND.play()
					xy = pg.mouse.get_pos()
					x, y = xy[0], xy[1]
					if game == Games.OXO:
						game_mode = GameOptions.get_game_mode_selected(x, y)
						if game_mode is not None: screen = OXO().main_game_loop(screen, game_mode)
					else:
						game_level = GameOptions.get_game_level_selected(x, y)
						if game_level is not None:
							if game == Games.NIM: screen = Nim().main_game_loop(screen, game_level)
							elif game == Games.CONNECT4: screen = Connect4().main_game_loop(screen, game_level)
							elif game == Games.OTHELLO: screen = Othello().main_game_loop(screen, game_level)
							else: screen = Checkers().main_game_loop(screen, game_level)
					if GameOptions.back_btn_clicked(x, y):
						run = False
						return screen
					if screen is not None: GameOptions.draw_game_options_screen(screen, game)
			pg.display.update()
		return screen