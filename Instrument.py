# Instrument.py
import numpy as np
from MusicPlayer_base_original import MusicPlayer
from note_frequence_base import note_to_frequency

class Instrument:
    def __init__(self, player: MusicPlayer, nom: str):
        self.nom = nom
        self.player = player

    def _note_to_freq(self, note: str):
        """
        Essaie plusieurs formats pour trouver la fréquence :
        - clé exactement telle quelle
        - clé en majuscules (A4)
        - ou si l'utilisateur tape 'la'/'do' on peut éventuellement étendre
        """
        if not note:
            return 440
        # si déjà présent tel quel
        if note in note_to_frequency:
            return note_to_frequency[note]
        # essai en majuscule simple (A4, C#4, ...)
        note_up = note.upper()
        if note_up in note_to_frequency:
            return note_to_frequency[note_up]
        # fallback : LA4
        return 440

    def jouer(self, note: str, duration: float):
        """Méthode par défaut : sinus pur"""
        freq = self._note_to_freq(note)
        self.player.play(freq, duration)


class Flute(Instrument):
    def __init__(self, player):
        super().__init__(player, "Flûte")

    def jouer(self, note: str, duration: float):
        freq = self._note_to_freq(note)
        # Flûte : sinusoïde + léger vibrato (exemple)
        t = np.linspace(0, duration, int(self.player.sample_rate * duration), False)
        vibrato = 1.0 + 0.003 * np.sin(2 * np.pi * 5 * t)  # petit vibrato 5Hz
        tone = np.sin(2 * np.pi * freq * t * vibrato)
        self.player._play_tone(tone, duration)


class Guitare(Instrument):
    def __init__(self, player):
        super().__init__(player, "Guitare")

    def jouer(self, note: str, duration: float):
        freq = self._note_to_freq(note)
        t = np.linspace(0, duration, int(self.player.sample_rate * duration), False)
        # Onde enrichie : somme d'harmoniques avec décroissance
        tone = (0.6 * np.sin(2 * np.pi * freq * t) +
                0.3 * np.sin(2 * np.pi * 2 * freq * t) +
                0.1 * np.sin(2 * np.pi * 3 * freq * t))
        # légère enveloppe d'attaque/décroissance
        env = np.minimum(1, 5 * t) * np.exp(-3 * t)
        tone = tone * env
        self.player._play_tone(tone, duration)

class Piano(Instrument):
    def __init__(self, player):
        super().__init__(player, "Piano")

    def jouer(self, note: str, duration: float):
        freq = note_to_frequency.get(note, 440)
        self.player.play(freq, duration)


class Batterie(Instrument):
    def __init__(self, player):
        super().__init__(player, "Batterie")

    def jouer(self, note: str, duration: float):
        # Percussion : bruit blanc amorti (indépendant de la note)
        t = np.linspace(0, duration, int(self.player.sample_rate * duration), False)
        noise = np.random.uniform(-1, 1, len(t))
        envelope = np.exp(-8 * t)  # décroissance rapide
        tone = noise * envelope
        self.player._play_tone(tone, duration)
