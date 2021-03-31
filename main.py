import pygame as pg
import os
from  MCTSTest import *
from config import *
from GameOptions import *


def draw_main_screen(screen = None):
	""" Creates main screen with games available
	"""
	#define main window settings and background
	mainScreen = pg.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))    
	if screen is not None: mainScreen = screen
	pg.display.set_caption('MCTS Games')
	mainScreen.blit(GAMES_BGR.convert_alpha(), [0, 0])
	return mainScreen

def play():
	main_screen = draw_main_screen()
	MAIN_MUSIC_THEME.set_volume(0.03)
	pg.mixer.Channel(0).play(MAIN_MUSIC_THEME, -1)
	clock = pg.time.Clock()
	run = True
	game = None
	while run:        
		clock.tick(FPS) #run the clock at a predefined FPS rate        
		for event in pg.event.get():
			if event.type == pg.QUIT: run = False
			if event.type == pg.MOUSEBUTTONDOWN:
				screen = None
				xy = pg.mouse.get_pos()
				x, y = xy[0], xy[1]
				if x in range (GAME_BTNS_MARGIN_LEFT, GAME_BTNS_MARGIN_RIGHT):
					if y in range(85, 135):	
						game = Games.OXO
					elif y in range(180, 230): 
						game = Games.NIM
					elif y in range(275, 325): 
						game = Games.CONNECT4
					elif y in range(370, 420): 
						game = Games.OTHELLO
					elif y in range(463, 515): 
						game = Games.CHECKERS
					else: print()
					if game is not None:
						screen = GameOptions.game_options_main(main_screen, game)
				if screen is not None: draw_main_screen(screen)
		pg.display.update()
	pg.quit()

def run_all_unit_tests_in_cmd():
	os.system('cmd /c "python -m unittest OXOTest.py"')
	os.system('cmd /c "python -m unittest NimTest.py"')
	os.system('cmd /c "python -m unittest Connect4Test.py"')
	os.system('cmd /c "python -m unittest OthelloTest.py"')	
	os.system('cmd /c "python -m unittest CheckersTest.py"')


if __name__ == "__main__":
	""" Uncomment mode to play a game, test MCTS or run unit tests for all games
	"""
	mode = Modes.PLAY
	#mode = Modes.TEST_MCTS
	#mode = Modes.RUN_UNIT_TESTS

	if mode == Modes.TEST_MCTS:       
		test_MCTS()
	elif mode == Modes.RUN_UNIT_TESTS:
		run_all_unit_tests_in_cmd()
	else:
		play()