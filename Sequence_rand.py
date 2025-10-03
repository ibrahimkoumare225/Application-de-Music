import numpy as np
import pygame
import random

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


def generate_random_sequence(length=20, mode="mixte"):
    """Génère une séquence de (note, fréquence, durée) selon le mode choisi."""
    notes = list(note_to_frequency.keys())
    sequence = []

    # Définir la durée selon le mode choisi
    if mode == "court":
        fixed_duration = 0.5
    elif mode == "moyen":
        fixed_duration = 1.5
    elif mode == "long":
        fixed_duration = 3.0
    else:
        fixed_duration = None  # mixte => aléatoire

    for _ in range(length):
        note = random.choice(notes)
        freq = note_to_frequency[note]

        if fixed_duration is not None:
            duration = fixed_duration
        else:
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


def ask_duration_mode():
    """Demande à l'utilisateur le mode de durée des notes."""
    modes = {
        "1": ("court", "0.5 s"),
        "2": ("moyen", "1.5 s"),
        "3": ("long", "3.0 s"),
        "4": ("mixte", "durées aléatoires (0.5–3.0 s)")
    }

    print("\nChoisissez la durée des notes :")
    for k, (m, desc) in modes.items():
        print(f"{k}. {m.capitalize()} ({desc})")

    while True:
        choice = input("Votre choix (1-4) : ").strip()
        if choice in modes:
            return modes[choice][0]
        print("❌ Choix invalide, veuillez entrer 1, 2, 3 ou 4.")


def main():
    enable_guitar_hero = False
    mp = MusicPlayer()

    # Demander le nombre de notes
    length = ask_sequence_length()

    # Demander le mode de durée
    mode = ask_duration_mode()

    # Générer et jouer la séquence
    if length >= 100:
        enable_guitar_hero = True
        is_first_time = True
        if enable_guitar_hero and is_first_time:
            print("\n🎸 Mode Guitar Hero activé !")
            print("Retrouver le mode dans le menu principal !\n")
            is_first_time = False
    else:
        seq = generate_random_sequence(length=length, mode=mode)
        for i, (note, freq, dur) in enumerate(seq, start=1):
            print(f"[{i}/{length}] Lecture : {note}, {freq} Hz, Durée : {dur:.2f} s")
            mp.play(freq, dur)

    print("\n✅ Séquence aléatoire terminée.")
    return enable_guitar_hero


if __name__ == "__main__":
    main()
