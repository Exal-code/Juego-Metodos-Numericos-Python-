# ============================================
# entities.py - Entidades del juego
# ============================================
# Player, Book, Camera, Inventory, TextInput

import pygame
import math
from config import (
    TILE_SIZE, MAP_WIDTH, MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT,
    PLAYER_SPEED, PICKUP_DISTANCE, PLAYER_SKIN, PLAYER_SHIRT,
    PLAYER_PANTS, PLAYER_CAP, PLAYER_BACKPACK, PLAYER_HAIR, PLAYER_EYE,
    BOOK_COLORS, INVENTORY_BG, INVENTORY_BORDER, WHITE, BLACK,
    LIGHT_GRAY, DARK_GRAY, INPUT_BG, INPUT_BORDER, INPUT_ACTIVE, INPUT_TEXT,
    HOUSE_MAP, FURNITURE_BLOCKED, TILE_WALL, TILE_SIZE,
)


# ============================================
#  JUGADOR
# ============================================
class Player:
    """
    Personaje del jugador estilo Ash Ketchum.
    Se dibuja con primitivas de Pygame.
    4 direcciones × 2 frames de caminata.
    """

    # Direcciones
    DOWN, LEFT, RIGHT, UP = 0, 1, 2, 3

    def __init__(self, x, y):
        # Posición en píxeles (centro del personaje)
        self.x = x
        self.y = y
        self.direction = self.DOWN
        self.frame = 0
        self.frame_timer = 0
        self.moving = False
        # Tamaño del hitbox para colisiones (más pequeño que el sprite)
        self.hitbox_half = 10

    def handle_input(self, keys):
        """Procesa las teclas de movimiento (WASD / flechas)."""
        dx, dy = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -PLAYER_SPEED
            self.direction = self.LEFT
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = PLAYER_SPEED
            self.direction = self.RIGHT

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -PLAYER_SPEED
            self.direction = self.UP
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = PLAYER_SPEED
            self.direction = self.DOWN

        self.moving = dx != 0 or dy != 0
        return dx, dy

    def try_move(self, dx, dy):
        """
        Intenta mover al jugador en dx, dy.
        Verifica colisiones separadamente en X e Y para permitir deslizarse
        por las paredes.
        """
        # Movimiento en X
        if dx != 0:
            new_x = self.x + dx
            if self._can_move(new_x, self.y):
                self.x = new_x

        # Movimiento en Y
        if dy != 0:
            new_y = self.y + dy
            if self._can_move(self.x, new_y):
                self.y = new_y

    def _can_move(self, x, y):
        """Verifica si la posición (x, y) es válida (sin colisiones)."""
        h = self.hitbox_half
        # Verificar las 4 esquinas del hitbox
        corners = [
            (x - h, y - h),
            (x + h, y - h),
            (x - h, y + h),
            (x + h, y + h),
        ]
        for cx, cy in corners:
            col = int(cx // TILE_SIZE)
            row = int(cy // TILE_SIZE)
            # Fuera del mapa = bloquear
            if col < 0 or col >= len(HOUSE_MAP[0]) or row < 0 or row >= len(HOUSE_MAP):
                return False
            # Pared = bloquear
            if HOUSE_MAP[row][col] == TILE_WALL:
                return False
            # Mueble = bloquear
            if (col, row) in FURNITURE_BLOCKED:
                return False
        return True

    def update(self, dt):
        """Actualiza la animación del personaje."""
        if self.moving:
            self.frame_timer += dt
            if self.frame_timer > 0.15:  # Cambiar frame cada 150ms
                self.frame = 1 - self.frame  # Alternar entre 0 y 1
                self.frame_timer = 0
        else:
            self.frame = 0
            self.frame_timer = 0

    def draw(self, surface, cam_x, cam_y):
        """
        Dibuja el personaje en pantalla.
        Estilo Ash: gorra roja, camiseta azul, mochila.
        """
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)

        # Offset de piernas para animación de caminata
        leg_offset = 3 if self.frame == 1 else 0

        if self.direction == self.DOWN:
            self._draw_front(surface, sx, sy, leg_offset)
        elif self.direction == self.UP:
            self._draw_back(surface, sx, sy, leg_offset)
        elif self.direction == self.LEFT:
            self._draw_side(surface, sx, sy, leg_offset, flip=True)
        elif self.direction == self.RIGHT:
            self._draw_side(surface, sx, sy, leg_offset, flip=False)

    def _draw_front(self, surface, sx, sy, leg_off):
        """Vista frontal (mirando abajo)."""
        # Piernas
        pygame.draw.rect(surface, PLAYER_PANTS, (sx - 6, sy + 6, 5, 10 + leg_off))
        pygame.draw.rect(surface, PLAYER_PANTS, (sx + 1, sy + 6, 5, 10 - leg_off))
        # Cuerpo
        pygame.draw.rect(surface, PLAYER_SHIRT, (sx - 8, sy - 4, 16, 12))
        # Brazos
        pygame.draw.rect(surface, PLAYER_SKIN, (sx - 10, sy - 2, 3, 8))
        pygame.draw.rect(surface, PLAYER_SKIN, (sx + 7, sy - 2, 3, 8))
        # Cabeza
        pygame.draw.circle(surface, PLAYER_SKIN, (sx, sy - 10), 8)
        # Ojos
        pygame.draw.circle(surface, PLAYER_EYE, (sx - 3, sy - 11), 2)
        pygame.draw.circle(surface, PLAYER_EYE, (sx + 3, sy - 11), 2)
        # Gorra
        pygame.draw.rect(surface, PLAYER_CAP, (sx - 8, sy - 18, 16, 5))
        pygame.draw.rect(surface, PLAYER_CAP, (sx - 10, sy - 14, 20, 3))
        # Mochila (visible en los lados)
        pygame.draw.rect(surface, PLAYER_BACKPACK, (sx - 12, sy - 3, 4, 8))

    def _draw_back(self, surface, sx, sy, leg_off):
        """Vista trasera (mirando arriba)."""
        # Piernas
        pygame.draw.rect(surface, PLAYER_PANTS, (sx - 6, sy + 6, 5, 10 - leg_off))
        pygame.draw.rect(surface, PLAYER_PANTS, (sx + 1, sy + 6, 5, 10 + leg_off))
        # Cuerpo
        pygame.draw.rect(surface, PLAYER_SHIRT, (sx - 8, sy - 4, 16, 12))
        # Mochila (visible por detrás)
        pygame.draw.rect(surface, PLAYER_BACKPACK, (sx - 6, sy - 2, 12, 10))
        pygame.draw.rect(surface, (100, 50, 10), (sx - 5, sy, 10, 6))  # detalle
        # Cabeza
        pygame.draw.circle(surface, PLAYER_HAIR, (sx, sy - 10), 8)
        # Gorra
        pygame.draw.rect(surface, PLAYER_CAP, (sx - 8, sy - 18, 16, 5))
        # Brazos
        pygame.draw.rect(surface, PLAYER_SKIN, (sx - 10, sy - 2, 3, 8))
        pygame.draw.rect(surface, PLAYER_SKIN, (sx + 7, sy - 2, 3, 8))

    def _draw_side(self, surface, sx, sy, leg_off, flip):
        """Vista lateral (izquierda o derecha)."""
        m = -1 if flip else 1  # Multiplicador de espejo

        # Piernas
        pygame.draw.rect(surface, PLAYER_PANTS, (sx - 4, sy + 6, 4, 10 + leg_off))
        pygame.draw.rect(surface, PLAYER_PANTS, (sx, sy + 6, 4, 10 - leg_off))
        # Cuerpo
        pygame.draw.rect(surface, PLAYER_SHIRT, (sx - 6, sy - 4, 12, 12))
        # Brazo visible
        pygame.draw.rect(surface, PLAYER_SKIN, (sx + m * 5, sy - 1, 3, 8))
        # Mochila (en el lado trasero)
        pygame.draw.rect(surface, PLAYER_BACKPACK, (sx - m * 6, sy - 2, 5, 9))
        # Cabeza
        pygame.draw.circle(surface, PLAYER_SKIN, (sx, sy - 10), 8)
        # Ojo
        pygame.draw.circle(surface, PLAYER_EYE, (sx + m * 3, sy - 11), 2)
        # Gorra
        pygame.draw.rect(surface, PLAYER_CAP, (sx - 6, sy - 18, 12, 5))
        pygame.draw.rect(surface, PLAYER_CAP, (sx + m * 4, sy - 14, 8 * m, 3) if m > 0
                         else (sx - 12, sy - 14, 8, 3))

    def get_rect(self):
        """Retorna el rectángulo del hitbox del jugador."""
        h = self.hitbox_half
        return pygame.Rect(self.x - h, self.y - h, h * 2, h * 2)


# ============================================
#  LIBRO
# ============================================
class Book:
    """Un libro recogible en el mapa de la casa."""

    def __init__(self, x, y, color_name):
        self.x = x  # Posición central en píxeles
        self.y = y
        self.color_name = color_name  # "green", "red", "blue", "purple"
        self.color = BOOK_COLORS[color_name]
        self.collected = False
        self.bob_timer = 0  # Para animación de flotación

    def update(self, dt):
        """Actualiza la animación de flotación."""
        self.bob_timer += dt

    def distance_to(self, px, py):
        """Distancia al punto (px, py)."""
        return math.sqrt((self.x - px) ** 2 + (self.y - py) ** 2)

    def draw(self, surface, cam_x, cam_y, player_x, player_y):
        """
        Dibuja el libro en pantalla.
        Muestra icono [E] si el jugador está cerca.
        """
        if self.collected:
            return

        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)

        # Pequeña animación de flotación
        bob = math.sin(self.bob_timer * 3) * 2

        # Sombra
        pygame.draw.ellipse(surface, (0, 0, 0, 80),
                            (sx - 8, sy + 8, 16, 6))

        # Libro (rectángulo con borde)
        book_rect = pygame.Rect(sx - 8, sy - 10 + bob, 16, 20)
        pygame.draw.rect(surface, self.color, book_rect)
        pygame.draw.rect(surface, (max(0, self.color[0] - 40),
                                    max(0, self.color[1] - 40),
                                    max(0, self.color[2] - 40)), book_rect, 2)
        # Líneas del libro (páginas)
        pygame.draw.line(surface, WHITE, (sx - 6, sy - 6 + bob), (sx + 6, sy - 6 + bob), 1)
        pygame.draw.line(surface, WHITE, (sx - 6, sy - 2 + bob), (sx + 6, sy - 2 + bob), 1)
        pygame.draw.line(surface, WHITE, (sx - 6, sy + 2 + bob), (sx + 6, sy + 2 + bob), 1)

        # Mostrar [E] si el jugador está cerca
        dist = self.distance_to(player_x, player_y)
        if dist < PICKUP_DISTANCE:
            # Fondo del icono
            font = pygame.font.SysFont("Arial", 16, bold=True)
            text = font.render("[E]", True, (255, 255, 100))
            text_rect = text.get_rect(center=(sx, sy - 24 + bob))
            bg_rect = text_rect.inflate(6, 4)
            pygame.draw.rect(surface, (0, 0, 0, 180), bg_rect, border_radius=3)
            pygame.draw.rect(surface, (255, 255, 100), bg_rect, 1, border_radius=3)
            surface.blit(text, text_rect)


# ============================================
#  CÁMARA
# ============================================
class Camera:
    """Cámara que sigue al jugador con suavizado."""

    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, target_x, target_y):
        """
        Centra la cámara en el jugador.
        Clampea para no mostrar fuera del mapa.
        """
        # Centrar en el objetivo
        target_cam_x = target_x - SCREEN_WIDTH // 2
        target_cam_y = target_y - SCREEN_HEIGHT // 2

        # Suavizado (lerp)
        self.x += (target_cam_x - self.x) * 0.15
        self.y += (target_cam_y - self.y) * 0.15

        # Clampear a los bordes del mapa
        self.x = max(0, min(self.x, MAP_WIDTH - SCREEN_WIDTH))
        self.y = max(0, min(self.y, MAP_HEIGHT - SCREEN_HEIGHT))

    def apply(self, x, y):
        """Convierte coordenadas del mundo a coordenadas de pantalla."""
        return int(x - self.x), int(y - self.y)


# ============================================
#  INVENTARIO (estilo Minecraft)
# ============================================
class Inventory:
    """
    Sistema de inventario con 4 casillas estilo Minecraft.
    Las casillas empiezan vacías (transparentes).
    Al recoger un libro, se llena la siguiente casilla disponible.
    Si se recoge otro del mismo color, se incrementa el contador.
    """

    def __init__(self):
        self.books = {"green": 0, "red": 0, "blue": 0, "purple": 0}
        # Orden de los slots: se llenan de izquierda a derecha
        self.slot_order = []  # Lista de color_names en orden de recolección

    def add_book(self, color_name):
        """Agrega un libro al inventario."""
        if color_name in self.books:
            self.books[color_name] += 1
            # Agregar al orden de slots si es la primera vez
            if color_name not in self.slot_order:
                self.slot_order.append(color_name)

    def get_total(self):
        """Retorna el total de libros recogidos."""
        return sum(self.books.values())

    def get_books(self):
        """Retorna el diccionario de libros."""
        return dict(self.books)

    def reset(self):
        """Reinicia el inventario."""
        self.books = {"green": 0, "red": 0, "blue": 0, "purple": 0}
        self.slot_order = []

    def draw(self, surface):
        """Dibuja la barra de inventario estilo Minecraft."""
        slot_size = 48
        slot_gap = 4
        num_slots = 4
        total_width = num_slots * slot_size + (num_slots - 1) * slot_gap
        start_x = (SCREEN_WIDTH - total_width) // 2
        start_y = SCREEN_HEIGHT - slot_size - 8

        font_count = pygame.font.SysFont("Arial", 14, bold=True)

        for i in range(num_slots):
            slot_x = start_x + i * (slot_size + slot_gap)
            slot_y = start_y
            slot_rect = pygame.Rect(slot_x, slot_y, slot_size, slot_size)

            if i < len(self.slot_order):
                # === Casilla con libro ===
                color_name = self.slot_order[i]
                count = self.books[color_name]
                book_color = BOOK_COLORS[color_name]

                # Fondo semi-transparente
                slot_surf = pygame.Surface((slot_size, slot_size), pygame.SRCALPHA)
                slot_surf.fill((30, 30, 40, 180))
                surface.blit(slot_surf, (slot_x, slot_y))

                # Borde del color del libro
                pygame.draw.rect(surface, book_color, slot_rect, 2, border_radius=4)

                # Dibujar libro dentro del slot
                bx = slot_x + 10
                by = slot_y + 8
                bw = 28
                bh = 32

                # Libro (rectángulo de color)
                book_rect = pygame.Rect(bx, by, bw, bh)
                pygame.draw.rect(surface, book_color, book_rect, border_radius=3)
                darker = (max(0, book_color[0]-50), max(0, book_color[1]-50),
                          max(0, book_color[2]-50))
                pygame.draw.rect(surface, darker, book_rect, 2, border_radius=3)

                # Líneas de páginas
                for j in range(3):
                    ly = by + 8 + j * 8
                    pygame.draw.line(surface, (240, 240, 240),
                                     (bx + 4, ly), (bx + bw - 4, ly), 1)

                # Lomo del libro
                pygame.draw.rect(surface, darker, (bx, by, 4, bh), border_radius=1)

                # Número de libros (arriba a la derecha del slot)
                if count > 0:
                    count_text = font_count.render(str(count), True, WHITE)
                    count_rect = count_text.get_rect()
                    cx = slot_x + slot_size - count_rect.width - 3
                    cy = slot_y + 2

                    # Fondo del número
                    bg = count_rect.inflate(4, 2)
                    bg.topleft = (cx - 2, cy - 1)
                    bg_surf = pygame.Surface((bg.width, bg.height), pygame.SRCALPHA)
                    bg_surf.fill((0, 0, 0, 180))
                    surface.blit(bg_surf, bg.topleft)
                    surface.blit(count_text, (cx, cy))

            else:
                # === Casilla vacía (transparente) ===
                slot_surf = pygame.Surface((slot_size, slot_size), pygame.SRCALPHA)
                slot_surf.fill((50, 50, 60, 60))  # Muy transparente
                surface.blit(slot_surf, (slot_x, slot_y))

                # Borde sutil
                pygame.draw.rect(surface, (100, 100, 120, 80), slot_rect, 2, border_radius=4)


# ============================================
#  CAMPO DE TEXTO (TextInput)
# ============================================
class TextInput:
    """
    Campo de entrada de texto simple.
    Admite números, punto decimal, signo negativo.
    """

    def __init__(self, x, y, width, height, font_size=22):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.active = True
        self.font = pygame.font.SysFont("Consolas", font_size)
        self.cursor_visible = True
        self.cursor_timer = 0
        self.max_length = 20

    def handle_event(self, event):
        """Procesa un evento de teclado."""
        if not self.active:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_DELETE:
                self.text = ""
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return "submit"
            else:
                char = event.unicode
                # Solo permitir números, punto, signo negativo, y espacio
                if char and len(self.text) < self.max_length:
                    if char in "0123456789.-+ ":
                        self.text += char
        return None

    def update(self, dt):
        """Actualiza el parpadeo del cursor."""
        self.cursor_timer += dt
        if self.cursor_timer > 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def get_value(self):
        """Retorna el texto ingresado."""
        return self.text.strip()

    def get_numeric_value(self):
        """Intenta convertir el texto a número. Retorna None si falla."""
        try:
            return float(self.text.strip())
        except (ValueError, TypeError):
            return None

    def clear(self):
        """Limpia el campo."""
        self.text = ""

    def draw(self, surface):
        """Dibuja el campo de texto."""
        # Fondo
        pygame.draw.rect(surface, INPUT_BG, self.rect, border_radius=5)

        # Borde (color cambia si está activo)
        border_color = INPUT_ACTIVE if self.active else INPUT_BORDER
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=5)

        # Texto
        text_surface = self.font.render(self.text, True, INPUT_TEXT)
        text_rect = text_surface.get_rect(
            midleft=(self.rect.x + 10, self.rect.centery)
        )
        # Clipear el texto al rectángulo
        clip_rect = self.rect.inflate(-10, -4)
        surface.set_clip(clip_rect)
        surface.blit(text_surface, text_rect)
        surface.set_clip(None)

        # Cursor
        if self.active and self.cursor_visible:
            cursor_x = text_rect.right + 2
            if cursor_x > self.rect.right - 10:
                cursor_x = self.rect.right - 10
            pygame.draw.line(surface, INPUT_TEXT,
                             (cursor_x, self.rect.y + 6),
                             (cursor_x, self.rect.bottom - 6), 2)
