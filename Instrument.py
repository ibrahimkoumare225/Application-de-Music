import numpy as np
from MusicPlayer_Base import MusicPlayer
from note_frequence_base import note_to_frequency

# Classe abstraite Instrument
class Instrument:
    def __init__(self, player: MusicPlayer, nom: str):
        self.nom = nom
        self.player = player

    def jouer(self, note: str, duration: float):
        """Méthode par défaut : sinus pur"""
        freq = note_to_frequency.get(note, 440)  # défaut = LA4
        self.player.play(freq, duration)


class Flute(Instrument):
    def __init__(self, player):
        super().__init__(player, "Flûte")

    def jouer(self, note: str, duration: float):
        freq = note_to_frequency.get(note, 440)
        self.player.play(freq, duration)


class Guitare(Instrument):
    def __init__(self, player):
        super().__init__(player, "Guitare")

    def jouer(self, note: str, duration: float):
        freq = note_to_frequency.get(note, 440)
        t = np.linspace(0, duration, int(self.player.sample_rate * duration), False)

        # Onde carrée (approximation guitare électrique simple)
        tone = np.sign(np.sin(2 * np.pi * freq * t))
        self.player._play_tone(tone, duration)


class Batterie(Instrument):
    def __init__(self, player):
        super().__init__(player, "Batterie")

    def jouer(self, note: str, duration: float):
        # Percussion : bruit blanc amorti
        t = np.linspace(0, duration, int(self.player.sample_rate * duration), False)
        noise = np.random.uniform(-1, 1, len(t))
        envelope = np.exp(-5 * t)  # décroissance rapide
        tone = noise * envelope
        self.player._play_tone(tone, duration)
