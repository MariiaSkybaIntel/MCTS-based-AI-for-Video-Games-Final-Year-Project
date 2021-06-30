# MCTS-based-AI-for-Video-Games - CSSE course Final Year Project

MCTS belongs to the family of search algorithms used in the Artificial Intelligence domain of Computer Science. It uses Monte Carlo simulations to find optimal actions by drawing random samples from the decision space and can be used for any problem that can be modelled as {state: action} set of pairs. 

In Reinforcement Learning an intelligent agent is always trying to expand tree nodes which look promising for finding a solution. However, it is not guaranteed that the current best node is the optimal node and occasionally exploring new nodes is as important as expanding (exploiting) good ones.

## Motivation
- Efficiency. MCTS doesn't require a heuristic function which may be time-consuming to develop.
- Universality. Implementing a game’s mechanics is sufficient for MCTS to be able to explore the search space.
- Asymmetric tree growth.
- MCTS can be stopped anytime to return the best move.

## MCTS steps

<img src= "https://github.com/cmulation/MCTS-for-Video-Games-Final-Year-Project/blob/main/MCTS_steps.jpg" width="700" height="400"/>

## Prerequisites:
1. Install Python 3: https://www.python.org/downloads/
2. Install Pygame: pip install pygame
3. Install Numpy: pip install numpy


## To play games:
A selection of 5 games was developed for this project: OXO, Nim, Connect4, Othello and Checkers. Each game has an info button where you can get familiar with the rules.

To play:

supporting -> mcts_games -> MCTS games.exe   OR
main.py (line 62) -> uncomment mode = Modes.PLAY  -> Run


## To run MCTS tests:
Testing was done to measure MCTS-based AI performance. These tests can be run the following way:
1. MCTSTest.py (lines 39-46) -> uncomment desired game and test_type 
							 -> set number of simulations (line 47)
							 -> set number of games (line 77) 
2. main.py (line 63) -> uncomment mode = Modes.TEST_MCTS -> Run

## To run unit tests:
main.py (line 64) -> uncomment mode = Modes.TEST_MCTS -> Run

## Games GUI
<img src= "https://github.com/cmulation/MCTS-for-Video-Games-Final-Year-Project/blob/main/GUI_examples/main.jpg" width="400" height="630"/>
<img src= "https://github.com/cmulation/MCTS-for-Video-Games-Final-Year-Project/blob/main/GUI_examples/oxo.jpg" width="400" height="625"/>
<img src= "https://github.com/cmulation/MCTS-for-Video-Games-Final-Year-Project/blob/main/GUI_examples/nim.jpg" width="600" height="730"/>
<img src= "https://github.com/cmulation/MCTS-for-Video-Games-Final-Year-Project/blob/main/GUI_examples/c4.jpg" width="600" height="680"/>
<img src= "https://github.com/cmulation/MCTS-for-Video-Games-Final-Year-Project/blob/main/GUI_examples/othello.jpg" width="600" height="830"/>
<img src= "https://github.com/cmulation/MCTS-for-Video-Games-Final-Year-Project/blob/main/GUI_examples/checkers.jpg" width="1000" height="825"/>

