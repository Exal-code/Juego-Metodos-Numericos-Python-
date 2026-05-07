# ============================================
# house.py - Mapa de la casa y fase de recolección
# ============================================

import pygame
import random
import math
from config import (
    TILE_SIZE, MAP_COLS, MAP_ROWS, MAP_WIDTH, MAP_HEIGHT,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    HOUSE_MAP, FURNITURE, FURNITURE_BLOCKED, ROOMS,
    TILE_FLOOR, TILE_WALL, TILE_PATIO, TILE_BUNKER,
    WALL_COLOR, WALL_TOP_COLOR, FLOOR_PATIO, FLOOR_LIVING,
    BED_COLOR, BED_PILLOW, DESK_COLOR, LAMP_COLOR, LAMP_GLOW,
    STOVE_COLOR, FRIDGE_COLOR, TABLE_COLOR, CHAIR_COLOR,
    TUB_COLOR, TUB_INNER, TOILET_COLOR, SINK_COLOR,
    SOFA_COLOR, TV_COLOR, TV_SCREEN, ARMCHAIR_COLOR,
    BOX_COLOR, BOX_TAPE, BUNKER_ENTRANCE,
    BOOK_COLORS, PICKUP_DISTANCE,
    TIMER_COLOR, WHITE, BLACK, DARK_GRAY, LIGHT_GRAY,
    STATE_BUNKER, STATE_ENDING, ENDING_TIMEOUT,
)
from entities import Player, Book, Camera, Inventory


# ============================================
#  POSICIONES CLAVE DEL MAPA
# ============================================
# Búnker: columna 9, fila 2 (zona del patio, arriba)
BUNKER_COL = 9
BUNKER_ROW = 2
# Jugador inicia en la puerta principal (abajo centro)
PLAYER_START_COL = 9
PLAYER_START_ROW = 17

# Tiempo en segundos para el efecto de gas verde
GAS_START_TIME = 7
# Duración del congelamiento al acabarse el tiempo
FREEZE_DURATION = 3.0


# ============================================
#  FUNCIONES DE DIBUJO DEL MAPA
# ============================================

def get_floor_color(col, row):
    """Obtiene el color del piso según la habitación."""
    for cmin, cmax, rmin, rmax, color, _ in ROOMS:
        if cmin <= col <= cmax and rmin <= row <= rmax:
            return color
    # Si es patio
    if HOUSE_MAP[row][col] == TILE_PATIO or HOUSE_MAP[row][col] == TILE_BUNKER:
        return FLOOR_PATIO
    # Pasillos y puertas
    return FLOOR_LIVING


def get_room_name(col, row):
    """Obtiene el nombre de la habitación en la posición dada."""
    for cmin, cmax, rmin, rmax, _, name in ROOMS:
        if cmin <= col <= cmax and rmin <= row <= rmax:
            return name
    if 1 <= row <= 3:
        return "Patio"
    return ""


def draw_map(surface, cam_x, cam_y):
    """Dibuja el mapa de la casa (tiles)."""
    start_col = max(0, int(cam_x // TILE_SIZE))
    end_col = min(MAP_COLS, int((cam_x + SCREEN_WIDTH) // TILE_SIZE) + 2)
    start_row = max(0, int(cam_y // TILE_SIZE))
    end_row = min(MAP_ROWS, int((cam_y + SCREEN_HEIGHT) // TILE_SIZE) + 2)

    for row in range(start_row, end_row):
        for col in range(start_col, end_col):
            tile = HOUSE_MAP[row][col]
            sx = int(col * TILE_SIZE - cam_x)
            sy = int(row * TILE_SIZE - cam_y)
            rect = pygame.Rect(sx, sy, TILE_SIZE, TILE_SIZE)

            if tile == TILE_WALL:
                pygame.draw.rect(surface, WALL_COLOR, rect)
                pygame.draw.rect(surface, WALL_TOP_COLOR,
                                 (sx, sy, TILE_SIZE, 4))
                pygame.draw.line(surface, WALL_TOP_COLOR,
                                 (sx, sy + TILE_SIZE // 2),
                                 (sx + TILE_SIZE, sy + TILE_SIZE // 2), 1)
                if row % 2 == 0:
                    pygame.draw.line(surface, WALL_TOP_COLOR,
                                     (sx + TILE_SIZE // 2, sy),
                                     (sx + TILE_SIZE // 2, sy + TILE_SIZE // 2), 1)
                else:
                    pygame.draw.line(surface, WALL_TOP_COLOR,
                                     (sx + TILE_SIZE // 4, sy + TILE_SIZE // 2),
                                     (sx + TILE_SIZE // 4, sy + TILE_SIZE), 1)
                    pygame.draw.line(surface, WALL_TOP_COLOR,
                                     (sx + 3 * TILE_SIZE // 4, sy + TILE_SIZE // 2),
                                     (sx + 3 * TILE_SIZE // 4, sy + TILE_SIZE), 1)
            elif tile == TILE_PATIO:
                pygame.draw.rect(surface, FLOOR_PATIO, rect)
                for i in range(3):
                    gx = sx + 10 + i * 14
                    gy = sy + 15 + (i * 7) % 20
                    pygame.draw.line(surface, (60, 140, 60),
                                     (gx, gy), (gx - 2, gy - 6), 1)
                    pygame.draw.line(surface, (60, 140, 60),
                                     (gx, gy), (gx + 2, gy - 5), 1)
            elif tile == TILE_BUNKER:
                pygame.draw.rect(surface, FLOOR_PATIO, rect)
                bunker_rect = pygame.Rect(sx + 4, sy + 4, TILE_SIZE - 8, TILE_SIZE - 8)
                pygame.draw.rect(surface, BUNKER_ENTRANCE, bunker_rect, border_radius=3)
                pygame.draw.rect(surface, (130, 130, 145), bunker_rect, 2, border_radius=3)
                pygame.draw.circle(surface, (160, 160, 170),
                                   (sx + TILE_SIZE - 14, sy + TILE_SIZE // 2), 4)
                pygame.draw.circle(surface, DARK_GRAY,
                                   (sx + TILE_SIZE - 14, sy + TILE_SIZE // 2), 4, 1)
                font_small = pygame.font.SysFont("Arial", 9, bold=True)
                label = font_small.render("BÚNKER", True, (200, 200, 210))
                surface.blit(label, (sx + 6, sy + 6))
            else:
                floor_color = get_floor_color(col, row)
                pygame.draw.rect(surface, floor_color, rect)
                darker = (max(0, floor_color[0] - 10),
                          max(0, floor_color[1] - 10),
                          max(0, floor_color[2] - 10))
                pygame.draw.rect(surface, darker, rect, 1)

    # --- Dibujar puerta principal (en row 18, cols 9-10) ---
    # Vista: marco de puerta de madera en la pared inferior
    for dc in range(2):
        door_col = 9 + dc
        door_sx = int(door_col * TILE_SIZE - cam_x)
        door_sy = int(18 * TILE_SIZE - cam_y)
        if -TILE_SIZE < door_sx < SCREEN_WIDTH and -TILE_SIZE < door_sy < SCREEN_HEIGHT:
            # Piso del doorway
            pygame.draw.rect(surface, FLOOR_LIVING,
                             (door_sx, door_sy, TILE_SIZE, TILE_SIZE))
            # Marco de la puerta
            pygame.draw.rect(surface, (100, 60, 25),
                             (door_sx, door_sy, TILE_SIZE, TILE_SIZE), 3)


def draw_furniture(surface, cam_x, cam_y):
    """Dibuja todos los muebles de la casa."""
    for fc, fr, fw, fh, fcolor, fname in FURNITURE:
        sx = int(fc * TILE_SIZE - cam_x)
        sy = int(fr * TILE_SIZE - cam_y)
        w = fw * TILE_SIZE
        h = fh * TILE_SIZE

        if sx + w < 0 or sx > SCREEN_WIDTH or sy + h < 0 or sy > SCREEN_HEIGHT:
            continue

        rect = pygame.Rect(sx + 2, sy + 2, w - 4, h - 4)

        if fname == "cama":
            pygame.draw.rect(surface, fcolor, rect, border_radius=4)
            pygame.draw.rect(surface, (max(0, fcolor[0]-30), max(0, fcolor[1]-30),
                                        max(0, fcolor[2]-30)), rect, 2, border_radius=4)
            pillow = pygame.Rect(sx + 8, sy + 6, w - 16, h // 4)
            pygame.draw.rect(surface, BED_PILLOW, pillow, border_radius=3)
            for i in range(3):
                ly = sy + h // 3 + i * (h // 5)
                pygame.draw.line(surface, (max(0, fcolor[0]-15), max(0, fcolor[1]-15),
                                            max(0, fcolor[2]-15)),
                                 (sx + 6, ly), (sx + w - 6, ly), 1)
        elif fname == "escritorio":
            pygame.draw.rect(surface, fcolor, rect, border_radius=2)
            pygame.draw.rect(surface, (max(0, fcolor[0]-30), max(0, fcolor[1]-30),
                                        max(0, fcolor[2]-30)), rect, 2, border_radius=2)
            pygame.draw.rect(surface, (min(255,fcolor[0]+20), min(255,fcolor[1]+20),
                                        min(255,fcolor[2]+20)),
                             (sx + 4, sy + 2, w - 8, 4))
        elif fname == "lámpara":
            pygame.draw.rect(surface, DARK_GRAY, (sx + TILE_SIZE//3, sy + TILE_SIZE//2,
                                                    TILE_SIZE//3, TILE_SIZE//2 - 4))
            pygame.draw.circle(surface, LAMP_COLOR,
                               (sx + TILE_SIZE//2, sy + TILE_SIZE//3), TILE_SIZE//4)
            pygame.draw.circle(surface, LAMP_GLOW,
                               (sx + TILE_SIZE//2, sy + TILE_SIZE//3), TILE_SIZE//6)
        elif fname == "estufa":
            pygame.draw.rect(surface, fcolor, rect, border_radius=2)
            pygame.draw.rect(surface, (80, 80, 80), rect, 2, border_radius=2)
            for i in range(2):
                cx = sx + TILE_SIZE // 2 + i * (TILE_SIZE - 10) - 5
                cy = sy + TILE_SIZE // 2
                pygame.draw.circle(surface, (60, 60, 60), (cx, cy), 8)
                pygame.draw.circle(surface, (80, 80, 80), (cx, cy), 8, 1)
        elif fname == "refrigerador":
            pygame.draw.rect(surface, fcolor, rect, border_radius=3)
            pygame.draw.rect(surface, (180, 185, 190), rect, 2, border_radius=3)
            pygame.draw.rect(surface, (160, 160, 170),
                             (sx + w - 10, sy + h // 4, 4, h // 3), border_radius=2)
            pygame.draw.line(surface, (190, 195, 200),
                             (sx + 4, sy + h // 3), (sx + w - 4, sy + h // 3), 2)
        elif fname == "mesa":
            pygame.draw.rect(surface, fcolor, rect, border_radius=3)
            pygame.draw.rect(surface, (max(0, fcolor[0]-30), max(0, fcolor[1]-30),
                                        max(0, fcolor[2]-30)), rect, 2, border_radius=3)
        elif fname == "silla":
            pygame.draw.rect(surface, fcolor, rect, border_radius=2)
            pygame.draw.rect(surface, (max(0, fcolor[0]-25), max(0, fcolor[1]-25),
                                        max(0, fcolor[2]-25)), rect, 2, border_radius=2)
            pygame.draw.rect(surface, (max(0, fcolor[0]-15), max(0, fcolor[1]-15),
                                        max(0, fcolor[2]-15)),
                             (sx + 4, sy + 2, w - 8, 8), border_radius=2)
        elif fname == "tina":
            pygame.draw.rect(surface, fcolor, rect, border_radius=6)
            inner = rect.inflate(-10, -10)
            pygame.draw.rect(surface, TUB_INNER, inner, border_radius=4)
            pygame.draw.rect(surface, (150, 190, 210), rect, 2, border_radius=6)
        elif fname == "retrete":
            pygame.draw.rect(surface, fcolor, rect, border_radius=8)
            pygame.draw.rect(surface, (200, 200, 200), rect, 2, border_radius=8)
            pygame.draw.ellipse(surface, (230, 230, 235),
                                (sx + 6, sy + 6, w - 16, h - 12))
        elif fname == "lavabo":
            pygame.draw.rect(surface, fcolor, rect, border_radius=4)
            pygame.draw.rect(surface, (170, 170, 180), rect, 2, border_radius=4)
            pygame.draw.circle(surface, (150, 155, 160),
                               (sx + TILE_SIZE // 2, sy + 10), 4)
        elif fname == "sofá":
            pygame.draw.rect(surface, fcolor, rect, border_radius=5)
            pygame.draw.rect(surface, (max(0, fcolor[0]-30), max(0, fcolor[1]-30),
                                        max(0, fcolor[2]-30)), rect, 2, border_radius=5)
            for i in range(1, fw):
                lx = sx + i * TILE_SIZE
                pygame.draw.line(surface, (max(0, fcolor[0]-20), max(0, fcolor[1]-20),
                                            max(0, fcolor[2]-20)),
                                 (lx, sy + 4), (lx, sy + h - 4), 1)
        elif fname == "TV":
            pygame.draw.rect(surface, fcolor, rect, border_radius=2)
            screen_r = rect.inflate(-8, -8)
            pygame.draw.rect(surface, TV_SCREEN, screen_r, border_radius=2)
            pygame.draw.line(surface, (60, 80, 100),
                             (screen_r.left + 3, screen_r.top + 3),
                             (screen_r.left + 10, screen_r.top + 3), 1)
        elif fname == "sillón":
            pygame.draw.rect(surface, fcolor, rect, border_radius=4)
            pygame.draw.rect(surface, (max(0, fcolor[0]-25), max(0, fcolor[1]-25),
                                        max(0, fcolor[2]-25)), rect, 2, border_radius=4)
        elif fname == "cajas":
            pygame.draw.rect(surface, fcolor, rect, border_radius=2)
            pygame.draw.rect(surface, (max(0, fcolor[0]-30), max(0, fcolor[1]-30),
                                        max(0, fcolor[2]-30)), rect, 2, border_radius=2)
            pygame.draw.line(surface, BOX_TAPE,
                             (sx + w // 2, sy + 2), (sx + w // 2, sy + h - 2), 2)
            pygame.draw.line(surface, BOX_TAPE,
                             (sx + 2, sy + h // 2), (sx + w - 2, sy + h // 2), 2)
        else:
            pygame.draw.rect(surface, fcolor, rect, border_radius=2)
            pygame.draw.rect(surface, DARK_GRAY, rect, 1, border_radius=2)


def get_walkable_tiles():
    """
    Retorna una lista de posiciones (col, row) donde se pueden colocar libros.
    Excluye paredes, muebles, y la posición inicial del jugador.
    Los libros aparecen dentro de la casa Y en el patio.
    """
    walkable = []
    player_start = (PLAYER_START_COL, PLAYER_START_ROW)

    for row in range(MAP_ROWS):
        for col in range(MAP_COLS):
            tile = HOUSE_MAP[row][col]
            # Piso interior y patio (no paredes, no búnker)
            if tile in (TILE_FLOOR, TILE_PATIO) and (col, row) != player_start:
                if (col, row) not in FURNITURE_BLOCKED:
                    walkable.append((col, row))
    return walkable


# ============================================
#  FASE DE LA CASA (PANTALLA 2)
# ============================================
class HousePhase:
    """
    Fase de recolección: el jugador explora la casa,
    recoge libros y debe llegar al búnker en 30 segundos.
    Incluye: countdown, gas tóxico, congelamiento + fade a negro.
    """

    def __init__(self, sound_manager):
        self.sound_manager = sound_manager
        self.reset()

    def reset(self):
        """Reinicia la fase de la casa."""
        # Jugador: inicia en la puerta principal (abajo centro)
        start_x = PLAYER_START_COL * TILE_SIZE + TILE_SIZE // 2
        start_y = PLAYER_START_ROW * TILE_SIZE + TILE_SIZE // 2
        self.player = Player(start_x, start_y)
        self.camera = Camera()
        self.inventory = Inventory()

        # Temporizador de 30 segundos
        self.timer = 30.0
        self.timer_flash = 0

        # === COUNTDOWN ("Comenzar") ===
        self.countdown_phase = "freeze"  # "freeze" → "show_text" → "done"
        self.countdown_timer = 1.0
        self.game_started = False

        # === CONGELAMIENTO + FADE A NEGRO ===
        self.freeze_on_timeout = False
        self.freeze_timer = FREEZE_DURATION
        self.timeout_done = False  # Ya se mostró la pantalla de timeout

        # Generar libros en posiciones aleatorias DENTRO de la casa
        self.books = []
        walkable = get_walkable_tiles()
        random.shuffle(walkable)

        book_list = (["green"] * 2 + ["red"] * 2 +
                     ["blue"] * 2 + ["purple"] * 2)
        for i, color in enumerate(book_list):
            if i < len(walkable):
                col, row = walkable[i]
                bx = col * TILE_SIZE + TILE_SIZE // 2
                by = row * TILE_SIZE + TILE_SIZE // 2
                self.books.append(Book(bx, by, color))

        # Estado
        self.finished = False
        self.result = None

        # Sonido de pasos
        self.step_timer = 0
        self.step_interval = 0.25

        # Bunker cercano
        self.near_bunker = False

        # Fuentes
        self.font_timer = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 16)
        self.font_label = pygame.font.SysFont("Arial", 12)
        self.font_large = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 22)
        self.font_countdown = pygame.font.SysFont("Arial", 72, bold=True)

    def update(self, events, dt):
        """
        Actualiza la lógica de la fase de la casa.
        Retorna una tupla (next_state, data) cuando termine, o None.
        """
        # === CONGELAMIENTO → FADE A NEGRO → PANTALLA TIMEOUT ===
        if self.freeze_on_timeout:
            self.freeze_timer -= dt
            if self.freeze_timer <= 0:
                # Ir directamente al EndScreen de TIMEOUT (una sola pantalla)
                return (STATE_ENDING, ENDING_TIMEOUT)
            return None

        # === COUNTDOWN INICIAL ===
        if not self.game_started:
            self.countdown_timer -= dt
            if self.countdown_phase == "freeze":
                if self.countdown_timer <= 0:
                    self.countdown_phase = "show_text"
                    self.countdown_timer = 1.0
            elif self.countdown_phase == "show_text":
                if self.countdown_timer <= 0:
                    self.countdown_phase = "done"
                    self.game_started = True
            self.camera.update(self.player.x, self.player.y)
            return None

        # === LÓGICA NORMAL DEL JUEGO ===
        self.timer -= dt
        self.timer_flash += dt
        if self.timer <= 0:
            self.timer = 0
            # Congelar 3 segundos con fade a negro
            self.freeze_on_timeout = True
            self.freeze_timer = FREEZE_DURATION
            self.sound_manager.play("error")
            return None

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        dx, dy = self.player.handle_input(keys)
        self.player.try_move(dx, dy)
        self.player.update(dt)

        # Sonido de pasos
        if self.player.moving:
            self.step_timer += dt
            if self.step_timer >= self.step_interval:
                self.sound_manager.play("pasos")
                self.step_timer = 0
        else:
            self.step_timer = 0

        # Actualizar cámara
        self.camera.update(self.player.x, self.player.y)

        # Actualizar libros
        for book in self.books:
            book.update(dt)

        # Procesar eventos
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                # Recoger libro
                for book in self.books:
                    if not book.collected and book.distance_to(
                            self.player.x, self.player.y) < PICKUP_DISTANCE:
                        book.collected = True
                        self.inventory.add_book(book.color_name)
                        self.sound_manager.play("recoger")
                        break

                # Entrar al búnker
                bunker_x = BUNKER_COL * TILE_SIZE + TILE_SIZE // 2
                bunker_y = BUNKER_ROW * TILE_SIZE + TILE_SIZE // 2
                dist = math.sqrt((self.player.x - bunker_x) ** 2 +
                                 (self.player.y - bunker_y) ** 2)
                if dist < TILE_SIZE:
                    self.sound_manager.play("select")
                    return (STATE_BUNKER, self.inventory.get_books())

        # Cercanía al búnker
        bunker_x = BUNKER_COL * TILE_SIZE + TILE_SIZE // 2
        bunker_y = BUNKER_ROW * TILE_SIZE + TILE_SIZE // 2
        self.near_bunker = (math.sqrt((self.player.x - bunker_x) ** 2 +
                                      (self.player.y - bunker_y) ** 2) < TILE_SIZE)

        return None

    def draw(self, surface):
        """Dibuja toda la fase de la casa."""
        cam_x = self.camera.x
        cam_y = self.camera.y

        surface.fill(BLACK)

        # Mapa y muebles
        draw_map(surface, cam_x, cam_y)
        draw_furniture(surface, cam_x, cam_y)

        # Libros
        for book in self.books:
            book.draw(surface, cam_x, cam_y, self.player.x, self.player.y)

        # Indicador [E] búnker
        if self.near_bunker and self.game_started:
            bx = int(BUNKER_COL * TILE_SIZE + TILE_SIZE // 2 - cam_x)
            by = int(BUNKER_ROW * TILE_SIZE - cam_y)
            font = pygame.font.SysFont("Arial", 16, bold=True)
            text = font.render("[E] Entrar al búnker", True, (255, 255, 100))
            text_rect = text.get_rect(center=(bx, by - 10))
            bg = text_rect.inflate(8, 4)
            s = pygame.Surface((bg.width, bg.height), pygame.SRCALPHA)
            s.fill((0, 0, 0, 160))
            surface.blit(s, bg.topleft)
            pygame.draw.rect(surface, (255, 255, 100), bg, 1, border_radius=3)
            surface.blit(text, text_rect)

        # Jugador
        self.player.draw(surface, cam_x, cam_y)

        # HUD (solo si el juego ha empezado)
        if self.game_started:
            self._draw_timer(surface)
            self.inventory.draw(surface)
            self._draw_room_label(surface)

        # === EFECTO DE GAS TÓXICO (últimos 7 segundos) ===
        if self.game_started and 0 < self.timer <= GAS_START_TIME:
            gas_intensity = 1.0 - (self.timer / GAS_START_TIME)  # 0.0 → 1.0
            gas_alpha = int(gas_intensity * 150)
            gas_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            gas_surface.fill((0, 180, 0, gas_alpha))
            surface.blit(gas_surface, (0, 0))

        # === CONGELAMIENTO + FADE A NEGRO ===
        if self.freeze_on_timeout:
            # Progreso del fade: 0 (justo empezó) → 1 (terminó)
            fade_progress = 1.0 - (self.freeze_timer / FREEZE_DURATION)

            # Gas verde al máximo + fade a negro progresivo
            gas_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            gas_surface.fill((0, 180, 0, 150))
            surface.blit(gas_surface, (0, 0))

            # Overlay negro que se intensifica
            black_alpha = int(fade_progress * 255)
            black_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            black_surface.fill((0, 0, 0, black_alpha))
            surface.blit(black_surface, (0, 0))

        # === COUNTDOWN INICIAL ===
        if not self.game_started:
            self._draw_countdown(surface)

    def _draw_countdown(self, surface):
        """Dibuja el countdown ('Comenzar') al inicio."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        surface.blit(overlay, (0, 0))

        if self.countdown_phase == "show_text":
            text = self.font_countdown.render("¡COMENZAR!", True, (255, 255, 100))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

            # Sombra
            shadow = self.font_countdown.render("¡COMENZAR!", True, (0, 0, 0))
            surface.blit(shadow, (text_rect.x + 3, text_rect.y + 3))
            surface.blit(text, text_rect)

            sub = self.font_medium.render("Recoge los libros y entra al búnker",
                                           True, WHITE)
            surface.blit(sub, sub.get_rect(center=(SCREEN_WIDTH // 2,
                                                     SCREEN_HEIGHT // 2 + 55)))

    def _draw_timer(self, surface):
        """Dibuja el temporizador."""
        timer_bg = pygame.Surface((140, 45), pygame.SRCALPHA)
        timer_bg.fill((20, 20, 30, 200))
        surface.blit(timer_bg, (SCREEN_WIDTH - 150, 10))
        pygame.draw.rect(surface, (100, 100, 120),
                         (SCREEN_WIDTH - 150, 10, 140, 45), 2, border_radius=5)

        seconds = max(0, int(self.timer))
        millis = int((self.timer - int(self.timer)) * 100)

        if self.timer <= 10:
            flash = int(self.timer_flash * 4) % 2 == 0
            color = TIMER_COLOR if flash else (255, 150, 150)
        else:
            color = WHITE

        time_str = f"{seconds:02d}.{millis:02d}"
        timer_text = self.font_timer.render(time_str, True, color)
        timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH - 80, 32))
        surface.blit(timer_text, timer_rect)

        label = self.font_small.render("⏱ TIEMPO", True, LIGHT_GRAY)
        surface.blit(label, (SCREEN_WIDTH - 145, 12))

    def _draw_room_label(self, surface):
        """Muestra el nombre de la habitación actual."""
        col = int(self.player.x // TILE_SIZE)
        row = int(self.player.y // TILE_SIZE)
        room_name = get_room_name(col, row)

        if room_name:
            label_surface = pygame.Surface((140, 25), pygame.SRCALPHA)
            label_surface.fill((20, 20, 30, 160))
            surface.blit(label_surface, (10, 10))
            pygame.draw.rect(surface, (80, 80, 100), (10, 10, 140, 25), 1, border_radius=3)
            text = self.font_small.render(f"📍 {room_name}", True, WHITE)
            surface.blit(text, (18, 13))
