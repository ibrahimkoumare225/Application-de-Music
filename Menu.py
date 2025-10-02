#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI orientée objet : Choix d'un instrument + mode de jeu
"""
import random
from MusicPlayer_base_original import MusicPlayer, note_to_frequency
from Instrument import Piano, Guitare, Batterie, Flute


def normaliser(texte: str) -> str:
    return texte.strip().lower()
    return texte.strip().lower()


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
            choix = normaliser(
                input("Entrez le numéro ou le nom de l'instrument : "))
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
def mode_clavier(instrument):
    print("🎹 Mode clavier : tapez une lettre de a à z (q pour quitter)")
    alphabet = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    notes = list(note_to_frequency.keys())
    mapping = {lettre: notes[i % len(notes)]
               for i, lettre in enumerate(alphabet)}

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
    fichiers = ["notes_au_clavier", "mario"]
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
