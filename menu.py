# ============================================
# menu.py - Menú principal y pantallas finales
# ============================================

import pygame
import math
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    MENU_BG_TOP, MENU_BG_BOT, MENU_SELECTED, MENU_NORMAL,
    MENU_TITLE, MENU_SUBTITLE,
    WOOD_COLOR, WOOD_DARK, WOOD_LIGHT,
    WHITE, BLACK, DARK_GRAY, LIGHT_GRAY,
    STATE_HOUSE, STATE_MENU,
    ENDING_PERFECT, ENDING_PARTIAL, ENDING_FAILURE, ENDING_TIMEOUT,
    BUTTON_GREEN, BUTTON_GREEN_HOVER,
    WALL_COLOR, WALL_TOP_COLOR,
    FLOOR_PATIO,
)


# ============================================
#  MENÚ PRINCIPAL
# ============================================
class MainMenu:
    """
    Pantalla del menú principal con:
    - Fondo de casa
    - Letrero de madera con opciones
    - Sub-pantallas: Controles, Opciones, Créditos
    """

    OPTIONS = ["Juego Nuevo", "Controles", "Opciones", "Créditos", "Salir"]

    def __init__(self, sound_manager):
        self.sound_manager = sound_manager
        self.selected = 0
        self.sub_screen = None  # "controls", "options", "credits"

        # Fuentes
        self.font_title = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_subtitle = pygame.font.SysFont("Arial", 18)
        self.font_option = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_text = pygame.font.SysFont("Arial", 17)
        self.font_small = pygame.font.SysFont("Arial", 14)
        self.font_key = pygame.font.SysFont("Consolas", 16, bold=True)

        # Animación
        self.time = 0

    def update(self, events, dt):
        """
        Procesa eventos del menú.
        Retorna: "new_game" para iniciar, "quit" para salir, o None.
        """
        self.time += dt

        # Sub-pantallas
        if self.sub_screen:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_e):
                        self.sound_manager.play("select")
                        if self.sub_screen == "options":
                            pass  # toggle se maneja con clic
                        self.sub_screen = None
                        return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    # Botón volver (siempre presente en sub-pantallas)
                    back_btn = pygame.Rect(SCREEN_WIDTH // 2 - 80,
                                           SCREEN_HEIGHT - 80, 160, 40)
                    if back_btn.collidepoint(mouse):
                        self.sound_manager.play("select")
                        self.sub_screen = None
                        return None

                    # Toggle de sonido en opciones
                    if self.sub_screen == "options":
                        sound_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100,
                                                 SCREEN_HEIGHT // 2 - 20, 200, 45)
                        if sound_btn.collidepoint(mouse):
                            self.sound_manager.toggle()
                            self.sound_manager.play("select")
            return None

        # Menú principal
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected = (self.selected - 1) % len(self.OPTIONS)
                    self.sound_manager.play("select")
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected = (self.selected + 1) % len(self.OPTIONS)
                    self.sound_manager.play("select")
                elif event.key in (pygame.K_RETURN, pygame.K_e):
                    return self._select_option()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # Verificar clic en opciones del letrero
                for i in range(len(self.OPTIONS)):
                    opt_y = 265 + i * 50
                    opt_rect = pygame.Rect(SCREEN_WIDTH // 2 - 140,
                                            opt_y - 5, 280, 40)
                    if opt_rect.collidepoint(mouse):
                        self.selected = i
                        self.sound_manager.play("select")
                        return self._select_option()

            if event.type == pygame.MOUSEMOTION:
                mouse = pygame.mouse.get_pos()
                for i in range(len(self.OPTIONS)):
                    opt_y = 265 + i * 50
                    opt_rect = pygame.Rect(SCREEN_WIDTH // 2 - 140,
                                            opt_y - 5, 280, 40)
                    if opt_rect.collidepoint(mouse):
                        if self.selected != i:
                            self.selected = i

        return None

    def _select_option(self):
        """Ejecuta la opción seleccionada."""
        option = self.OPTIONS[self.selected]
        if option == "Juego Nuevo":
            return "new_game"
        elif option == "Controles":
            self.sub_screen = "controls"
        elif option == "Opciones":
            self.sub_screen = "options"
        elif option == "Créditos":
            self.sub_screen = "credits"
        elif option == "Salir":
            return "quit"
        return None

    def draw(self, surface):
        """Dibuja la pantalla del menú."""
        if self.sub_screen:
            self._draw_sub_screen(surface)
            return

        self._draw_main_menu(surface)

    def _draw_main_menu(self, surface):
        """Dibuja el menú principal con fondo de casa y letrero."""
        # --- Fondo degradado (cielo nocturno) ---
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(MENU_BG_TOP[0] * (1 - t) + MENU_BG_BOT[0] * t)
            g = int(MENU_BG_TOP[1] * (1 - t) + MENU_BG_BOT[1] * t)
            b = int(MENU_BG_TOP[2] * (1 - t) + MENU_BG_BOT[2] * t)
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # --- Estrellas (puntos blancos) ---
        import random
        random.seed(42)  # Estrellas fijas
        for _ in range(50):
            sx = random.randint(0, SCREEN_WIDTH)
            sy = random.randint(0, SCREEN_HEIGHT // 3)
            brightness = random.randint(150, 255)
            twinkle = int(math.sin(self.time * 2 + sx) * 30)
            b = max(100, min(255, brightness + twinkle))
            surface.set_at((sx, sy), (b, b, b))
        random.seed()

        # --- Casa (fondo decorativo) ---
        house_x = SCREEN_WIDTH // 2 - 150
        house_y = SCREEN_HEIGHT - 250

        # Suelo / pasto
        pygame.draw.rect(surface, FLOOR_PATIO,
                         (0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80))

        # Estructura de la casa
        pygame.draw.rect(surface, WALL_COLOR,
                         (house_x, house_y, 300, 170))
        pygame.draw.rect(surface, WALL_TOP_COLOR,
                         (house_x, house_y, 300, 170), 3)

        # Techo
        roof_points = [
            (house_x - 20, house_y),
            (house_x + 150, house_y - 60),
            (house_x + 320, house_y),
        ]
        pygame.draw.polygon(surface, (139, 69, 19), roof_points)
        pygame.draw.polygon(surface, (100, 45, 10), roof_points, 3)

        # Ventanas
        for wx, wy in [(house_x + 30, house_y + 30),
                        (house_x + 200, house_y + 30)]:
            # Ventana
            pygame.draw.rect(surface, (60, 80, 120), (wx, wy, 60, 50))
            pygame.draw.rect(surface, (180, 160, 130), (wx, wy, 60, 50), 3)
            # Cruz de la ventana
            pygame.draw.line(surface, (180, 160, 130),
                             (wx + 30, wy), (wx + 30, wy + 50), 2)
            pygame.draw.line(surface, (180, 160, 130),
                             (wx, wy + 25), (wx + 60, wy + 25), 2)
            # Luz (brillo amarillo)
            glow = pygame.Surface((56, 46), pygame.SRCALPHA)
            glow.fill((255, 240, 180, 40))
            surface.blit(glow, (wx + 2, wy + 2))

        # Puerta
        pygame.draw.rect(surface, (80, 50, 25),
                         (house_x + 120, house_y + 70, 50, 100))
        pygame.draw.rect(surface, (60, 35, 15),
                         (house_x + 120, house_y + 70, 50, 100), 2)
        pygame.draw.circle(surface, (200, 180, 50),
                           (house_x + 160, house_y + 125), 4)

        # --- Título del juego ---
        title = self.font_title.render("30 Segundos", True, MENU_TITLE)
        subtitle = self.font_subtitle.render("Antes de la Tragedia", True, MENU_SUBTITLE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        sub_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 90))

        # Sombra del título
        shadow = self.font_title.render("30 Segundos", True, (0, 0, 0))
        surface.blit(shadow, (title_rect.x + 2, title_rect.y + 2))
        surface.blit(title, title_rect)
        surface.blit(subtitle, sub_rect)

        # --- Letrero de madera ---
        sign_x = SCREEN_WIDTH // 2 - 160
        sign_y = 130
        sign_w = 320
        sign_h = 380

        # Poste
        pygame.draw.rect(surface, WOOD_DARK,
                         (SCREEN_WIDTH // 2 - 8, sign_y + sign_h - 20,
                          16, 100))

        # Tablón principal
        pygame.draw.rect(surface, WOOD_COLOR,
                         (sign_x, sign_y, sign_w, sign_h), border_radius=8)
        pygame.draw.rect(surface, WOOD_DARK,
                         (sign_x, sign_y, sign_w, sign_h), 3, border_radius=8)

        # Textura de madera
        for i in range(sign_y + 10, sign_y + sign_h - 10, 12):
            pygame.draw.line(surface, WOOD_LIGHT,
                             (sign_x + 10, i), (sign_x + sign_w - 10, i), 1)

        # Clavos en las esquinas
        for cx, cy in [(sign_x + 15, sign_y + 15),
                        (sign_x + sign_w - 15, sign_y + 15),
                        (sign_x + 15, sign_y + sign_h - 15),
                        (sign_x + sign_w - 15, sign_y + sign_h - 15)]:
            pygame.draw.circle(surface, (100, 100, 110), (cx, cy), 4)
            pygame.draw.circle(surface, (70, 70, 80), (cx, cy), 4, 1)

        # Etiqueta "MENÚ"
        menu_label = self.font_subtitle.render("— MENÚ —", True, WOOD_DARK)
        surface.blit(menu_label,
                     menu_label.get_rect(center=(SCREEN_WIDTH // 2, sign_y + 30)))

        # --- Opciones del menú ---
        for i, option in enumerate(self.OPTIONS):
            opt_y = 265 + i * 50
            is_selected = i == self.selected

            if is_selected:
                # Fondo de selección
                sel_rect = pygame.Rect(SCREEN_WIDTH // 2 - 130,
                                        opt_y - 2, 260, 38)
                pygame.draw.rect(surface, WOOD_DARK, sel_rect, border_radius=5)

                # Indicador de selección
                arrow = self.font_option.render("▶", True, MENU_SELECTED)
                surface.blit(arrow, (SCREEN_WIDTH // 2 - 120, opt_y + 2))

            color = MENU_SELECTED if is_selected else MENU_NORMAL
            text = self.font_option.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2 + 10, opt_y + 15))
            surface.blit(text, text_rect)

        # --- Instrucciones ---
        hint = self.font_small.render("↑↓ Navegar  │  Enter: Seleccionar",
                                       True, (120, 120, 140))
        surface.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2,
                                                   SCREEN_HEIGHT - 20)))

    def _draw_sub_screen(self, surface):
        """Dibuja una sub-pantalla (controles, opciones, créditos)."""
        # Fondo
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(30 * (1 - t) + 45 * t)
            g = int(30 * (1 - t) + 35 * t)
            b = int(50 * (1 - t) + 55 * t)
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        if self.sub_screen == "controls":
            self._draw_controls(surface)
        elif self.sub_screen == "options":
            self._draw_options(surface)
        elif self.sub_screen == "credits":
            self._draw_credits(surface)

        # Botón volver
        back_btn = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 80, 160, 40)
        mouse = pygame.mouse.get_pos()
        hover = back_btn.collidepoint(mouse)
        b_color = (80, 80, 100) if hover else (60, 60, 80)
        pygame.draw.rect(surface, b_color, back_btn, border_radius=8)
        pygame.draw.rect(surface, WHITE, back_btn, 2, border_radius=8)
        b_text = self.font_option.render("← Volver", True, WHITE)
        surface.blit(b_text, b_text.get_rect(center=back_btn.center))

    def _draw_controls(self, surface):
        """Dibuja la pantalla de controles."""
        title = self.font_title.render("🎮 Controles", True, WHITE)
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))

        controls = [
            ("Movimiento", "W A S D  o  ← ↑ → ↓"),
            ("Recoger libro / Entrar búnker", "Tecla E"),
            ("Entregar respuesta", "Enter o clic en 'Entregar'"),
            ("Interacción en búnker", "Clic del mouse"),
            ("Pausa (en problemas)", "Clic en botón 'Pausa'"),
        ]

        y = 130
        for label, keys in controls:
            # Etiqueta
            label_text = self.font_text.render(label + ":", True, (180, 200, 220))
            surface.blit(label_text, (120, y))

            # Teclas
            key_text = self.font_key.render(keys, True, (255, 215, 0))
            surface.blit(key_text, (140, y + 28))

            # Separador
            pygame.draw.line(surface, (60, 60, 80), (120, y + 55),
                             (SCREEN_WIDTH - 120, y + 55), 1)
            y += 70

    def _draw_options(self, surface):
        """Dibuja la pantalla de opciones."""
        title = self.font_title.render("⚙ Opciones", True, WHITE)
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))

        # Toggle de sonido
        sound_on = self.sound_manager.is_enabled()
        status = "🔊 ACTIVADO" if sound_on else "🔇 DESACTIVADO"
        status_color = (100, 255, 100) if sound_on else (255, 100, 100)

        label = self.font_text.render("Sonido:", True, (180, 200, 220))
        surface.blit(label, label.get_rect(center=(SCREEN_WIDTH // 2,
                                                     SCREEN_HEIGHT // 2 - 60)))

        sound_btn = pygame.Rect(SCREEN_WIDTH // 2 - 100,
                                 SCREEN_HEIGHT // 2 - 20, 200, 45)
        mouse = pygame.mouse.get_pos()
        hover = sound_btn.collidepoint(mouse)
        btn_color = (80, 80, 100) if hover else (60, 60, 80)
        pygame.draw.rect(surface, btn_color, sound_btn, border_radius=8)
        pygame.draw.rect(surface, status_color, sound_btn, 2, border_radius=8)

        s_text = self.font_option.render(status, True, status_color)
        surface.blit(s_text, s_text.get_rect(center=sound_btn.center))

        hint = self.font_small.render("Clic para cambiar", True, LIGHT_GRAY)
        surface.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2,
                                                   SCREEN_HEIGHT // 2 + 45)))

    def _draw_credits(self, surface):
        """Dibuja la pantalla de créditos."""
        title = self.font_title.render("📜 Créditos", True, WHITE)
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))

        credits = [
            "",
            "🎮 30 Segundos Antes de la Tragedia",
            "",
            "Creado por:",
            "Exal Herrera y compañía",
            "",
            "Institución:",
            "FIME",
            "",
            "Materia:",
            "Métodos Numéricos",
            "",
            "Desarrollado con:",
            "Python + Pygame-CE",
        ]

        y = 130
        for line in credits:
            if line == "":
                y += 10
                continue
            # Alternar colores
            if line.startswith("🎮") or line.startswith("Creado") or \
               line.startswith("Institución") or line.startswith("Materia") or \
               line.startswith("Desarrollado"):
                color = (180, 200, 220)
                font = self.font_text
            else:
                color = MENU_SELECTED
                font = self.font_option

            text = font.render(line, True, color)
            surface.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, y)))
            y += 30


# ============================================
#  PANTALLA DE FINAL
# ============================================
class EndScreen:
    """
    Muestra uno de los 4 finales del juego.
    """

    def __init__(self, sound_manager):
        self.sound_manager = sound_manager
        self.ending_type = None
        self.days_completed = 0

        # Fuentes
        self.font_title = pygame.font.SysFont("Arial", 34, bold=True)
        self.font_text = pygame.font.SysFont("Arial", 20)
        self.font_small = pygame.font.SysFont("Arial", 16)
        self.font_button = pygame.font.SysFont("Arial", 20, bold=True)

        self.time = 0

    def init(self, ending_type, days_completed=0):
        """Inicializa la pantalla de final."""
        self.ending_type = ending_type
        self.days_completed = days_completed
        self.time = 0

        if ending_type in (ENDING_PERFECT, ENDING_PARTIAL):
            self.sound_manager.play("victoria")
        else:
            self.sound_manager.play("error")

    def update(self, events, dt):
        """
        Procesa eventos. Retorna "menu" para volver al menú, o None.
        """
        self.time += dt

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100,
                                        SCREEN_HEIGHT - 100, 200, 45)
                if btn_rect.collidepoint(mouse):
                    self.sound_manager.play("select")
                    return "menu"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.sound_manager.play("select")
                    return "menu"

        return None

    def draw(self, surface):
        """Dibuja la pantalla de final."""
        # Colores según tipo de final
        if self.ending_type == ENDING_PERFECT:
            bg_top = (20, 60, 20)
            bg_bot = (10, 40, 30)
            accent = (100, 255, 100)
            emoji = "🏆"
        elif self.ending_type == ENDING_PARTIAL:
            bg_top = (20, 40, 60)
            bg_bot = (15, 30, 50)
            accent = (100, 200, 255)
            emoji = "🎉"
        elif self.ending_type == ENDING_FAILURE:
            bg_top = (60, 20, 20)
            bg_bot = (40, 10, 15)
            accent = (255, 100, 100)
            emoji = "💀"
        else:  # TIMEOUT
            bg_top = (50, 30, 10)
            bg_bot = (35, 20, 10)
            accent = (255, 150, 50)
            emoji = "⏱"

        # Fondo degradado
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(bg_top[0] * (1 - t) + bg_bot[0] * t)
            g = int(bg_top[1] * (1 - t) + bg_bot[1] * t)
            b = int(bg_top[2] * (1 - t) + bg_bot[2] * t)
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Emoji grande
        emoji_font = pygame.font.SysFont("Segoe UI Emoji", 60)
        emoji_text = emoji_font.render(emoji, True, WHITE)
        surface.blit(emoji_text,
                     emoji_text.get_rect(center=(SCREEN_WIDTH // 2, 100)))

        # Texto principal según final
        if self.ending_type == ENDING_PERFECT:
            line1 = "¡Felicidades, lo has conseguido!"
            line2 = "Eres todo un genio"
            line3 = f"Días resueltos: 4/4"
        elif self.ending_type == ENDING_PARTIAL:
            line1 = "¡Enhorabuena!"
            line2 = "Has conseguido que te rescaten"
            line3 = f"Días resueltos: {self.days_completed}/4"
        elif self.ending_type == ENDING_FAILURE:
            line1 = "Estás perdido..."
            line2 = "No has podido ser rescatado"
            line3 = f"Días completados: {self.days_completed}/4"
        else:
            line1 = "¡Tiempo agotado!"
            line2 = "No has podido entrar al búnker"
            line3 = ""

        # Renderizar textos
        y = 190
        t1 = self.font_title.render(line1, True, accent)
        surface.blit(t1, t1.get_rect(center=(SCREEN_WIDTH // 2, y)))
        y += 50

        t2 = self.font_text.render(line2, True, WHITE)
        surface.blit(t2, t2.get_rect(center=(SCREEN_WIDTH // 2, y)))
        y += 40

        if line3:
            t3 = self.font_text.render(line3, True, LIGHT_GRAY)
            surface.blit(t3, t3.get_rect(center=(SCREEN_WIDTH // 2, y)))
            y += 40

        # Recomendación para fracaso
        if self.ending_type == ENDING_FAILURE:
            rec = self.font_small.render(
                "💡 Recomendación: agarra todos los libros que puedas,",
                True, (200, 200, 150))
            rec2 = self.font_small.render(
                "sirven como apoyo visual para resolver los problemas.",
                True, (200, 200, 150))
            surface.blit(rec, rec.get_rect(center=(SCREEN_WIDTH // 2, y + 20)))
            surface.blit(rec2, rec2.get_rect(center=(SCREEN_WIDTH // 2, y + 44)))

        # Botón volver al menú
        btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100,
                                SCREEN_HEIGHT - 100, 200, 45)
        mouse = pygame.mouse.get_pos()
        hover = btn_rect.collidepoint(mouse)

        # Animación de pulso
        pulse = 1 + math.sin(self.time * 3) * 0.03
        if hover:
            btn_color = (min(255, accent[0] + 30),
                         min(255, accent[1] + 30),
                         min(255, accent[2] + 30))
        else:
            btn_color = accent

        pygame.draw.rect(surface, btn_color, btn_rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, btn_rect, 2, border_radius=10)
        b_text = self.font_button.render("Volver al menú", True, WHITE)
        surface.blit(b_text, b_text.get_rect(center=btn_rect.center))
