import numpy as np
import pygame
import random
import sys

from note_frequence_base import note_to_frequency
from guitar_hero import play_guitar_hero


class MusicPlayer:
    def __init__(self, sample_rate=44100):
        pygame.mixer.pre_init(frequency=sample_rate, size=-16, channels=2)
        pygame.init()
        self.sample_rate = sample_rate

    def _make_tone(self, frequency, duration=0.5):
        t = np.linspace(0, duration, int(
            self.sample_rate * duration), endpoint=False)
        wave = np.sin(2 * np.pi * frequency * t)

        # Petit envelope pour éviter les clics
        attack_len = int(0.01 * self.sample_rate)
        decay_len = int(0.01 * self.sample_rate)
        env = np.ones_like(wave)
        env[:attack_len] = np.linspace(0, 1, attack_len)
        env[-decay_len:] = np.linspace(1, 0, decay_len)
        wave *= env

        stereo = np.vstack((wave, wave)).T
        audio = np.ascontiguousarray((32767 * stereo).astype(np.int16))
        sound = pygame.sndarray.make_sound(audio)
        sound.set_volume(0.1)
        return sound

    def play(self, frequency, duration=0.5):
        sound = self._make_tone(frequency, duration)
        sound.play()
        pygame.time.delay(int(duration * 1000))


def generate_random_sequence(length=20):
    """Génère une séquence aléatoire de (note, fréquence, durée)."""
    notes = list(note_to_frequency.keys())
    sequence = []
    for _ in range(length):
        note = random.choice(notes)
        freq = note_to_frequency[note]
        # durée aléatoire entre 0.5 et 3 secondes
        duration = random.uniform(0.5, 3.0)
        sequence.append((note, freq, duration))
    return sequence


def ask_sequence_length():
    """Demande à l'utilisateur combien de notes jouer."""
    while True:
        try:
            n = int(input("Combien de notes voulez-vous jouer ? "))
            if n > 0:
                return n
            else:
                print("Le nombre doit être supérieur à 0.")
        except ValueError:
            print("Veuillez entrer un nombre entier valide.")


def main():
    mp = MusicPlayer()

    # Demander le nombre de notes
    length = ask_sequence_length()

    # Générer et jouer la séquence
    if length >= 100:
        play_guitar_hero(length)
    else:
        seq = generate_random_sequence(length=length)
        for note, freq, dur in seq:
            print(
                f"Lecture : {note}, Fréquence : {freq} Hz, Durée : {dur:.2f} s")
            mp.play(freq, dur)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
