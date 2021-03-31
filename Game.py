class Game:
	""" A state of the game, i.e. the game board. These are the only functions which are
		absolutely necessary to implement UCT in any 2-player complete information deterministic
		zero-sum game, although they can be enhanced and made quicker, for example by using a
		get_random_move() function to generate a random move during rollout.
		By convention the players are numbered 1 and 2.
	"""
	def __init__(self):
		self.player_just_moved = 2 # At the root pretend the player just moved is player 2 - player 1 has the first move
		self.board = []

	def clone(self):
		""" Create a deep clone of this game state.
		"""
		game = Game()
		game.player_just_moved = self.player_just_moved
		return game

	def do_move(self, move):
		""" Update a state by carrying out the given move.
			Must update playerJustMoved.
		"""
		self.player_just_moved = 3 - self.player_just_moved
		pass

	def get_moves(self):
		""" Get all possible moves from this state.
		"""
		pass

	def get_result(self, player_just_moved):
		""" Get the game result from the viewpoint of playerjm.
		"""
		pass

	def is_game_over(self):	
		""" Returns True if the last move was a winning one,
		i.e. the game is over
		"""
		pass

	def __repr__(self):
		""" Don't need this - but good style.
		"""
		pass