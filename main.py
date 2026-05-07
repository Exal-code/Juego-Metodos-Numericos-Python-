# ============================================
# main.py - Punto de entrada del juego
# "30 Segundos Antes de la Tragedia"
# ============================================
#
# CÓMO EJECUTAR ESTE JUEGO
# ============================================
# 1. Abrir terminal (CMD, PowerShell, bash)
# 2. Instalar pygame-ce:
#    pip install pygame-ce
# 3. Ejecutar:
#    python main.py
#
# NOTA: No requiere servidor web. Es un juego de escritorio.
# No requiere archivos de sonido .wav externos.
# ============================================

import pygame
import sys
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK,
    STATE_MENU, STATE_HOUSE, STATE_BUNKER, STATE_ENDING,
    ENDING_PERFECT, ENDING_PARTIAL, ENDING_FAILURE, ENDING_TIMEOUT,
)
from sounds import SoundManager
from menu import MainMenu, EndScreen
from house import HousePhase
from bunker import BunkerPhase


class Game:
    """
    Clase principal del juego.
    Gestiona el ciclo de juego y las transiciones entre pantallas.
    """

    def __init__(self):
        # --- Inicializar Pygame ---
        pygame.init()
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        except Exception:
            pass  # El juego funciona sin audio

        # --- Pantalla ---
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("30 Segundos Antes de la Tragedia")
        self.clock = pygame.time.Clock()

        # --- Sistemas ---
        self.sound_manager = SoundManager()

        # --- Pantallas / Fases ---
        self.menu = MainMenu(self.sound_manager)
        self.house_phase = HousePhase(self.sound_manager)
        self.bunker_phase = BunkerPhase(self.sound_manager)
        self.end_screen = EndScreen(self.sound_manager)

        # --- Estado actual ---
        self.state = STATE_MENU
        self.running = True

    def run(self):
        """Bucle principal del juego."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time en segundos

            # --- Recoger Eventos ---
            events = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                events.append(event)

            if not self.running:
                break

            # --- Actualizar según estado ---
            if self.state == STATE_MENU:
                result = self.menu.update(events, dt)
                if result == "new_game":
                    self._start_new_game()
                elif result == "quit":
                    self.running = False

            elif self.state == STATE_HOUSE:
                result = self.house_phase.update(events, dt)
                if result:
                    next_state, data = result
                    if next_state == STATE_BUNKER:
                        self._enter_bunker(data)
                    elif next_state == STATE_ENDING:
                        self._show_ending(data, 0)

            elif self.state == STATE_BUNKER:
                result = self.bunker_phase.update(events, dt)
                if result:
                    days = self.bunker_phase.days_completed
                    self._show_ending(result, days)

            elif self.state == STATE_ENDING:
                result = self.end_screen.update(events, dt)
                if result == "menu":
                    self._return_to_menu()

            # --- Dibujar ---
            self.screen.fill(BLACK)

            if self.state == STATE_MENU:
                self.menu.draw(self.screen)
            elif self.state == STATE_HOUSE:
                self.house_phase.draw(self.screen)
            elif self.state == STATE_BUNKER:
                self.bunker_phase.draw(self.screen)
            elif self.state == STATE_ENDING:
                self.end_screen.draw(self.screen)

            pygame.display.flip()

        # --- Cleanup ---
        pygame.quit()
        sys.exit()

    def _start_new_game(self):
        """Inicia un juego nuevo (fase de la casa)."""
        self.house_phase.reset()
        self.state = STATE_HOUSE

    def _enter_bunker(self, books_collected):
        """Transiciona a la fase del búnker."""
        self.bunker_phase.init_with_books(books_collected)
        self.state = STATE_BUNKER

    def _show_ending(self, ending_type, days_completed):
        """Muestra la pantalla de final."""
        self.end_screen.init(ending_type, days_completed)
        self.state = STATE_ENDING

    def _return_to_menu(self):
        """Regresa al menú principal."""
        self.menu.selected = 0
        self.state = STATE_MENU


# ============================================
#  PUNTO DE ENTRADA
# ============================================
if __name__ == "__main__":
    game = Game()
    game.run()
