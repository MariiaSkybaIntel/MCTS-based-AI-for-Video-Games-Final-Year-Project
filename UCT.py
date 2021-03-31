from math import *
import time
import random
from Node import Node


class UCT:

    def uct(root_state, sims_per_move):
        """ Conduct a UCT search for sims_per_move iterations starting from root_state.
            Return the best move from the root_state.
            Assumes 2 alternating players (player 1 starts), with game results in the set (0.0, 0.5, 1.0).
        """
        root_node = Node(state = root_state)
        for i in range(sims_per_move):
            node = root_node
            state = root_state.clone()

            # Select
            while node.untried_moves == [] and node.child_nodes != []: # node is fully expanded and non-terminal
                node = node.select_child_using_uct_policy()
                state.do_move(node.move)

            # Expand
            if node.untried_moves != []: # if we can expand (i.e. state/node is non-terminal - there are moves left)
                move = random.choice(node.untried_moves)
                state.do_move(move)
                node = node.add_child(move, state) # add child and descend tree
        
            # Simulate
            moves = state.get_moves()
            while moves != []: # while state is non-terminal
                state.do_move(random.choice(moves))
                moves = state.get_moves()

            # Backpropagate
            while node != None: # backpropagate from the expanded node and work back to the root node
                node.update(state.get_result(node.player_just_moved))
                node = node.parent_node

        return sorted(root_node.child_nodes, key = lambda c: c.visits)[-1].move    