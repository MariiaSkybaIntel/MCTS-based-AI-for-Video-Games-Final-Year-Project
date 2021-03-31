Prerequisites:
1. Install Python 3: https://www.python.org/downloads/
2. Install Pygame: pip install pygame
3. Install Numpy: pip install numpy


Folder contents: 
-high_resolution_attachments (UML Use case, class diagrams and other images in higher resolution)
-mcts_games (contains MCTS games.exe file and folder with media required for .exe to work)
-source_code (full source code of the project)


HOW TO PLAY GAMES: 
supporting -> mcts_games -> MCTS games.exe   OR
open source_code folder in ide -> main.py -> uncomment mode = Modes.PLAY (line 62) -> Run



HOW TO RUN MCTS TESTS:
1. MCTSTest.py (lines 39-46) -> uncomment desired game and test_type 
							 -> set number of simulations (line 47)
							 -> set number of games (line 77) 
2. main.py (line 63) -> uncomment mode = Modes.TEST_MCTS -> Run



HOW TO RUN UNIT TESTS:
main.py (line 64) -> uncomment mode = Modes.TEST_MCTS -> Run