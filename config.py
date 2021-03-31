import pygame as pg
from enum import Enum

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEAL = (18, 173, 176)
DTEAL = (64, 87, 92)
PINK = (255, 20, 99)
PURPLE = (97, 82, 156)

#common settings
FPS = 60
DEFAULT_WIDTH, DEFAULT_HEIGHT = 400, 600
GAME_BTNS_MARGIN_LEFT = 78
GAME_BTNS_MARGIN_RIGHT = 323
FONT = 'Arial MT'
DEFAULT_SIMS_PER_MOVE = 1500
INTERVAL_BETWEEN_MOVES = 1 #in seconds (for demonstrating OXO AI vs AI play)
AVATAR_SIZE = 120

#set up fonts
pg.font.init()
MAIN_FONT = pg.font.SysFont(FONT, 25)
SCREEN_MSG_FONT = pg.font.SysFont(FONT, 35, True)

#common images
GAMES_BGR = pg.image.load("./media/games.png")
GAMES_LEVELS = pg.image.load("./media/game-levels.png")
#common labels
AI_THINKING_LABEL = MAIN_FONT.render('THINKING...', True, PINK)
YOU_WON_LABEL = SCREEN_MSG_FONT.render("YOU WON!", True, PINK)
AI_WON_LABEL = SCREEN_MSG_FONT.render("AI WON!", True, PINK)
ITS_A_DRAW_LABEL = SCREEN_MSG_FONT.render("IT'S A DRAW!", True, PINK)
RESTARTING_GAME_LABEL = SCREEN_MSG_FONT.render("RESTARTING GAME...", True, DTEAL)
#common audio
pg.mixer.init() #for playing audio
MAIN_MUSIC_THEME = pg.mixer.Sound("./media/main-music-theme-8-Bit-Menu-David-Renda.wav")
CLICK_SOUND = pg.mixer.Sound("./media/click-sound.wav")
#enums
#oxo game modes
class GameModes(Enum):
	HUMANvsHUMAN = 1
	HUMANvsAI = 2
	AIvsAI = 3

class GameLevels(Enum):
	EASY = 1
	MEDIUM = 2
	HARD = 3

class Games(Enum):
	OXO = 1
	NIM = 2
	CONNECT4 = 3
	OTHELLO = 4
	CHECKERS = 5

class Modes(Enum):
	PLAY = 1
	TEST_MCTS = 2
	RUN_UNIT_TESTS = 3



#---CHECKERS---#
CHECKERS_SIMS_PER_MOVE_EASY = 10
CHECKERS_SIMS_PER_MOVE_MEDIUM = 500
CHECKERS_SIMS_PER_MOVE_HARD = 700
#screen settings
CHECKERS_BOARD_SIZE = 8
CHECKERS_SCREEN_WIDTH = 1000
CHECKERS_SCREEN_HEIGHT = 789
CHECKERS_PIECE_DIAMETER = 75
SOUND_BTN_LOC_X = 683
SOUND_BTN_LOC_Y = 15
HUM_PIECE_COUNT_LOC_X = 40
AI_PIECE_COUNT_LOC_X = 880
PIECE_COUNT_LOC_Y = 458
#game screens
CHECKERS_START_SCREEN = pg.transform.scale(pg.image.load("./media/checkers/start-screen.png"), (CHECKERS_SCREEN_WIDTH, CHECKERS_SCREEN_HEIGHT))
CHECKERS_HUMAN_TURN = pg.transform.scale(pg.image.load("./media/checkers/human-turn.png"), (CHECKERS_SCREEN_WIDTH, CHECKERS_SCREEN_HEIGHT))
CHECKERS_AI_TURN = pg.transform.scale(pg.image.load("./media/checkers/ai-turn.png"), (CHECKERS_SCREEN_WIDTH, CHECKERS_SCREEN_HEIGHT))
#human player pieces
CHECKERS_HUMAN_PIECE = pg.transform.scale(pg.image.load("./media/checkers/human-piece.png"), (CHECKERS_PIECE_DIAMETER, CHECKERS_PIECE_DIAMETER))
CHECKERS_HUMAN_PIECE_ACTIVE = pg.transform.scale(pg.image.load("./media/checkers/human-piece-active.png"), (CHECKERS_PIECE_DIAMETER, CHECKERS_PIECE_DIAMETER))
CHECKERS_HUMAN_KING = pg.transform.scale(pg.image.load("./media/checkers/human-king.png"), (CHECKERS_PIECE_DIAMETER, CHECKERS_PIECE_DIAMETER))
CHECKERS_HUMAN_KING_ACTIVE = pg.transform.scale(pg.image.load("./media/checkers/human-king-active.png"), (CHECKERS_PIECE_DIAMETER, CHECKERS_PIECE_DIAMETER))
#ai player pieces
CHECKERS_AI_PIECE = pg.transform.scale(pg.image.load("./media/checkers/ai-piece.png"), (CHECKERS_PIECE_DIAMETER, CHECKERS_PIECE_DIAMETER))
CHECKERS_AI_PIECE_ACTIVE = pg.transform.scale(pg.image.load("./media/checkers/ai-piece-active.png"), (CHECKERS_PIECE_DIAMETER, CHECKERS_PIECE_DIAMETER))
CHECKERS_AI_KING = pg.transform.scale(pg.image.load("./media/checkers/ai-king.png"), (CHECKERS_PIECE_DIAMETER, CHECKERS_PIECE_DIAMETER))
CHECKERS_AI_KING_ACTIVE = pg.transform.scale(pg.image.load("./media/checkers/ai-king-active.png"), (CHECKERS_PIECE_DIAMETER, CHECKERS_PIECE_DIAMETER))
#end of game screens
CHECKERS_HUMAN_WON = pg.transform.scale(pg.image.load("./media/checkers/human-won.png"), (CHECKERS_SCREEN_WIDTH, CHECKERS_SCREEN_HEIGHT))
CHECKERS_AI_WON = pg.transform.scale(pg.image.load("./media/checkers/ai-won.png"), (CHECKERS_SCREEN_WIDTH, CHECKERS_SCREEN_HEIGHT))
CHECKERS_ITS_A_DRAW = pg.transform.scale(pg.image.load("./media/checkers/its-a-draw.png"), (CHECKERS_SCREEN_WIDTH, CHECKERS_SCREEN_HEIGHT))
# checkers buttons
CHECKERS_SOUND_ON_BTN = pg.transform.scale(pg.image.load("./media/checkers/sound-on.png"), (121, 81))
CHECKERS_SOUND_OFF_BTN = pg.transform.scale(pg.image.load("./media/checkers/sound-off.png"), (121, 81))
#other imgs
CHECKERS_GAME_INFO = pg.image.load("./media/checkers/game-info.png")
CHECKERS_AVAILABLE_MOVE = pg.transform.scale(pg.image.load("./media/checkers/available-move.png"), (8, 8))
CHECKERS_RESTARTING_GAME = pg.transform.scale(pg.image.load("./media/checkers/restarting-game.png"), (CHECKERS_SCREEN_WIDTH, CHECKERS_SCREEN_HEIGHT))
#checkers piece count imgs
CHECKERS_12 = pg.image.load("./media/checkers/12.png")
CHECKERS_11 = pg.image.load("./media/checkers/11.png")
CHECKERS_10 = pg.image.load("./media/checkers/10.png")
CHECKERS_9 = pg.image.load("./media/checkers/9.png")
CHECKERS_8 = pg.image.load("./media/checkers/8.png")
CHECKERS_7 = pg.image.load("./media/checkers/7.png")
CHECKERS_6 = pg.image.load("./media/checkers/6.png")
CHECKERS_5 = pg.image.load("./media/checkers/5.png")
CHECKERS_4 = pg.image.load("./media/checkers/4.png")
CHECKERS_3 = pg.image.load("./media/checkers/3.png")
CHECKERS_2 = pg.image.load("./media/checkers/2.png")
CHECKERS_1 = pg.image.load("./media/checkers/1.png")
CHECKERS_0 = pg.image.load("./media/checkers/0.png")
#audio
CHECKERS_BGR_MUSIC = pg.mixer.Sound("./media/checkers/Kai Engel - Irsen's Tale.wav")
CHECKERS_WIN_SOUND = pg.mixer.Sound("./media/checkers/win-sound.wav")
CHECKERS_AI_THINKING_SOUND = pg.mixer.Sound("./media/checkers/ai-thinking-sound.wav")

class MoveDirection(Enum):
	NORTHEAST = 1
	NORTHWEST = 2
	SOUTHEAST = 3
	SOUTHWEST = 4


#---OTHELLO---#
#Othello settings
OTH_SIMS_PER_MOVE_EASY = 1
OTH_SIMS_PER_MOVE_MEDIUM = 10
OTH_SIMS_PER_MOVE_HARD = 100
OTH_SCREEN_WIDTH = 600
OTH_SCREEN_HEIGHT = 800
OTH_SQUARE_SIZE = 60
OTH_BIT_SIZE = 55
OTH_BOARD_SIZE = 8
#load background, bits images, avatars
OTH_BACKGROUND_IMG = pg.transform.scale(pg.image.load("./media/othello/main-bgr.png"), (OTH_SCREEN_WIDTH , OTH_SCREEN_HEIGHT))
OTH_GREEN_BIT = pg.transform.scale(pg.image.load("./media/othello/green-power.png"), (OTH_BIT_SIZE, OTH_BIT_SIZE))
OTH_YELLOW_BIT = pg.transform.scale(pg.image.load("./media/othello/yellow-power.png"), (OTH_BIT_SIZE, OTH_BIT_SIZE))
OTH_HUMAN_PLAYER_AVATAR = pg.transform.scale(pg.image.load("./media/othello/human-player-avatar.png"), (AVATAR_SIZE, AVATAR_SIZE))
OTH_AI_PLAYER_AVATAR = pg.transform.scale(pg.image.load("./media/othello/ai-player-avatar.png"), (AVATAR_SIZE, AVATAR_SIZE))
OTH_HUMAN_PLAYER_THINKING_AVATAR = pg.transform.scale(pg.image.load("./media/othello/human-player-avatar-thinking.png"), (OTH_BIT_SIZE, OTH_BIT_SIZE))
OTH_AI_PLAYER_THINKING_AVATAR = pg.transform.scale(pg.image.load("./media/othello/ai-player-avatar-thinking.png"), (AVATAR_SIZE, AVATAR_SIZE))
OTH_HUMAN_PLAYER_WINNER_AVATAR = pg.transform.scale(pg.image.load("./media/othello/human-player-winner-avatar.png"), (AVATAR_SIZE+100, AVATAR_SIZE+100))
OTH_AI_PLAYER_WINNER_AVATAR = pg.transform.scale(pg.image.load("./media/othello/ai-player-winner-avatar.png"), (AVATAR_SIZE+100, AVATAR_SIZE+95))
OTH_HUMAN_PLAYER_LOSER_AVATAR = pg.transform.scale(pg.image.load("./media/othello/human-player-loser-avatar.png"), (AVATAR_SIZE, AVATAR_SIZE))
OTH_AI_PLAYER_LOSER_AVATAR = pg.transform.scale(pg.image.load("./media/othello/ai-player-loser-avatar.png"), (AVATAR_SIZE, AVATAR_SIZE))
OTH_WINNER_STARS = pg.transform.scale(pg.image.load("./media/othello/game-over-stars.png"), (OTH_SCREEN_WIDTH, OTH_SCREEN_HEIGHT//2))
OTH_GAME_INFO = pg.transform.scale(pg.image.load("./media/othello/game-info.jpg"), (OTH_SCREEN_WIDTH , OTH_SCREEN_HEIGHT))
#othello buttons
OTH_RESTART_BTN = pg.transform.scale(pg.image.load("./media/othello/restart-btn.png"), (50, 50))
OTH_BACK_BTN = pg.transform.scale(pg.image.load("./media/othello/back-btn.png"), (40, 50))
OTH_SOUND_ON_BTN = pg.transform.scale(pg.image.load("./media/othello/sound-on-btn.png"), (55, 45))
OTH_SOUND_OFF_BTN = pg.transform.scale(pg.image.load("./media/othello/sound-off-btn.png"), (56, 46))
OTH_GAME_INFO_BTN = pg.transform.scale(pg.image.load("./media/othello/game-info-btn.png"), (35, 50))
#othello labels
OTH_YOU_WON_LABEL = pg.image.load("./media/othello/you-won-label.png")
OTH_ITS_A_DRAW_LABEL = pg.image.load("./media/othello/its-a-draw-label.png")
OTH_AI_WON_LABEL = pg.image.load("./media/othello/ai-won-label.png")
OTH_HUMAN_PLAYER_LABEL = MAIN_FONT.render('HUMAN PLAYER', True, DTEAL)
OTH_AI_PLAYER_LABEL = MAIN_FONT.render('AI', True, DTEAL)
OTH_AI_THINKING_LABEL = MAIN_FONT.render('THINKING...', True, DTEAL)
#load othello sounds
OTH_BGR_MUSIC = pg.mixer.Sound("./media/othello/bgr-music-Stasis-Steve-Oxen.wav")
OTH_AI_THINKING_SOUND = pg.mixer.Sound("./media/othello/ai-thinking-sound.wav")
OTH_WINNING_SOUND = pg.mixer.Sound("./media/othello/win-sound.wav")
OTH_ITS_A_DRAW_SOUND = pg.mixer.Sound("./media/othello/its-a-draw-sound-owl.wav")


#CONNECT4
C4_SIMS_PER_MOVE_EASY = 10
C4_SIMS_PER_MOVE_MEDIUM = 60
C4_SIMS_PER_MOVE_HARD = 1500
#Connect4 screen parameters
C4_SCREEN_WIDTH = 600
C4_SCREEN_HEIGHT = 650
C4_BIT_DIAMETER = 62
C4_ROWS = 6
C4_COLS = 7
#c4 images
C4_BACKGROUND_IMG = pg.transform.scale(pg.image.load("./media/connect4/bgr.png"), (C4_SCREEN_WIDTH , C4_SCREEN_HEIGHT))
C4_HUMAN_PLAYER_AVATAR = pg.transform.scale(pg.image.load("./media/connect4/human-player-avatar.png"), (AVATAR_SIZE, AVATAR_SIZE))
C4_AI_PLAYER_AVATAR = pg.transform.scale(pg.image.load("./media/connect4/ai-player-avatar.png"), (AVATAR_SIZE, AVATAR_SIZE))
C4_AI_PLAYER_THINKING_AVATAR = pg.transform.scale(pg.image.load("./media/connect4/ai-player-thinking-avatar.png"), (AVATAR_SIZE, AVATAR_SIZE))
C4_HUMAN_WINNER_AVATAR = pg.image.load("./media/connect4/human-player-winner-avatar.png")
C4_HUMAN_LOSER_AVATAR = pg.image.load("./media/connect4/human-player-loser-avatar.png")
C4_AI_WINNER_AVATAR = pg.image.load("./media/connect4/ai-player-winner-avatar.png")
C4_AI_LOSER_AVATAR = pg.image.load("./media/connect4/ai-player-loser-avatar.png")
C4_RED_MOON_BIT = pg.transform.scale(pg.image.load("./media/connect4/red-moon-bit.png"), (C4_BIT_DIAMETER, C4_BIT_DIAMETER))
C4_YELLOW_MOON_BIT = pg.transform.scale(pg.image.load("./media/connect4/yellow-moon-bit.png"), (C4_BIT_DIAMETER, C4_BIT_DIAMETER))
C4_RESTART_BTN = pg.transform.scale(pg.image.load("./media/connect4/restart-btn.png"), (50, 50))
C4_BACK_BTN = pg.transform.scale(pg.image.load("./media/connect4/back-btn.png"), (35, 50))
C4_SOUND_ON_BTN = pg.transform.scale(pg.image.load("./media/connect4/sound-on-btn.png"), (50, 45))
C4_SOUND_OFF_BTN = pg.transform.scale(pg.image.load("./media/connect4/sound-off-btn.png"), (50, 45))
C4_GAME_INFO_BTN = pg.transform.scale(pg.image.load("./media/connect4/game-info-btn.png"), (30, 50))
C4_GAME_INFO = pg.transform.scale(pg.image.load("./media/connect4/game-info.png"), (C4_SCREEN_WIDTH , C4_SCREEN_HEIGHT))
#connect4 labels
C4_YOU_WON_LABEL = SCREEN_MSG_FONT.render("YOU WON!", True, PINK)
C4_AI_WON_LABEL = SCREEN_MSG_FONT.render("AI WON!", True, PINK)
C4_HUMAN_PLAYER_LABEL = pg.transform.scale(pg.image.load("./media/connect4/human-player-label.png"), (120, 20))#mainFont.render('HUMAN', True, PINK)
C4_AI_PLAYER_LABEL =  pg.transform.scale(pg.image.load("./media/connect4/ai-player-label.png"), (40, 20))#mainFont.render('AI', True, PINK)
#connect4 audio
C4_BGR_MUSIC = pg.mixer.Sound("./media/connect4/main-theme-DanielBirch-Indigo-Moon.wav")
C4_AI_THINKING_SOUND = pg.mixer.Sound("./media/connect4/ai-thinking-sound.wav")
C4_WIN_SOUND = pg.mixer.Sound("./media/connect4/win-sound-nenadsimic-picked-coin-echo.wav")


#---NIM---#
#nim screen parameters
NIM_SIMS_PER_MOVE_EASY = 1
NIM_SIMS_PER_MOVE_MEDIUM = 10
NIM_SIMS_PER_MOVE_HARD = 1500
NIM_SCREEN_WIDTH = 600
NIM_SCREEN_HEIGHT = 700
NIM_DEFAULT_NUM_OF_OBJECTS = 21
NIM_BACKGROUND_IMG = pg.image.load("./media/nim/bgr.jpg")
NIM_BUBBLE = pg.transform.scale(pg.image.load("./media/nim/bubble.png"), (80, 80))
NIM_BUBBLE_SELECTED = pg.transform.scale(pg.image.load("./media/nim/bubble-selected.png"), (80, 80))
NIM_POP_BTN = pg.transform.scale(pg.image.load("./media/nim/pop-btn.png"), (200, 50))
NIM_UNDO_BTN = pg.transform.scale(pg.image.load("./media/nim/undo-btn.png"), (200, 50))
NIM_RESTART_BTN = pg.transform.scale(pg.image.load("./media/nim/restart-game-btn.png"), (50, 50))
NIM_BACK_BTN = pg.transform.scale(pg.image.load("./media/nim/back-btn.png"), (45, 60))
NIM_SOUND_ON_BTN = pg.transform.scale(pg.image.load("./media/nim/sound-on-btn.png"), (60, 45))
NIM_SOUND_OFF_BTN = pg.transform.scale(pg.image.load("./media/nim/sound-off-btn.png"), (60, 45))
NIM_GAME_INFO_BTN = pg.transform.scale(pg.image.load("./media/nim/game-info-btn.png"), (30, 45))
NIM_GAME_INFO = pg.image.load("./media/nim/game-info.png")
#nim labels
NIM_YOU_WON_LABEL = pg.image.load("./media/nim/you-won-label.png")
NIM_AI_WON_LABEL = pg.image.load("./media/nim/ai-won-label.png")
NIM_AI_THINKING_LABEL = pg.transform.scale(pg.image.load("./media/nim/ai-thinking-label.png"), (140, 40))
NIM_RESTARTING_GAME_LABEL = SCREEN_MSG_FONT.render("RESTARTING GAME...", True, PURPLE)
#nim audio
NIM_BGR_MUSIC = pg.mixer.Sound("./media/nim/bgr-music-precious-memories.wav")
NIM_BUBBLE_POP_SOUND = pg.mixer.Sound("./media/nim/bubble-pop-sound.wav")
NIM_WINNING_SOUND = pg.mixer.Sound("./media/nim/win-sound.wav")
NIM_AI_THINKING_SOUND = pg.mixer.Sound("./media/nim/ai-thinking-sound.wav")


#---OXO---#
OXO_DEFAULT_SIMS_PER_MOVE = 1500
#oxo screen settings
OXO_SCREEN_WIDTH = 400
OXO_SCREEN_HEIGHT = 600
OXO_ROWS, OXO_COLS = 3, 3
OXO_SQUARE_SIZE = 100
OXO_SYMBOL_SIZE = 90
OXO_SYMBOL_BORDER = 2
OXO_GAME_MODES_BTN_MARGIN_LEFT = 60
OXO_GAME_MODES_BTN_MARGIN_RIGHT = 340

#common oxo images
OXO_GAME_MODES = pg.image.load("./media/game-modes.png")
OXO_X_SYMBOL = pg.transform.scale(pg.image.load("./media/oxo/x.png"), (OXO_SYMBOL_SIZE, OXO_SYMBOL_SIZE))
OXO_O_SYMBOL = pg.transform.scale(pg.image.load("./media/oxo/o.png"), (OXO_SYMBOL_SIZE, OXO_SYMBOL_SIZE))
OXO_BLACK_LINE = pg.transform.scale(pg.image.load("./media/oxo/line.png"), (285, 15))
OXO_ITS_A_DRAW = pg.transform.scale(pg.image.load("./media/oxo/its-a-draw.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
OXO_AI_WON = pg.transform.scale(pg.image.load("./media/oxo/ai-won.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
#common oxo buttons
OXO_SOUND_ON_BTN = pg.transform.scale(pg.image.load("./media/oxo/sound-on-btn.png"), (50 , 40))
OXO_SOUND_OFF_BTN = pg.transform.scale(pg.image.load("./media/oxo/sound-off-btn.png"), (50 , 40))
#human vs human mode images
OXO_HUM_VS_HUM_START_SCREEN = pg.transform.scale(pg.image.load("./media/oxo/human-vs-human-mode/start-screen.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
OXO_HUM_VS_HUM_PLAYER1_TURN = pg.transform.scale(pg.image.load("./media/oxo/human-vs-human-mode/player1-turn.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
OXO_HUM_VS_HUM_PLAYER2_TURN = pg.transform.scale(pg.image.load("./media/oxo/human-vs-human-mode/player2-turn.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
OXO_HUM_VS_HUM_GAME_INFO = pg.transform.scale(pg.image.load("./media/oxo/human-vs-human-mode/game-info.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
OXO_HUM_VS_HUM_PLAYER1_WON = pg.transform.scale(pg.image.load("./media/oxo/human-vs-human-mode/player1-won.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
OXO_HUM_VS_HUM_PLAYER2_WON = pg.transform.scale(pg.image.load("./media/oxo/human-vs-human-mode/player2-won.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
#human vs ai mode images
OXO_HUM_VS_AI_START_SCREEN = pg.transform.scale(pg.image.load("./media/oxo/human-vs-ai-mode/start-screen.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
OXO_HUM_VS_AI_HUMAN_TURN = pg.transform.scale(pg.image.load("./media/oxo/human-vs-ai-mode/human-turn.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
OXO_HUM_VS_AI_AI_TURN = pg.transform.scale(pg.image.load("./media/oxo/human-vs-ai-mode/ai-turn.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
OXO_HUM_VS_AI_GAME_INFO = pg.transform.scale(pg.image.load("./media/oxo/human-vs-ai-mode/game-info.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
OXO_HUM_VS_AI_HUMAN_WON = pg.transform.scale(pg.image.load("./media/oxo/human-vs-ai-mode/human-won.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
#ai vs ai mode images
OXO_AI_VS_AI_START_SCREEN = pg.transform.scale(pg.image.load("./media/oxo/ai-vs-ai-mode/start-screen.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
OXO_AI_VS_AI_AI1_TURN = pg.transform.scale(pg.image.load("./media/oxo/ai-vs-ai-mode/ai1-turn.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
OXO_AI_VS_AI_AI2_TURN = pg.transform.scale(pg.image.load("./media/oxo/ai-vs-ai-mode/ai2-turn.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
OXO_AI_VS_AI_GAME_INFO = pg.transform.scale(pg.image.load("./media/oxo/ai-vs-ai-mode/game-info.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
#other imgs
OXO_RESTARTING_GAME = pg.transform.scale(pg.image.load("./media/oxo/restarting-game.png"), (OXO_SCREEN_WIDTH, OXO_SCREEN_HEIGHT))
#OXO_SOUND_ON_DARK = pg.image.load("./media/oxo/sound-on-btn.png")
OXO_SOUND_OFF_BTN_DARK = pg.image.load("./media/oxo/sound-off-btn-dark.png")
OXO_SOUND_ON_BTN_DARK = pg.image.load("./media/oxo/sound-on-btn-dark.png")
#oxo audio
OXO_BGR_MUSIC = pg.mixer.Sound("./media/oxo/main-theme.wav")
OXO_AI_THINKING_SOUND = pg.mixer.Sound("./media/oxo/ai-thinking-sound.wav")
OXO_WIN_SOUND = pg.mixer.Sound("./media/oxo/win-sound.wav")
OXO_SOUND_BTN_LOC_X = 248
OXO_SOUND_BTN_LOC_Y = 5
#all oxo winning combos
class OXOWinLine(Enum):
	VERTICAL1 = 1
	VERTICAL2 = 2
	VERTICAL3 = 3
	HORIZONTAL1 = 4
	HORIZONTAL2 = 5
	HORIZONTAL3 = 6
	DIAGONAL1 = 7
	DIAGONAL2 = 8