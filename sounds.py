# ============================================
# sounds.py - Sistema de sonido del juego
# ============================================
# Genera tonos simples con pygame.mixer.
# Si el audio no está disponible, el juego funciona igual.

import math
import struct

try:
    import pygame
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False


def _generate_tone(frequency, duration, volume=0.3, sample_rate=22050):
    """Genera un tono sinusoidal simple como pygame.mixer.Sound."""
    n_samples = int(sample_rate * duration)
    buf = bytearray()
    for i in range(n_samples):
        t = i / sample_rate
        value = int(volume * 32767 * math.sin(2 * math.pi * frequency * t))
        # Clamp
        value = max(-32767, min(32767, value))
        buf += struct.pack('<h', value)
    return pygame.mixer.Sound(buffer=bytes(buf))


def _generate_rising_tone(freq_start, freq_end, duration, volume=0.3, sample_rate=22050):
    """Genera un tono que sube de frecuencia (para sonido de recoger)."""
    n_samples = int(sample_rate * duration)
    buf = bytearray()
    for i in range(n_samples):
        t = i / sample_rate
        freq = freq_start + (freq_end - freq_start) * (t / duration)
        value = int(volume * 32767 * math.sin(2 * math.pi * freq * t))
        value = max(-32767, min(32767, value))
        buf += struct.pack('<h', value)
    return pygame.mixer.Sound(buffer=bytes(buf))


def _generate_descending_tone(freq_start, freq_end, duration, volume=0.3, sample_rate=22050):
    """Genera un tono que baja de frecuencia (para sonido de error)."""
    return _generate_rising_tone(freq_start, freq_end, duration, volume, sample_rate)


def _generate_noise_burst(duration, volume=0.1, sample_rate=22050):
    """Genera un burst de ruido corto (para pasos)."""
    import random
    n_samples = int(sample_rate * duration)
    buf = bytearray()
    for i in range(n_samples):
        # Envelope para que suene como un paso (fade in/out rápido)
        t = i / n_samples
        envelope = min(t * 10, 1.0) * max(0, 1.0 - (t - 0.3) * 3)
        value = int(volume * 32767 * (random.random() * 2 - 1) * envelope)
        value = max(-32767, min(32767, value))
        buf += struct.pack('<h', value)
    return pygame.mixer.Sound(buffer=bytes(buf))


def _generate_victory_fanfare(volume=0.3, sample_rate=22050):
    """Genera una pequeña fanfarria de victoria."""
    notes = [(523, 0.15), (659, 0.15), (784, 0.15), (1047, 0.4)]
    buf = bytearray()
    for freq, dur in notes:
        n_samples = int(sample_rate * dur)
        for i in range(n_samples):
            t = i / sample_rate
            envelope = min(1.0, (n_samples - i) / (sample_rate * 0.05))
            value = int(volume * 32767 * math.sin(2 * math.pi * freq * t) * envelope)
            value = max(-32767, min(32767, value))
            buf += struct.pack('<h', value)
    return pygame.mixer.Sound(buffer=bytes(buf))


class SoundManager:
    """
    Maneja todos los sonidos del juego.
    Genera tonos simples si no hay archivos .wav.
    Si el audio falla, el juego sigue funcionando.
    """

    def __init__(self):
        self.enabled = True
        self.sounds = {}
        self._initialized = False

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self._generate_sounds()
            self._initialized = True
        except Exception:
            self._initialized = False

    def _generate_sounds(self):
        """Genera todos los sonidos del juego."""
        try:
            # Sonido de pasos (ruido corto)
            self.sounds["pasos"] = _generate_noise_burst(0.08, volume=0.08)

            # Sonido de recoger libro (tono ascendente)
            self.sounds["recoger"] = _generate_rising_tone(400, 800, 0.2, volume=0.25)

            # Sonido de hoja nueva (tono suave)
            self.sounds["hoja"] = _generate_rising_tone(300, 500, 0.3, volume=0.15)

            # Sonido de error (tono descendente)
            self.sounds["error"] = _generate_descending_tone(500, 200, 0.4, volume=0.3)

            # Sonido de victoria (fanfarria)
            self.sounds["victoria"] = _generate_victory_fanfare(volume=0.25)

            # Sonido de botón / selección
            self.sounds["select"] = _generate_tone(600, 0.08, volume=0.15)

            # Sonido de tick del reloj
            self.sounds["tick"] = _generate_tone(800, 0.03, volume=0.05)

        except Exception:
            pass

    def play(self, sound_name):
        """Reproduce un sonido por nombre."""
        if not self.enabled or not self._initialized:
            return
        try:
            sound = self.sounds.get(sound_name)
            if sound:
                sound.play()
        except Exception:
            pass

    def toggle(self):
        """Activa/desactiva el sonido. Retorna el nuevo estado."""
        self.enabled = not self.enabled
        if not self.enabled:
            try:
                pygame.mixer.stop()
            except Exception:
                pass
        return self.enabled

    def is_enabled(self):
        """Retorna True si el sonido está activado."""
        return self.enabled
