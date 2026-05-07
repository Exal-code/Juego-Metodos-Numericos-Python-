# ============================================
# config.py - Constantes y configuración global
# ============================================

# --- Pantalla ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# --- Tiles y Mapa ---
TILE_SIZE = 48
MAP_COLS = 20
MAP_ROWS = 19
MAP_WIDTH = MAP_COLS * TILE_SIZE   # 960
MAP_HEIGHT = MAP_ROWS * TILE_SIZE  # 912

# --- Colores Generales ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# --- Colores de la Casa ---
FLOOR_BEDROOM = (180, 200, 220)
FLOOR_KITCHEN = (240, 230, 210)
FLOOR_BATHROOM = (200, 230, 230)
FLOOR_LIVING = (210, 185, 155)
FLOOR_PATIO = (80, 160, 80)
WALL_COLOR = (101, 67, 33)
WALL_TOP_COLOR = (130, 90, 50)

# --- Colores de Muebles ---
BED_COLOR = (70, 130, 180)
BED_PILLOW = (230, 230, 245)
DESK_COLOR = (139, 119, 101)
LAMP_COLOR = (255, 215, 0)
LAMP_GLOW = (255, 255, 200)
STOVE_COLOR = (105, 105, 105)
FRIDGE_COLOR = (220, 225, 230)
TABLE_COLOR = (160, 82, 45)
CHAIR_COLOR = (139, 90, 43)
TUB_COLOR = (173, 216, 230)
TUB_INNER = (200, 230, 245)
TOILET_COLOR = (240, 240, 240)
SINK_COLOR = (200, 200, 210)
SOFA_COLOR = (140, 35, 35)
TV_COLOR = (25, 25, 25)
TV_SCREEN = (40, 60, 80)
ARMCHAIR_COLOR = (139, 69, 19)
BOX_COLOR = (210, 180, 100)
BOX_TAPE = (180, 150, 70)

# --- Colores de Libros ---
BOOK_COLORS = {
    "green":  (34, 180, 34),
    "red":    (220, 50, 50),
    "blue":   (50, 120, 255),
    "purple": (148, 103, 189),
}

# --- Colores del Búnker ---
BUNKER_WALL = (85, 85, 95)
BUNKER_FLOOR = (65, 65, 75)
BUNKER_CEILING = (75, 75, 85)
METAL_DOOR = (120, 120, 135)
METAL_DOOR_DARK = (90, 90, 105)
SHELF_COLOR = (101, 67, 33)
SHELF_DARK = (80, 50, 25)
BUNKER_ENTRANCE = (90, 90, 100)

# --- Colores del Jugador ---
PLAYER_SKIN = (255, 218, 185)
PLAYER_SHIRT = (0, 120, 200)
PLAYER_PANTS = (0, 0, 139)
PLAYER_CAP = (220, 20, 60)
PLAYER_BACKPACK = (139, 69, 19)
PLAYER_HAIR = (50, 30, 10)
PLAYER_EYE = (30, 30, 30)

# --- Colores de UI ---
UI_BG = (35, 35, 45)
UI_BORDER = (100, 100, 120)
WOOD_COLOR = (160, 110, 60)
WOOD_DARK = (120, 80, 40)
WOOD_LIGHT = (190, 140, 80)
TIMER_COLOR = (255, 70, 70)
TIMER_BG = (30, 30, 40, 180)
INVENTORY_BG = (30, 30, 40)
INVENTORY_BORDER = (80, 80, 100)

# --- Colores del Menú ---
MENU_BG_TOP = (30, 30, 50)
MENU_BG_BOT = (50, 40, 60)
MENU_SELECTED = (255, 215, 0)
MENU_NORMAL = (200, 200, 210)
MENU_TITLE = (255, 100, 100)
MENU_SUBTITLE = (180, 180, 200)

# --- Colores del Modal ---
MODAL_BG = (40, 40, 55)
MODAL_BORDER = (120, 120, 150)
MODAL_HEADER = (50, 50, 70)
BUTTON_GREEN = (50, 140, 50)
BUTTON_GREEN_HOVER = (70, 180, 70)
BUTTON_RED = (180, 50, 50)
BUTTON_RED_HOVER = (220, 70, 70)
BUTTON_BLUE = (50, 100, 180)
BUTTON_BLUE_HOVER = (70, 130, 220)
BUTTON_GRAY = (100, 100, 110)
BUTTON_GRAY_HOVER = (130, 130, 140)
INPUT_BG = (25, 25, 35)
INPUT_BORDER = (90, 90, 110)
INPUT_ACTIVE = (80, 160, 220)
INPUT_TEXT = (240, 240, 240)

# --- Estados del Juego ---
STATE_MENU = "menu"
STATE_CONTROLS = "controls"
STATE_OPTIONS = "options"
STATE_CREDITS = "credits"
STATE_HOUSE = "house"
STATE_BUNKER = "bunker"
STATE_PROBLEM = "problem"
STATE_ENDING = "ending"

# --- Tipos de Final ---
ENDING_PERFECT = "perfect"      # 4/4 aciertos
ENDING_PARTIAL = "partial"      # 3/4 aciertos (1 error)
ENDING_FAILURE = "failure"      # 2+ errores
ENDING_TIMEOUT = "timeout"      # No entró al búnker

# --- Temporización de Días (en segundos) ---
DAY_BASE_TIMES = [20 * 60, 30 * 60, 50 * 60, 50 * 60]  # 20, 30, 50, 50 min
DAY_BONUSES = [0, 10 * 60, 20 * 60, 40 * 60]            # 0, 10, 20, 40 min
DAY_PENALTY = 3 * 60                                     # 3 min

# --- Movimiento del Jugador ---
PLAYER_SPEED = 3
PICKUP_DISTANCE = 30  # distancia en píxeles para recoger libro

# --- Tipos de Tile ---
TILE_FLOOR = 0
TILE_WALL = 1
TILE_PATIO = 2
TILE_BUNKER = 3

# --- Datos del Mapa de la Casa ---
# 0 = suelo, 1 = pared, 2 = patio, 3 = entrada al búnker
# LAYOUT: Patio+Búnker arriba, Baño+Sala, Recámara1+Cocina, Recámara2 abajo, puerta principal
HOUSE_MAP = [
    #  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 0  pared superior
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],  # 1  Patio
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],  # 2  Búnker col 9
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],  # 3  Patio
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],  # 4  pared (puerta cols 8-11)
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 5  Baño | Sala
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 6
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 7
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 8  puerta col 6
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],  # 9  pared (puertas col 4, 14)
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 10 Recámara 1 | Cocina
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 11
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 12
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 13 puerta col 9
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],  # 14 pared (puertas col 4, 14)
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 15 Recámara 2
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 16
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 17
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 18 pared inferior (puerta cols 9-10)
]

# --- Definición de Muebles ---
# Cada mueble: (col, row, ancho_tiles, alto_tiles, color, nombre)
FURNITURE = [
    # Recámara 1 (rows 10-13, cols 1-8)
    (1, 10, 2, 2, BED_COLOR, "cama"),
    (6, 10, 2, 1, DESK_COLOR, "escritorio"),
    (8, 10, 1, 1, LAMP_COLOR, "lámpara"),

    # Cocina (rows 10-13, cols 10-18)
    (10, 10, 2, 1, STOVE_COLOR, "estufa"),
    (18, 10, 1, 2, FRIDGE_COLOR, "refrigerador"),
    (13, 11, 3, 2, TABLE_COLOR, "mesa"),
    (12, 12, 1, 1, CHAIR_COLOR, "silla"),
    (16, 11, 1, 1, CHAIR_COLOR, "silla"),

    # Baño (rows 5-8, cols 1-5)
    (1, 5, 2, 2, TUB_COLOR, "tina"),
    (5, 5, 1, 1, TOILET_COLOR, "retrete"),
    (5, 7, 1, 1, SINK_COLOR, "lavabo"),

    # Sala (rows 5-8, cols 7-18)
    (8, 5, 3, 1, SOFA_COLOR, "sofá"),
    (9, 7, 1, 1, TV_COLOR, "TV"),
    (7, 7, 1, 1, ARMCHAIR_COLOR, "sillón"),
    (11, 7, 1, 1, ARMCHAIR_COLOR, "sillón"),
    (17, 7, 2, 2, BOX_COLOR, "cajas"),

    # Recámara 2 (rows 15-17, cols 1-18)
    (1, 15, 2, 2, BED_COLOR, "cama"),
    (5, 15, 2, 1, DESK_COLOR, "escritorio"),
    (7, 16, 1, 1, LAMP_COLOR, "lámpara"),
    (16, 15, 2, 2, BOX_COLOR, "cajas"),
    (13, 16, 1, 1, ARMCHAIR_COLOR, "sillón"),
]

# Crear set de tiles bloqueados por muebles (para colisiones)
FURNITURE_BLOCKED = set()
for fc, fr, fw, fh, _, _ in FURNITURE:
    for dc in range(fw):
        for dr in range(fh):
            FURNITURE_BLOCKED.add((fc + dc, fr + dr))

# --- Definición de Habitaciones (para colores de piso) ---
# (col_min, col_max, row_min, row_max, color, nombre)
ROOMS = [
    (1, 8, 10, 13, FLOOR_BEDROOM,  "Recámara 1"),
    (10, 18, 10, 13, FLOOR_KITCHEN, "Cocina"),
    (1, 5, 5, 8, FLOOR_BATHROOM, "Baño"),
    (7, 18, 5, 8, FLOOR_LIVING,   "Sala"),
    (1, 18, 15, 17, FLOOR_BEDROOM, "Recámara 2"),
]
