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
    'character_box': (0, SCREEN_HEIGHT),
    'shop': (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
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
    'carrot': 0.6,
    'cabbage': 0.6,
    'overgine': 0.5,
    'tulip': 0.5,
    'lettuce': 0.4,
    'pumpkin': 0.4,
    'turnip': 0.3,
    'bell_pepper': 0.3,
    'beetroot': 0.2,
    'blue_star': 0.2,
    'edamame': 0.1
}

# shop settings
SALE_PRICES = {
    'wood': 4,
    'apple': 2,
    'orange': 2,
    'peach': 2,
    'pear': 2,
    'fish': 12,
    'wheat': 3,
    'tomato': 3,
    'corn': 8,
    'cabbage': 4,
    'carrot': 5,
    'overgine': 5,
    'tulip': 6,
    'lettuce': 6,
    'pumpkin': 7,
    'turnip': 7,
    'bell_pepper': 8,
    'beetroot': 8,
    'blue_star': 9,
    'edamame': 9,
    'wheat_seed': 1,
    'tomato_seed': 1,
    'corn_seed': 1,
    'cabbage_seed': 1,
    'carrot_seed': 1,
    'overgine_seed': 1,
    'tulip_seed': 1,
    'lettuce_seed': 1,
    'pumpkin_seed': 1,
    'turnip_seed': 1,
    'bell_pepper_seed': 1,
    'beetroot_seed': 1,
    'blue_star_seed': 1,
    'edamame_seed': 1
}

PURCHASE_PRICES = {
    'wood': 8,
    'apple': 4,
    'orange': 4,
    'peach': 4,
    'pear': 4,
    'fish': 24,
    'wheat': 6,
    'tomato': 6,
    'corn': 16,
    'cabbage': 8,
    'carrot': 10,
    'overgine': 10,
    'tulip': 12,
    'lettuce': 12,
    'pumpkin': 14,
    'turnip': 14,
    'bell_pepper': 16,
    'beetroot': 16,
    'blue_star': 18,
    'edamame': 18,
    'wheat_seed': 2,
    'tomato_seed': 2,
    'corn_seed': 2,
    'cabbage_seed': 2,
    'carrot_seed': 2,
    'overgine_seed': 2,
    'tulip_seed': 2,
    'lettuce_seed': 2,
    'pumpkin_seed': 2,
    'turnip_seed': 2,
    'bell_pepper_seed': 2,
    'beetroot_seed': 2,
    'blue_star_seed': 2,
    'edamame_seed': 2
}
