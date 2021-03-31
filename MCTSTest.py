# LEGACY COMMENT
# This is a very simple implementation of the UCT Monte Carlo Tree Search algorithm in Python 2.7.
# The function UCT(root_state, sims_per_move) is towards the bottom of the code.
# It aims to have the clearest and simplest possible code, and for the sake of clarity, the code
# is orders of magnitude less efficient than it could be made, particularly by using a
# state.GetRandomMove() or state.DoRandomRollout() function.
#
# Example GameState classes for Nim, OXO and Othello are included to give some idea of how you
# can write your own GameState use UCT in your 2-player game. Change the game to be played in
# the UCTPlayGame() function at the bottom of the code.
#
# Written by Peter Cowling, Ed Powley, Daniel Whitehouse (University of York, UK) September 2012.
#
# Licence is granted to freely use and distribute for any sensible/legal purpose so long as this comment
# remains in any distributed code.

import time
import random
import pygame as pg
from enum import Enum
from Node import Node
from UCT import UCT
from config import C4_WIN_SOUND
from OXO import OXO
from Nim import Nim
from Connect4 import Connect4
from Othello import Othello
from Checkers import Checkers

class TestType(Enum):
		RANDOMvsAI = 1
		AIvsRANDOM = 2
		AIvsAI = 3

def _play_game():
	""" Play a sample game between two players (three test_modes are available). 
		Uncomment game and test_type, then set sims_per_move to run tests.
	"""
	game = OXO()
	#game = Nim()
	#game = Connect4()
	#game = Othello()	
	#game = Checkers()
	#test_type = TestType.RANDOMvsAI
	#test_type = TestType.AIvsRANDOM
	test_type = TestType.AIvsAI
	sims_per_move = 1500
	moves = game.get_moves()
	while (moves != []):
		if game.player_just_moved == 2:
			if test_type == TestType.RANDOMvsAI:
				move =  random.choice(moves)
			elif test_type == TestType.AIvsRANDOM or test_type == TestType.AIvsAI:
				move = UCT.uct(game, sims_per_move)
		else:
			if test_type == TestType.RANDOMvsAI or test_type == TestType.AIvsAI:
				move = UCT.uct(game, sims_per_move)
			elif test_type == TestType.AIvsRANDOM:
				move =  random.choice(moves)
					
		game.do_move(move)
		if game.is_game_over():
			break
		moves = game.get_moves()
	game_result = game.get_result(game.player_just_moved)
	
	if (game_result == 1.0 and game.player_just_moved == 1) or (game_result == 0.0 and game.player_just_moved == 2):
		return 1 #player1 won
	elif (game_result == 1.0 and game.player_just_moved == 2) or (game_result == 0.0 and game.player_just_moved == 1):
		return 2 #player2 won
	elif game_result == 0.5:
		return 0.5 # it's a draw

def test_MCTS():
	""" Play n games and print games results summary
	"""
	number_of_games = 500
	t_start = time.time() #start the timer
	P1 = P2 = draw = num_of_games = 0
	while num_of_games < number_of_games:
		game_outcome = _play_game()
		if game_outcome == 1:
			P1 = P1 + 1
		elif game_outcome == 2:
			P2 = P2 + 1
		else:
			draw = draw + 1
		num_of_games = num_of_games + 1
		if num_of_games % 100 == 0:
			print (f"Number of Games: {num_of_games}")
			print (f"Player 1 won: {P1} games")
			print (f"Player 2 won: {P2} games")
			print(f"draws {draw}")
	#stop the timer
	t_end = time.time()
	#print final summary of all games played
	total_time = (t_end-t_start)/60
	print (f"Player 1 won: {P1} games")
	print (f"Player 2 won: {P2} games")
	print(f"draws {draw}")
	print(round(total_time, 2))
	print (P1)
	print (P2)
	print(draw)
	print(f"Total time: {total_time} mins")
	C4_WIN_SOUND.play()

	