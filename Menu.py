#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI orientée objet : Choix d'un instrument + mode de jeu
"""
import random
import pygame
import numpy as np
from note_frequence_base import note_to_frequency

# --- Classe MusicPlayer de base ---
from MusicPlayer_base_original import MusicPlayer

# --- Classe Instrument ---
from Instrument import Guitare, Batterie, Flute


def normaliser(texte: str) -> str:
    return texte.strip().lower()


# --- Classe Piano avec son intégré ---
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
        if note not in note_to_frequency:
            print(f"❌ Note inconnue : {note}")
            return
        freq = note_to_frequency[note]
        wave = self.make_wave(freq, duration)
        arr = self.to_stereo(wave)
        sound = pygame.sndarray.make_sound(arr)
        sound.play()
        pygame.time.delay(int((duration or self.NOTE_DURATION) * 1000))


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
        "1": "fichier",
        "2": "clavier",
        "3": "aléatoire",
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
        print("1) À partir d’un fichier")
        print("2) Notes au clavier (a–z)")
        print("3) Aléatoire")
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

        if self.mode == "clavier":
            mode_clavier(self.instrument)
        elif self.mode == "aléatoire":
            mode_aleatoire(self.instrument)
        elif self.mode == "fichier":
            menu_fichier(self.instrument)

        print(f"👉 Mode sélectionné : {self.mode}")


# === Modes de jeu ===
# === Modes de jeu ===
def mode_clavier(instrument):
    if isinstance(instrument, Piano):
        # Mapping spécifique au piano
        KEY_NOTE_MAP = {
            "a": "C4",
            "s": "D4",
            "d": "E4",
            "f": "F4",
            "g": "G4",
            "h": "A4",
            "j": "B4",
            "k": "C5",
        }

        print("🎹 Mode clavier Piano :")
        for key, note in KEY_NOTE_MAP.items():
            print(f"   Touche '{key}' → {note}")
        print("Tapez q pour quitter.\n")

        while True:
            touche = normaliser(input("Lettre : "))
            if touche == "q":
                break
            elif touche in KEY_NOTE_MAP:
                note = KEY_NOTE_MAP[touche]
                print(f"🎵 {touche} → {note}")
                instrument.jouer(note, 0.8)
            else:
                print("❌ Touche invalide. Utilisez seulement : " +
                      ", ".join(KEY_NOTE_MAP.keys()))

    else:
        # Mode générique pour les autres instruments
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
    notes = random.sample(list(note_to_frequency.keys()), 5)
    print(f"🎲 Notes générées aléatoirement : {notes}")
    for note in notes:
        instrument.jouer(note, 0.5)


def menu_fichier(instrument):
    fichiers = ["pirate.txt", "mario.txt"]
    for i, f in enumerate(fichiers, 1):
        print(f"{i}) {f}")
    while True:
        choix = input("Votre choix : ")
        if choix == "1":
            mode_clavier(instrument)
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
