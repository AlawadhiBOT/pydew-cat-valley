import pygame.display
from pygame.math import Vector2

# SCREEN
infoObject = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = infoObject.current_w, infoObject.current_h
TILE_SIZE = 64
del infoObject

# General overlay
OVERLAY_POSITIONS = {
    'seed': (SCREEN_WIDTH / 13, SCREEN_HEIGHT - 15),
    'inven': (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 10),
    'tool': (SCREEN_WIDTH / 2 + 10, SCREEN_HEIGHT - 10 + 10),
    'stamina': (SCREEN_WIDTH - 5, SCREEN_HEIGHT - 5),
    'xp': "is a function of inven, use that.",
    'heart': (6, 6),
    'character_box': (0, SCREEN_HEIGHT)
}

STAMINA_COLORS = {
    "very happy": (174, 212, 153),
    "happy": (192, 212, 112),
    "normal": (234, 225, 110),
    "unhappy": (238, 186, 119),
    "sad": (102, 65, 101),
    "dead": (220, 224, 210)
}

GAME_MESSAGES = {
    "TXT_BEG": (SCREEN_WIDTH - 30, SCREEN_HEIGHT - SCREEN_HEIGHT // 7),
    "TEXT_SPACE": 10,
    "TEXT_TIMER": 700,
    "TEXT_CHOICES": ["SWAPPED TOOL"]
}

# player
PLAYER_TOOL_OFFSET = {
    'left': Vector2(-50, 50),
    'right': Vector2(50, 40),
    'up': Vector2(0, -10),
    'down': Vector2(0, 50)}

INVENTORY_OFFSETS = {
    3: (38 + 19, 76),
}

PLAYER_LEVEL_STATS = {
    "max xp": 30,
    'dig': 1,
    'water': 1,
    'buy': 1,
    'sell': 2,
    'plant': 3,
    'harvest': 3,
    'fish': 3,
    'wood': 5,
}

PLAYER_STAMINA_STATS = {
    "stamina": 200,
    "stamina increase": 10,
    "dig": 5,
    "water": 3,
    'fishing': 2,
    "tree": 1,
    "plant": 1,
    'buy': 1,
    "sell": 1
}

# level
LAYERS = {
    'water': 0,
    'ground': 1,
    'port': 2,
    'soil': 3,
    'soil water': 4,
    'rain floor': 5,
    'house bottom': 6,
    'ground plant': 7,
    'main': 8,
    'house top': 9,
    'fruit': 10,
    'rain drops': 11,
}

MAP_NUMBERS = {
    "Starting": 0,
    "Forest": 1,
}

# plant settings
PLANT_OFFSET = {
    'wheat': -16,
    'tomato': -8,
    'corn': -16,
    'cabbage': -16,
    'carrot': -16,
    'overgine': -16,
    'tulip': -16,
    'lettuce': -16,
    'pumpkin': -16,
    'turnip': -16,
    'bell_pepper': -16,
    'beetroot': -16,
    'blue_star': -16,
    'edamame': -16
}

# works as an adjustment to deal with tall plants
BIG_PLANT_OFFSET = {
    'wheat': 0,
    'tomato': 0,
    'corn': 16,
    'cabbage': 0,
    'carrot': 0,
    'overgine': 0,
    'tulip': 0,
    'lettuce': 0,
    'pumpkin': 0,
    'turnip': 0,
    'bell_pepper': 0,
    'beetroot': 0,
    'blue_star': 0,
    'edamame': 0
}

APPLE_POS = {
    "Small": [(18, 17), (30, 37), (12, 50), (30, 45), (20, 30), (30, 10)],
    "Large": [(30, 24), (60, 65), (50, 50), (16, 40), (45, 50), (42, 70)],
    "Fir Tree": [(30, 24), (60, 65), (50, 50), (16, 40), (45, 50), (42, 70)],
    "green_tree": [(30, 24), (60, 65), (50, 50), (16, 40), (45, 50), (42, 70)],
}

# tomato originally 0.7
GROW_SPEED = {
    'wheat': 1,
    'tomato': 0.7,
    'corn': 1,
    'carrot': 1,
    'cabbage': 1,
    'overgine': 1,
    'tulip': 1,
    'lettuce': 1,
    'pumpkin': 1,
    'turnip': 1,
    'bell_pepper': 1,
    'beetroot': 1,
    'blue_star': 1,
    'edamame': 1
}

# shop settings
SALE_PRICES = {
    'wood': 4,
    'apple': 2,
    'corn': 10,
    'fish': 12,
    'tomato': 15,
}

PURCHASE_PRICES = {
    'corn': 4,
    'tomato': 5
}
