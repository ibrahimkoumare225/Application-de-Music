#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI orientée objet : Choix d'un instrument + mode de jeu
"""
import random
import pygame
import numpy as np
from note_frequence_base import note_to_frequency
from Sequence_rand import main as main_sequence_rand

# --- Classe MusicPlayer de base ---
from MusicPlayer_base_original import MusicPlayer

# --- Classe Instrument ---
from Instrument import Guitare, Batterie, Flute


def normaliser(texte: str) -> str:
    return texte.strip().lower()


# --- Classe Piano avec interface Pygame ---
class Piano:
    def __init__(self, player: MusicPlayer):
        self.nom = "Piano"
        self.player = player
        self.SAMPLE_RATE = 44100
        self.BITS = -16
        self.CHANNELS = 2
        self.MAX_VOLUME = 0.5
        self.NOTE_DURATION = 1.0

        pygame.mixer.init(frequency=self.SAMPLE_RATE, size=self.BITS, channels=self.CHANNELS)
        pygame.init()

        # Mapping clavier -> notes
        self.KEY_NOTE_MAP = {
            pygame.K_a: "C4",
            pygame.K_s: "D4",
            pygame.K_d: "E4",
            pygame.K_f: "F4",
            pygame.K_g: "G4",
            pygame.K_h: "A4",
            pygame.K_j: "B4",
            pygame.K_k: "C5",
        }

        # Préparer les sons
        self.note_sounds = {}
        for key, note in self.KEY_NOTE_MAP.items():
            freq = note_to_frequency[note]
            wave = self.make_wave(freq, duration=self.NOTE_DURATION)
            arr = self.to_stereo(wave)
            sound = pygame.sndarray.make_sound(arr)
            self.note_sounds[key] = sound

    def make_wave(self, freq, duration=None):
        if duration is None:
            duration = self.NOTE_DURATION
        t = np.linspace(0, duration, int(self.SAMPLE_RATE * duration), False)
        wave = np.sin(2 * np.pi * freq * t)

        # Enveloppe ADSR simplifiée
        attack = int(0.02 * self.SAMPLE_RATE)
        envelope = np.ones_like(wave)
        envelope[:attack] = np.linspace(0, 1, attack)
        envelope[attack:] = np.exp(-3 * (t[attack:] / duration))
        return (wave * envelope).astype(np.float32)

    def to_stereo(self, wave, volume=None):
        if volume is None:
            volume = self.MAX_VOLUME
        wav = wave * (32767 * volume)
        wav = np.clip(wav, -32768, 32767).astype(np.int16)
        if self.CHANNELS == 2:
            wav = np.column_stack((wav, wav))
        return wav

    def jouer(self, note: str, duration: float = None):
        # Jouer via le mapping clavier interne si note correspond
        key = None
        for k, n in self.KEY_NOTE_MAP.items():
            if n == note:
                key = k
                break
        if key and key in self.note_sounds:
            self.note_sounds[key].play()
            pygame.time.delay(int((duration or self.NOTE_DURATION) * 1000))
        else:
            print(f"❌ Note inconnue : {note}")

    def interface_piano(self):
        """Lancer l'interface graphique Pygame du piano"""
        window = pygame.display.set_mode((600, 200))
        pygame.display.set_caption("Clavier Piano")
        font = pygame.font.SysFont(None, 24)
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.note_sounds:
                        self.note_sounds[event.key].play()
                    if event.key == pygame.K_ESCAPE:
                        running = False

            window.fill((0, 0, 0))
            y = 50
            for k, note in self.KEY_NOTE_MAP.items():
                txt = f"Touche {pygame.key.name(k)} -> {note}"
                img = font.render(txt, True, (255, 255, 255))
                window.blit(img, (20, y))
                y += 30
            pygame.display.flip()

        pygame.quit()


# --- Menu principal ---
class Menu:
    INSTRUMENTS = {
        "1": Piano,
        "2": Guitare,
        "3": Batterie,
        "4": Flute,
        "piano": Piano,
        "guitare": Guitare,
        "batterie": Batterie,
        "flute": Flute,
        "flûte": Flute,
        "drum": Batterie,
        "drums": Batterie,
    }

    MODES = {
        "3": "fichier",
        "1": "clavier",
        "2": "aléatoire",
        "fichier": "fichier",
        "clavier": "clavier",
        "aleatoire": "aléatoire",
        "aléatoire": "aléatoire",
    }

    def __init__(self):
        self.instrument = None
        self.mode = None
        self.player = MusicPlayer()

    def afficher_menu_instruments(self):
        print("=== Choix de l'instrument ===")
        print("1) Piano")
        print("2) Guitare")
        print("3) Batterie")
        print("4) Flûte")
        print("q) Quitter\n")

    def afficher_menu_modes(self):
        print("\n=== Choix du mode de jeu ===")
        print("1) Notes au clavier (a–z / interface piano)")
        print("2) Aléatoire")
        print("3) À partir d’un fichier")
        print("q) Quitter\n")

    def choisir_instrument(self):
        while True:
            self.afficher_menu_instruments()
            choix = normaliser(input("Entrez le numéro ou le nom de l'instrument : "))
            if choix in self.INSTRUMENTS:
                return self.INSTRUMENTS[choix](self.player)
            elif choix in ("q", "quit", "exit"):
                return None
            else:
                print("❌ Entrée invalide, réessayez.\n")

    def choisir_mode(self):
        while True:
            self.afficher_menu_modes()
            choix = normaliser(input("Entrez le numéro ou le nom du mode : "))
            if choix in self.MODES:
                return self.MODES[choix]
            elif choix in ("q", "quit", "exit"):
                return None
            else:
                print("❌ Entrée invalide, réessayez.\n")

    def lancer(self):
        self.instrument = self.choisir_instrument()
        if not self.instrument:
            print("Fin du programme.")
            return

        print(f"\n🎶 Vous avez choisi l’instrument : {self.instrument.nom}")
        self.mode = self.choisir_mode()

        if not self.mode:
            print("Fin du programme.")
            return

        # Si c'est le piano et mode clavier, lancer l'interface Pygame
        if self.mode == "clavier" and isinstance(self.instrument, Piano):
            self.instrument.interface_piano()
        elif self.mode == "clavier":
            mode_clavier(self.instrument)
        elif self.mode == "aléatoire":
            mode_aleatoire(self.instrument)
        elif self.mode == "fichier":
            menu_fichier(self.instrument)

        print(f"👉 Mode sélectionné : {self.mode}")


# === Modes génériques pour autres instruments ===
def mode_clavier(instrument):
    print("🎼 Mode clavier (a–z)")
    alphabet = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    notes = list(note_to_frequency.keys())
    mapping = {lettre: notes[i % len(notes)] for i, lettre in enumerate(alphabet)}

    while True:
        touche = normaliser(input("Lettre : "))
        if touche == "q":
            break
        elif touche in mapping:
            note = mapping[touche]
            print(f"🎵 Lettre '{touche}' → note {note}")
            instrument.jouer(note, 0.5)
        else:
            print("❌ Entrée invalide (a–z seulement).")


def mode_aleatoire(instrument):
    print("🎲 Mode aléatoire : lancement de la séquence aléatoire")
    main_sequence_rand()  # Utilise le code de Sequence_rand.py


def menu_fichier(instrument):
    fichiers = ["pirate.txt", "mario.txt"]
    for i, f in enumerate(fichiers, 1):
        print(f"{i}) {f}")
    while True:
        choix = input("Votre choix : ")
        if choix == "1":
            mp = MusicPlayer()
            mp.play_from_file("pirate.txt")
            break
        elif choix == "2":
            mp = MusicPlayer()
            mp.play_from_file("mario.txt")
            break
        else:
            print("❌ Choix invalide.")


if __name__ == "__main__":
    jeu = Menu()
    jeu.lancer()
