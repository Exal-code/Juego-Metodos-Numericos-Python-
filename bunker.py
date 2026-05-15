# ============================================
# bunker.py - Fase del búnker (5 días de supervivencia)
# ============================================

import pygame
import math
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BUNKER_WALL, BUNKER_FLOOR, BUNKER_CEILING,
    METAL_DOOR, METAL_DOOR_DARK, SHELF_COLOR, SHELF_DARK,
    BOOK_COLORS, WHITE, BLACK, DARK_GRAY, LIGHT_GRAY,
    MODAL_BG, MODAL_BORDER, MODAL_HEADER,
    BUTTON_GREEN, BUTTON_GREEN_HOVER,
    BUTTON_RED, BUTTON_RED_HOVER,
    BUTTON_BLUE, BUTTON_BLUE_HOVER,
    BUTTON_GRAY, BUTTON_GRAY_HOVER,
    INPUT_BG, INPUT_BORDER, INPUT_ACTIVE, INPUT_TEXT,
    DAY_BASE_TIMES, DAY_BONUSES, DAY_PENALTY,
    ENDING_PERFECT, ENDING_PARTIAL, ENDING_FAILURE,
    PLAYER_SKIN, PLAYER_SHIRT, PLAYER_PANTS, PLAYER_CAP,
    PLAYER_HAIR, PLAYER_BACKPACK,
)
from entities import TextInput
from problems import get_bunker_problems, check_field_answer, check_all_fields, BOOK_EXAMPLES


# ============================================
#  MODAL DE PROBLEMA
# ============================================
class ProblemModal:
    """
    Ventana emergente para resolver un problema matemático.
    Incluye: enunciado, campo de texto, timer, botones, pistas de libros.
    """

    def __init__(self, problem, time_seconds, books_collected, sound_manager):
        self.problem = problem
        self.time_remaining = time_seconds
        self.time_total = time_seconds
        self.books = books_collected
        self.sound_manager = sound_manager

        # Estado
        self.paused = False
        self.finished = False
        self.result = None
        self.show_hint = None

        # Selección de ejemplos de libros para esta sesión
        # Si el jugador tiene 1 libro de un color, elige aleatoriamente
        # cuál de los 2 ejemplos mostrar (se fija al crear el modal).
        import random as _rnd
        self.book_example_selection = {}
        for color in ["green", "red", "blue", "purple"]:
            count = books_collected.get(color, 0)
            if count == 1:
                self.book_example_selection[color] = _rnd.randint(0, 1)
            # Si count == 2, se muestran ambos; si count == 0, no se muestra nada

        # Múltiples campos de respuesta
        self.fields = problem.get("fields", [])
        self.text_inputs = []
        self.active_field = 0
        for i, field in enumerate(self.fields):
            ti = TextInput(0, 0, 200, 30, font_size=18)
            ti.active = (i == 0)
            self.text_inputs.append(ti)
        # Fallback si no hay fields
        if not self.text_inputs:
            self.text_inputs = [TextInput(0, 0, 280, 40)]

        # Fuentes
        self.font_title = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_text = pygame.font.SysFont("Arial", 15)
        self.font_label = pygame.font.SysFont("Arial", 14, bold=True)
        self.font_timer = pygame.font.SysFont("Consolas", 28, bold=True)
        self.font_button = pygame.font.SysFont("Arial", 16, bold=True)
        self.font_hint = pygame.font.SysFont("Arial", 15)
        self.font_small = pygame.font.SysFont("Arial", 13)

        # Geometría del modal
        self.modal_rect = pygame.Rect(40, 30, SCREEN_WIDTH - 80, SCREEN_HEIGHT - 60)

        # Mensaje de resultado
        self.result_message = ""
        self.result_timer = 0
        self.show_result = False

    def update(self, events, dt):
        if self.show_result:
            self.result_timer -= dt
            if self.result_timer <= 0:
                return self.result
            return None

        if not self.paused:
            self.time_remaining -= dt
            if self.time_remaining <= 0:
                self.time_remaining = 0
                self._set_result("timeout", "⏱ ¡Se acabó el tiempo!")
                return None

        # Actualizar campo activo
        if self.active_field < len(self.text_inputs):
            self.text_inputs[self.active_field].update(dt)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                self._handle_click(mouse)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    # Cambiar al siguiente campo
                    self._switch_field((self.active_field + 1) % len(self.text_inputs))
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self._submit_answer()
                else:
                    if self.active_field < len(self.text_inputs):
                        self.text_inputs[self.active_field].handle_event(event)

        return None

    def _switch_field(self, idx):
        """Cambia el campo activo."""
        for i, ti in enumerate(self.text_inputs):
            ti.active = (i == idx)
        self.active_field = idx

    def _handle_click(self, mouse):
        """Procesa clics del mouse en el modal."""
        # Botón Entregar
        btn_submit = pygame.Rect(self.modal_rect.centerx - 70,
                                  self.modal_rect.bottom - 55, 140, 38)
        if btn_submit.collidepoint(mouse):
            self.sound_manager.play("select")
            self._submit_answer()
            return

        # Botón Pausa
        btn_pause = pygame.Rect(self.modal_rect.right - 100,
                                 self.modal_rect.top + 45, 80, 30)
        if btn_pause.collidepoint(mouse):
            self.sound_manager.play("select")
            self.paused = not self.paused
            return

        # Clic en campos de texto
        for i, ti in enumerate(self.text_inputs):
            if ti.rect.collidepoint(mouse):
                self._switch_field(i)
                return

        # Clic en libros (ejemplos fijos)
        book_y = self.modal_rect.top + 90
        color_order = ["green", "red", "blue", "purple"]
        for i, color in enumerate(color_order):
            if self.books.get(color, 0) > 0:
                book_rect = pygame.Rect(self.modal_rect.left + 15,
                                         book_y + i * 55, 95, 45)
                if book_rect.collidepoint(mouse):
                    self.sound_manager.play("select")
                    self.show_hint = color if self.show_hint != color else None
                    return

    def _submit_answer(self):
        """Envía las respuestas del jugador (todos los campos)."""
        if self.show_result:
            return

        user_answers = [ti.get_value() for ti in self.text_inputs]

        # Verificar si todos están vacíos
        if all(a == "" for a in user_answers):
            self._set_result("wrong", "❌ No ingresaste una respuesta")
            return

        if check_all_fields(self.problem, user_answers):
            self._set_result("correct", "✅ ¡Respuesta correcta!")
        else:
            self._set_result("wrong", "❌ Incorrecto")

    def _set_result(self, result, message):
        """Establece el resultado y muestra el mensaje."""
        self.result = result
        self.result_message = message
        self.show_result = True
        self.result_timer = 2.5  # Mostrar mensaje por 2.5 segundos

        if result == "correct":
            self.sound_manager.play("victoria")
        else:
            self.sound_manager.play("error")

    def _wrap_text(self, text, font, max_width):
        """Divide el texto en líneas que quepan en max_width píxeles."""
        words = text.split()
        lines = []
        current = ""
        for word in words:
            test = current + " " + word if current else word
            if font.size(test)[0] < max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def draw(self, surface):
        """Dibuja el modal de problema completo."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        mr = self.modal_rect
        mouse = pygame.mouse.get_pos()

        # Fondo del modal
        pygame.draw.rect(surface, MODAL_BG, mr, border_radius=10)
        pygame.draw.rect(surface, MODAL_BORDER, mr, 2, border_radius=10)

        # Header con nombre del método
        header = pygame.Rect(mr.left, mr.top, mr.width, 40)
        pygame.draw.rect(surface, MODAL_HEADER, header,
                         border_top_left_radius=10, border_top_right_radius=10)
        topic = self.problem.get("topic", "Problema")
        title = self.font_title.render(f"📝 Método: {topic}", True, WHITE)
        surface.blit(title, (mr.left + 15, mr.top + 10))

        # Timer
        mins = int(self.time_remaining // 60)
        secs = int(self.time_remaining % 60)
        timer_color = (255, 80, 80) if self.time_remaining < 60 else WHITE
        timer_text = self.font_timer.render(f"{mins:02d}:{secs:02d}", True, timer_color)
        surface.blit(timer_text, (mr.right - 120, mr.top + 5))

        # Botón Pausa
        btn_pause = pygame.Rect(mr.right - 100, mr.top + 45, 80, 30)
        pause_hover = btn_pause.collidepoint(mouse)
        p_color = BUTTON_GRAY_HOVER if pause_hover else BUTTON_GRAY
        pygame.draw.rect(surface, p_color, btn_pause, border_radius=5)
        pause_label = "▶ Reanudar" if self.paused else "⏸ Pausa"
        p_text = self.font_small.render(pause_label, True, WHITE)
        surface.blit(p_text, p_text.get_rect(center=btn_pause.center))

        # --- Libros con pistas (lado izquierdo) ---
        books_x = mr.left + 10
        books_y = mr.top + 85
        books_title = self.font_small.render("📚 Libros:", True, LIGHT_GRAY)
        surface.blit(books_title, (books_x, books_y - 15))

        color_order = ["green", "red", "blue", "purple"]
        color_names = {"green": "Verde", "red": "Rojo", "blue": "Azul", "purple": "Morado"}
        book_idx = 0

        for color in color_order:
            count = self.books.get(color, 0)
            if count > 0:
                by = books_y + book_idx * 55
                book_rect = pygame.Rect(books_x + 5, by, 95, 45)
                is_selected = self.show_hint == color
                bg_color = (70, 70, 85) if is_selected else (50, 50, 65)
                pygame.draw.rect(surface, bg_color, book_rect, border_radius=5)
                pygame.draw.rect(surface, BOOK_COLORS[color], book_rect, 2, border_radius=5)
                icon = pygame.Rect(books_x + 10, by + 8, 18, 25)
                pygame.draw.rect(surface, BOOK_COLORS[color], icon, border_radius=2)
                name = self.font_small.render(f"{color_names[color]} x{count}", True, WHITE)
                surface.blit(name, (books_x + 33, by + 14))
                book_idx += 1

        # Mostrar ejemplos de libro (fórmulas y recomendaciones fijas)
        if self.show_hint and self.show_hint in BOOK_EXAMPLES:
            color = self.show_hint
            count = self.books.get(color, 0)
            examples = BOOK_EXAMPLES[color]

            # Determinar qué ejemplos mostrar
            if count >= 2:
                examples_to_show = examples  # ambos
            elif count == 1:
                idx = self.book_example_selection.get(color, 0)
                examples_to_show = [examples[idx]]
            else:
                examples_to_show = []

            hint_y = books_y + book_idx * 55 + 10
            for ex in examples_to_show:
                # Panel de fondo para cada ejemplo
                panel_h = 80
                panel_rect = pygame.Rect(books_x, hint_y, 120, panel_h)
                pygame.draw.rect(surface, (55, 55, 70), panel_rect, border_radius=5)
                pygame.draw.rect(surface, BOOK_COLORS[color], panel_rect, 1, border_radius=5)

                # Título del método
                title_text = self.font_small.render(ex["titulo"], True, (255, 215, 0))
                surface.blit(title_text, (books_x + 5, hint_y + 3))

                # Fórmula (con word-wrap)
                formula_lines = self._wrap_text(ex["formula"], self.font_small, 110)
                fy = hint_y + 17
                for line in formula_lines[:2]:
                    lt = self.font_small.render(line, True, (180, 255, 180))
                    surface.blit(lt, (books_x + 5, fy))
                    fy += 13

                # Recomendación (con word-wrap)
                rec_lines = self._wrap_text(ex["recomendacion"], self.font_small, 110)
                for line in rec_lines[:3]:
                    lt = self.font_small.render(line, True, (200, 200, 220))
                    surface.blit(lt, (books_x + 5, fy))
                    fy += 13

                hint_y += panel_h + 5

        # --- Contenido principal (centro-derecha) ---
        content_x = mr.left + 130
        content_w = mr.width - 150

        # Enunciado del problema (soporta \n)
        problem_y = mr.top + 55
        problem_text = self.problem["text"]
        raw_lines = problem_text.split("\n")
        all_lines = []
        for raw_line in raw_lines:
            if raw_line.strip() == "":
                all_lines.append("")
                continue
            words = raw_line.split()
            current_l = ""
            for word in words:
                test = current_l + " " + word if current_l else word
                if self.font_text.size(test)[0] < content_w - 20:
                    current_l = test
                else:
                    if current_l:
                        all_lines.append(current_l)
                    current_l = word
            if current_l:
                all_lines.append(current_l)

        for i, line in enumerate(all_lines):
            if line == "":
                continue
            lt = self.font_text.render(line, True, WHITE)
            surface.blit(lt, (content_x + 10, problem_y + i * 20))

        # --- Campos de respuesta ---
        num_fields = len(self.fields)
        fields_start_y = problem_y + len(all_lines) * 20 + 15

        if num_fields <= 2:
            # Layout simple: campos en columna
            for i, field in enumerate(self.fields):
                fy = fields_start_y + i * 45
                lbl = self.font_label.render(field["label"], True, (255, 215, 0))
                surface.blit(lbl, (content_x + 10, fy))
                lbl_w = lbl.get_width() + 5
                self.text_inputs[i].rect.x = content_x + 10 + lbl_w
                self.text_inputs[i].rect.y = fy - 3
                self.text_inputs[i].rect.width = min(200, content_w - lbl_w - 30)
                self.text_inputs[i].rect.height = 28
                self.text_inputs[i].draw(surface)
        elif num_fields == 7:
            # Layout para 7 campos: primeros 4 arriba, 3 errores abajo
            col_w = (content_w - 20) // 2
            for i in range(4):
                row = i // 2
                col = i % 2
                fx = content_x + 10 + col * col_w
                fy = fields_start_y + row * 45
                lbl = self.font_label.render(self.fields[i]["label"], True, (255, 215, 0))
                surface.blit(lbl, (fx, fy))
                lbl_w = lbl.get_width() + 3
                inp_w = max(60, col_w - lbl_w - 10)
                self.text_inputs[i].rect.x = fx + lbl_w
                self.text_inputs[i].rect.y = fy - 3
                self.text_inputs[i].rect.width = inp_w
                self.text_inputs[i].rect.height = 28
                self.text_inputs[i].draw(surface)

            # Separador
            sep_y = fields_start_y + 95
            pygame.draw.line(surface, LIGHT_GRAY,
                             (content_x + 10, sep_y), (content_x + content_w - 20, sep_y), 1)
            err_label = self.font_small.render("Márgenes de Error:", True, LIGHT_GRAY)
            surface.blit(err_label, (content_x + 10, sep_y + 3))

            # 3 campos de error debajo
            err_col_w = (content_w - 20) // 2
            for j in range(3):
                idx = 4 + j
                row = j // 2
                col = j % 2
                fx = content_x + 10 + col * err_col_w
                fy = sep_y + 22 + row * 45
                lbl = self.font_label.render(self.fields[idx]["label"], True, (255, 200, 100))
                surface.blit(lbl, (fx, fy))
                lbl_w = lbl.get_width() + 3
                inp_w = max(60, err_col_w - lbl_w - 10)
                self.text_inputs[idx].rect.x = fx + lbl_w
                self.text_inputs[idx].rect.y = fy - 3
                self.text_inputs[idx].rect.width = inp_w
                self.text_inputs[idx].rect.height = 28
                self.text_inputs[idx].draw(surface)
        else:
            # Layout genérico
            for i, field in enumerate(self.fields):
                fy = fields_start_y + i * 38
                lbl = self.font_label.render(field["label"], True, (255, 215, 0))
                surface.blit(lbl, (content_x + 10, fy))
                lbl_w = lbl.get_width() + 5
                self.text_inputs[i].rect.x = content_x + 10 + lbl_w
                self.text_inputs[i].rect.y = fy - 3
                self.text_inputs[i].rect.width = min(180, content_w - lbl_w - 30)
                self.text_inputs[i].rect.height = 28
                self.text_inputs[i].draw(surface)

        # Botón Entregar
        btn_submit = pygame.Rect(mr.centerx - 70, mr.bottom - 55, 140, 38)
        s_hover = btn_submit.collidepoint(mouse)
        s_color = BUTTON_GREEN_HOVER if s_hover else BUTTON_GREEN
        pygame.draw.rect(surface, s_color, btn_submit, border_radius=8)
        pygame.draw.rect(surface, WHITE, btn_submit, 2, border_radius=8)
        s_text = self.font_button.render("📩 Entregar", True, WHITE)
        surface.blit(s_text, s_text.get_rect(center=btn_submit.center))

        # Indicador de pausa
        if self.paused:
            pause_overlay = pygame.Surface((mr.width - 4, 40), pygame.SRCALPHA)
            pause_overlay.fill((0, 0, 0, 180))
            surface.blit(pause_overlay, (mr.left + 2, mr.centery - 20))
            pt = self.font_title.render("⏸ JUEGO EN PAUSA", True, (255, 215, 0))
            surface.blit(pt, pt.get_rect(center=(mr.centerx, mr.centery)))

        # Mostrar resultado
        if self.show_result:
            result_overlay = pygame.Surface((mr.width - 4, 60), pygame.SRCALPHA)
            r_bg = (20, 80, 20, 220) if self.result == "correct" else (80, 20, 20, 220)
            result_overlay.fill(r_bg)
            surface.blit(result_overlay, (mr.left + 2, mr.centery + 40))

            r_color = (100, 255, 100) if self.result == "correct" else (255, 100, 100)
            rt = self.font_title.render(self.result_message, True, r_color)
            surface.blit(rt, rt.get_rect(center=(mr.centerx, mr.centery + 70)))


# ============================================
#  FASE DEL BÚNKER (PANTALLA 3)
# ============================================
class BunkerPhase:
    """
    Fase del búnker: 5 días de supervivencia.
    Días 1-4: resolver un problema cada día.
    Día 5: final del juego.
    """

    def __init__(self, sound_manager):
        self.sound_manager = sound_manager
        self.reset({})

    def reset(self, books_collected):
        """Reinicia la fase del búnker con los libros recolectados."""
        self.books = books_collected  # dict {color: count}

        # Estado del juego
        self.current_day = 1
        self.errors = 0
        self.has_error = False  # True una vez que comete un error
        self.penalty_next_day = False  # -3 min en el siguiente día
        self.no_bonus_forever = False  # Una vez que hay error, sin bonus
        self.days_completed = 0

        # Problemas aleatorios (4 para los 4 días)
        self.problems = get_bunker_problems()

        # Suministros (10 de cada uno, -2 por día)
        self.water = 10
        self.food = 10

        # UI estado
        self.show_arrow = True
        self.arrow_timer = 0
        self.modal = None  # ProblemModal actual
        self.transitioning = False
        self.transition_timer = 0
        self.day_start_shown = False

        # Mensaje temporal
        self.message = ""
        self.message_timer = 0

        # === Fracaso pendiente (mostrar mensaje antes de salir) ===
        self.failure_pending = False
        self.failure_timer = 0

        # Resultado final
        self.finished = False
        self.ending_type = None

        # Fuentes
        self.font_title = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_subtitle = pygame.font.SysFont("Arial", 20)
        self.font_text = pygame.font.SysFont("Arial", 16)
        self.font_small = pygame.font.SysFont("Arial", 13)
        self.font_day = pygame.font.SysFont("Arial", 36, bold=True)
        self.font_message = pygame.font.SysFont("Arial", 22, bold=True)

        # Reproducir sonido de hoja
        self.sound_manager.play("hoja")

    def init_with_books(self, books_collected):
        """Inicializa con los libros recogidos en la fase de casa."""
        self.reset(books_collected)

    def _get_day_time(self, day_index):
        """
        Calcula el tiempo para un día específico.
        day_index: 0-3 (días 1-4)
        """
        base = DAY_BASE_TIMES[day_index]

        # Agregar bonificación si no ha tenido errores
        if not self.no_bonus_forever:
            base += DAY_BONUSES[day_index]

        # Aplicar penalización si viene de un error
        if self.penalty_next_day:
            base -= DAY_PENALTY
            self.penalty_next_day = False

        return max(60, base)  # Mínimo 1 minuto

    def update(self, events, dt):
        """
        Actualiza la lógica del búnker.
        Retorna el tipo de ending cuando termina, o None.
        """
        # === Fracaso pendiente: mostrar mensaje antes de salir ===
        if self.failure_pending:
            self.failure_timer -= dt
            self.message_timer -= dt
            if self.failure_timer <= 0:
                return ENDING_FAILURE
            return None

        # Si está en transición entre días
        if self.transitioning:
            self.transition_timer -= dt
            # Seguir mostrando mensajes durante la transición
            if self.message_timer > 0:
                self.message_timer -= dt
            if self.transition_timer <= 0:
                self.transitioning = False
                self.day_start_shown = False
                self.arrow_timer = 0
                # Actualizar suministros
                self.water = max(0, self.water - 2)
                self.food = max(0, self.food - 2)
                self.sound_manager.play("hoja")
            return None

        # Mensaje temporal
        if self.message_timer > 0:
            self.message_timer -= dt

        # Si hay un modal de problema abierto
        if self.modal:
            result = self.modal.update(events, dt)
            if result:
                return self._handle_problem_result(result)
            return None

        # Día 5: mostrar final directamente
        if self.current_day == 5:
            if self.errors == 0:
                return ENDING_PERFECT
            else:
                return ENDING_PARTIAL

        # Actualizar flecha parpadeante
        self.arrow_timer += dt

        # Procesar clics
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # Verificar clic en la puerta
                door_rect = self._get_door_rect()
                if door_rect.collidepoint(mouse) and self.modal is None:
                    self._open_problem()

        return None

    def _get_door_rect(self):
        """Retorna el rectángulo de la puerta del búnker."""
        return pygame.Rect(SCREEN_WIDTH - 120, 150, 80, 200)

    def _open_problem(self):
        """Abre el modal de problema para el día actual."""
        day_index = self.current_day - 1
        if day_index >= len(self.problems):
            return

        problem = self.problems[day_index]
        time_sec = self._get_day_time(day_index)

        self.modal = ProblemModal(
            problem, time_sec, self.books, self.sound_manager
        )

    def _handle_problem_result(self, result):
        """
        Procesa el resultado de un problema.
        result: "correct", "wrong", o "timeout"
        """
        self.modal = None

        if result == "correct":
            self.days_completed += 1
            self.message = "✅ ¡Correcto! Pasas al siguiente día."
            self.message_timer = 3.0

            # Avanzar al siguiente día
            self.current_day += 1
            self.transitioning = True
            self.transition_timer = 2.0

        else:  # "wrong" o "timeout"
            self.errors += 1

            if self.errors >= 2:
                # Segundo error → mostrar mensaje de fracaso antes de salir
                self.message = "💀 ¡Has fallado dos veces! No podrás ser rescatado..."
                self.message_timer = 4.0
                self.failure_pending = True
                self.failure_timer = 4.0
                self.sound_manager.play("error")
                return None  # No retornar ending inmediatamente

            # Primer error
            self.has_error = True
            self.no_bonus_forever = True
            self.penalty_next_day = True

            self.message = "⚠ ¡Error! Solo te queda una oportunidad más."
            self.message_timer = 4.0

            # Avanzar al siguiente día (sin completar este)
            self.current_day += 1
            self.transitioning = True
            self.transition_timer = 3.0

        # Verificar si llegamos al día 5
        if self.current_day == 5:
            self.transitioning = True
            self.transition_timer = 2.0

        return None

    def draw(self, surface):
        """Dibuja la pantalla completa del búnker."""
        # Fondo del búnker
        self._draw_bunker_bg(surface)

        # Personaje sentado
        self._draw_character(surface)

        # Estantería con libros (izquierda)
        self._draw_bookshelf(surface)

        # Puerta de metal (derecha)
        self._draw_door(surface)

        # Suministros en el piso
        self._draw_supplies(surface)

        # HUD: día actual
        self._draw_day_hud(surface)

        # Flecha parpadeante sobre la puerta
        if self.modal is None and self.current_day <= 4 and not self.transitioning:
            self._draw_arrow(surface)

        # Transición entre días
        if self.transitioning:
            self._draw_transition(surface)

        # Mensaje temporal (dibujado ENCIMA de la transición para que sea visible)
        if self.message_timer > 0 and self.message:
            self._draw_message(surface)

        # Fracaso pendiente: overlay oscuro + mensaje
        if self.failure_pending:
            fail_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fail_overlay.fill((0, 0, 0, 180))
            surface.blit(fail_overlay, (0, 0))
            self._draw_message(surface)

        # Modal de problema (encima de todo)
        if self.modal:
            self.modal.draw(surface)

    def _draw_bunker_bg(self, surface):
        """Dibuja el fondo del interior del búnker."""
        # Suelo
        surface.fill(BUNKER_FLOOR)

        # Paredes laterales
        pygame.draw.rect(surface, BUNKER_WALL, (0, 0, SCREEN_WIDTH, 120))
        # Techo/cielo (efecto de techo metálico)
        pygame.draw.rect(surface, BUNKER_CEILING, (0, 0, SCREEN_WIDTH, 40))

        # Líneas de paneles metálicos (paredes)
        for i in range(0, SCREEN_WIDTH, 80):
            pygame.draw.line(surface, (95, 95, 105), (i, 40), (i, 120), 1)

        # Líneas del suelo
        for i in range(120, SCREEN_HEIGHT, 60):
            pygame.draw.line(surface, (60, 60, 70), (0, i), (SCREEN_WIDTH, i), 1)

        # Remaches
        for x in range(20, SCREEN_WIDTH, 80):
            for y in [45, 110]:
                pygame.draw.circle(surface, (110, 110, 120), (x, y), 3)
                pygame.draw.circle(surface, (80, 80, 90), (x, y), 3, 1)

    def _draw_character(self, surface):
        """Dibuja al personaje sentado en una silla (centro)."""
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2 + 30

        # Silla
        pygame.draw.rect(surface, (100, 60, 30), (cx - 18, cy - 10, 36, 40), border_radius=3)
        pygame.draw.rect(surface, (80, 45, 20), (cx - 18, cy - 30, 36, 25), border_radius=3)
        # Patas
        pygame.draw.rect(surface, (70, 40, 15), (cx - 16, cy + 25, 6, 15))
        pygame.draw.rect(surface, (70, 40, 15), (cx + 10, cy + 25, 6, 15))

        # Piernas (sentado)
        pygame.draw.rect(surface, PLAYER_PANTS, (cx - 10, cy + 5, 8, 20))
        pygame.draw.rect(surface, PLAYER_PANTS, (cx + 2, cy + 5, 8, 20))

        # Torso
        pygame.draw.rect(surface, PLAYER_SHIRT, (cx - 12, cy - 15, 24, 22))

        # Mochila (detrás)
        pygame.draw.rect(surface, PLAYER_BACKPACK, (cx - 14, cy - 12, 5, 16))

        # Brazos
        pygame.draw.rect(surface, PLAYER_SKIN, (cx - 15, cy - 10, 4, 14))
        pygame.draw.rect(surface, PLAYER_SKIN, (cx + 11, cy - 10, 4, 14))

        # Cabeza
        pygame.draw.circle(surface, PLAYER_SKIN, (cx, cy - 25), 12)

        # Ojos
        pygame.draw.circle(surface, (30, 30, 30), (cx - 4, cy - 26), 2)
        pygame.draw.circle(surface, (30, 30, 30), (cx + 4, cy - 26), 2)

        # Boca (sonrisa ligera)
        pygame.draw.arc(surface, (30, 30, 30),
                        (cx - 5, cy - 25, 10, 8), 3.4, 6.0, 1)

        # Gorra
        pygame.draw.rect(surface, PLAYER_CAP, (cx - 12, cy - 38, 24, 8), border_radius=2)
        pygame.draw.rect(surface, PLAYER_CAP, (cx - 14, cy - 31, 28, 4))

    def _draw_bookshelf(self, surface):
        """Dibuja la estantería con los libros recogidos (izquierda)."""
        shelf_x = 30
        shelf_y = 150

        # Marco de la estantería
        shelf_rect = pygame.Rect(shelf_x, shelf_y, 90, 250)
        pygame.draw.rect(surface, SHELF_COLOR, shelf_rect, border_radius=3)
        pygame.draw.rect(surface, SHELF_DARK, shelf_rect, 2, border_radius=3)

        # Repisas
        for i in range(4):
            ry = shelf_y + 10 + i * 60
            pygame.draw.line(surface, SHELF_DARK,
                             (shelf_x + 5, ry + 50), (shelf_x + 85, ry + 50), 3)

        # Libros en las repisas
        color_order = ["green", "red", "blue", "purple"]
        color_names = {"green": "Verde", "red": "Rojo", "blue": "Azul", "purple": "Morado"}
        shelf_slot = 0

        for color in color_order:
            count = self.books.get(color, 0)
            if count > 0:
                by = shelf_y + 15 + shelf_slot * 60
                # Dibujar libros apilados
                for j in range(min(count, 2)):
                    bx = shelf_x + 12 + j * 30
                    book_rect = pygame.Rect(bx, by, 22, 35)
                    pygame.draw.rect(surface, BOOK_COLORS[color], book_rect, border_radius=2)
                    c = BOOK_COLORS[color]
                    darker = (max(0, c[0]-40), max(0, c[1]-40), max(0, c[2]-40))
                    pygame.draw.rect(surface, darker, book_rect, 1, border_radius=2)
                    # Líneas de páginas
                    for k in range(3):
                        pygame.draw.line(surface, (220, 220, 220),
                                         (bx + 3, by + 8 + k * 8),
                                         (bx + 19, by + 8 + k * 8), 1)

                shelf_slot += 1

        # Etiqueta
        if sum(self.books.values()) == 0:
            label = self.font_small.render("(vacía)", True, LIGHT_GRAY)
            surface.blit(label, (shelf_x + 20, shelf_y + 120))

    def _draw_door(self, surface):
        """Dibuja la puerta de metal con agujero (derecha)."""
        door_rect = self._get_door_rect()

        # Puerta
        pygame.draw.rect(surface, METAL_DOOR, door_rect, border_radius=3)
        pygame.draw.rect(surface, METAL_DOOR_DARK, door_rect, 3, border_radius=3)

        # Efecto metálico (líneas verticales)
        for i in range(door_rect.left + 10, door_rect.right - 10, 15):
            pygame.draw.line(surface, (130, 130, 145),
                             (i, door_rect.top + 10), (i, door_rect.bottom - 10), 1)

        # Remaches en las esquinas
        for dx, dy in [(15, 15), (15, -15), (-15, 15), (-15, -15)]:
            rx = door_rect.centerx + dx
            ry = door_rect.centery + dy
            pygame.draw.circle(surface, (140, 140, 155), (rx, ry), 4)
            pygame.draw.circle(surface, (100, 100, 115), (rx, ry), 4, 1)

        # Agujero en la parte inferior (ranura para las hojas)
        slot_rect = pygame.Rect(door_rect.centerx - 25,
                                door_rect.bottom - 30, 50, 12)
        pygame.draw.rect(surface, (20, 20, 25), slot_rect, border_radius=2)
        pygame.draw.rect(surface, METAL_DOOR_DARK, slot_rect, 1, border_radius=2)

        # Texto "Puerta"
        label = self.font_small.render("Puerta", True, LIGHT_GRAY)
        surface.blit(label, label.get_rect(center=(door_rect.centerx,
                                                     door_rect.top - 10)))

    def _draw_supplies(self, surface):
        """Dibuja los suministros (agua y comida) en el piso."""
        sx = 160
        sy = SCREEN_HEIGHT - 100

        # Título
        title = self.font_small.render("Suministros:", True, LIGHT_GRAY)
        surface.blit(title, (sx, sy - 18))

        # Botellas de agua (rectángulos azules)
        for i in range(self.water):
            bx = sx + i * 18
            by = sy
            pygame.draw.rect(surface, (50, 130, 220), (bx, by, 12, 25), border_radius=3)
            pygame.draw.rect(surface, (40, 100, 180), (bx, by, 12, 25), 1, border_radius=3)
            # Tapa
            pygame.draw.rect(surface, (70, 150, 240), (bx + 3, by - 3, 6, 5), border_radius=1)

        # Latas de comida (rectángulos rojos)
        for i in range(self.food):
            bx = sx + i * 18
            by = sy + 35
            pygame.draw.rect(surface, (200, 60, 60), (bx, by, 14, 18), border_radius=2)
            pygame.draw.rect(surface, (160, 40, 40), (bx, by, 14, 18), 1, border_radius=2)
            # Etiqueta
            pygame.draw.rect(surface, (230, 230, 210), (bx + 2, by + 5, 10, 6))

        # Etiquetas
        water_label = self.font_small.render(f"💧 Agua: {self.water}", True, (100, 180, 255))
        food_label = self.font_small.render(f"🥫 Comida: {self.food}", True, (255, 120, 120))
        surface.blit(water_label, (sx + 200, sy + 5))
        surface.blit(food_label, (sx + 200, sy + 40))

    def _draw_day_hud(self, surface):
        """Dibuja el indicador del día actual."""
        # Fondo
        hud_rect = pygame.Rect(10, 10, 160, 50)
        s = pygame.Surface((160, 50), pygame.SRCALPHA)
        s.fill((20, 20, 30, 200))
        surface.blit(s, (10, 10))
        pygame.draw.rect(surface, (100, 100, 120), hud_rect, 2, border_radius=5)

        # Día
        day_text = self.font_subtitle.render(f"📅 Día {self.current_day}/5", True, WHITE)
        surface.blit(day_text, (20, 15))

        # Errores
        err_color = (255, 100, 100) if self.errors > 0 else (100, 255, 100)
        err_text = self.font_small.render(
            f"❌ Errores: {self.errors}/1", True, err_color)
        surface.blit(err_text, (20, 40))

        # Días completados
        comp_text = self.font_small.render(
            f"✅ Resueltos: {self.days_completed}/4", True, (100, 255, 150))
        comp_rect = comp_text.get_rect(topright=(SCREEN_WIDTH - 20, 15))
        surface.blit(comp_text, comp_rect)

    def _draw_arrow(self, surface):
        """Dibuja una flecha parpadeante sobre la puerta."""
        door_rect = self._get_door_rect()
        # Parpadeo
        if int(self.arrow_timer * 3) % 2 == 0:
            ax = door_rect.centerx
            ay = door_rect.top - 35

            # Flecha apuntando hacia abajo
            points = [
                (ax, ay + 20),       # punta
                (ax - 12, ay),       # izquierda
                (ax - 5, ay),
                (ax - 5, ay - 10),
                (ax + 5, ay - 10),
                (ax + 5, ay),
                (ax + 12, ay),       # derecha
            ]
            pygame.draw.polygon(surface, (255, 215, 0), points)
            pygame.draw.polygon(surface, (200, 170, 0), points, 2)

            # Texto "Clic"
            click_text = self.font_small.render("¡Clic aquí!", True, (255, 215, 0))
            surface.blit(click_text,
                         click_text.get_rect(center=(ax, ay - 20)))

    def _draw_message(self, surface):
        """Dibuja un mensaje temporal en la parte inferior."""
        # Fondo
        msg_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250,
                                SCREEN_HEIGHT // 2 - 25, 500, 50)
        s = pygame.Surface((500, 50), pygame.SRCALPHA)

        if "Error" in self.message or "⚠" in self.message:
            s.fill((80, 20, 20, 220))
        else:
            s.fill((20, 80, 20, 220))
        surface.blit(s, msg_rect.topleft)
        pygame.draw.rect(surface, WHITE, msg_rect, 2, border_radius=5)

        msg_text = self.font_message.render(self.message, True, WHITE)
        surface.blit(msg_text, msg_text.get_rect(center=msg_rect.center))

    def _draw_transition(self, surface):
        """Dibuja una transición entre días."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        alpha = max(0, min(255, int(200 * (1 - self.transition_timer / 3.0))))
        overlay.fill((0, 0, 0, alpha))
        surface.blit(overlay, (0, 0))

        if self.transition_timer < 1.5:
            if self.current_day <= 5:
                dt = self.font_day.render(f"Día {self.current_day}", True, WHITE)
                surface.blit(dt, dt.get_rect(center=(SCREEN_WIDTH // 2,
                                                       SCREEN_HEIGHT // 2)))
