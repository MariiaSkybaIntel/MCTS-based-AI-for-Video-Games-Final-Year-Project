from math import log, sqrt


class Node:
	"""A node in the game tree. Note win or loss outcome is always calculated from the viewpoint of playerJustMoved.
	"""
	def __init__(self, move = None, parent = None, state = None):
		self.move = move #the move that got us to this node - "None" for the root node
		self.parent_node = parent #"None" for the root node
		self.child_nodes = []
		self.wins = 0
		self.visits = 0
		try:
			self.untried_moves = state.get_moves() #future child nodes
			self.player_just_moved = state.player_just_moved #the only part of the state that the Node needs later
		except ValueError:
			print("The state passed cannot be None")

	def select_child_using_uct_policy(self):
		""" Use the UCB1 formula to select a child node
		"""
		s = sorted(self.child_nodes, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
		#s = sorted(self.child_nodes, key = lambda c: (c.wins/c.visits) + (1 * sqrt((log(self.visits))/c.visits)))[-1]
		return s

	def add_child(self, move, state):
		""" Remove m from untriedMoves and add a new child node for this move.
			Return the added child node
		"""
		n = Node(move = move, parent = self, state = state)
		self.untried_moves.remove(move)
		self.child_nodes.append(n)
		return n

	def update(self, result):
		""" Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
		"""
		self.visits += 1
		self.wins += result

	def __repr__(self):
		return f"[Move: {str(self.move)} Wins/Visits: {str(self.wins)}/{str(self.visits)} Untried: {str(self.untriedMoves)}]"