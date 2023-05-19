from pygame.math import Vector2

# SCREEN
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 810
TILE_SIZE = 64

OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 15),
    'seed': (70, SCREEN_HEIGHT - 5),
    'stamina': (15, 15),
    'xp': (15, 50)}

PLAYER_TOOL_OFFSET = {
    'left': Vector2(-50, 50),
    'right': Vector2(50, 40),
    'up': Vector2(0, -10),
    'down': Vector2(0, 50)}

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

APPLE_POS = {
    "Small": [(18, 17), (30, 37), (12, 50), (30, 45), (20, 30), (30, 10)],
    "Large": [(30, 24), (60, 65), (50, 50), (16, 40), (45, 50), (42, 70)],
    "Fir Tree": [(30, 24), (60, 65), (50, 50), (16, 40), (45, 50), (42, 70)],
    "green_tree": [(30, 24), (60, 65), (50, 50), (16, 40), (45, 50), (42, 70)],
}

GROW_SPEED = {
    'corn': 1,
    'tomato': 0.7
}

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

INVENTORY_OFFSETS = {
    0: (42, 116),
    1: (89, 89),
    2: 5,
    3: (38 + 19, 76),
    4: (800, 76),
    5: 19
}

GAME_MESSAGES = {
    "TXT_BEG": (SCREEN_WIDTH - 30, SCREEN_HEIGHT - SCREEN_HEIGHT // 7),
    "TEXT_SPACE": 10,
    "TEXT_TIMER": 700,
    "TEXT_CHOICES": ["SWAPPED TOOL"]
}
