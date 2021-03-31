import abc

class GameGUIInterface(metaclass=abc.ABCMeta):
	""" Includes all methods required for creating GUI for games
	"""
	@abc.abstractmethod
	def quit_game_btn_clicked(x, y):
		""" Checks if Quit game button was clicked.
			Returns boolean.
		"""
		pass

	@abc.abstractmethod
	def restart_game_btn_clicked(x, y):
		""" Checks if Restart game button was clicked.
			Returns boolean.
		"""
		pass

	@abc.abstractmethod
	def sound_btn_clicked(x, y):
		""" Checks if Sound button was clicked.
			Returns boolean.
		"""
		pass

	@abc.abstractmethod
	def game_info_btn_clicked(x, y):
		""" Checks if Game Info button was clicked.
			Returns boolean.
		"""
		pass

	@abc.abstractmethod
	def close_game_info_btn_clicked(x, y):
		""" Checks if Close Game Info button was clicked.
			Returns boolean.
		"""
		pass

	@abc.abstractmethod
	def display_game_info(screen):
		""" Displays game info depending on the game and game mode chosen.
			Returns None.
		"""
		pass

	@abc.abstractmethod
	def display_winner(screen, audio_muted):
		""" Displays who is game winner on the screen.
			Returns None.
		"""
		pass

	@abc.abstractmethod
	def get_cell_clicked(x, y):
		""" Gets the cell clicked on the board given the mouse click coordinates.
			Returns an int or a tuple (row, col)
		"""
		pass
