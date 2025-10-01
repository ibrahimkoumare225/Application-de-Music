#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main.py : CLI choix instrument + mode + génération de son
"""

import random
from MusicPlayer_Base import MusicPlayer
from note_frequence_base import note_to_frequency
from Instrument import Flute, Guitare, Batterie   # <-- fichier où tu as défini tes classes

INSTRUMENTS = {
    "flûte": Flute,
    "flute": Flute,
    "guitare": Guitare,
    "batterie": Batterie,
    "drums": Batterie,
    "drum": Batterie
}

MODES = {
    "1": "aléatoire",
    "2": "clavier",
    "3": "fichier",
    "aleatoire": "aléatoire",
    "aléatoire": "aléatoire",
    "clavier": "clavier",
    "fichier": "fichier"
}

def afficher_menu_instruments():
    print("=== Choix de l'instrument ===")
    print("1) Flûte")
    print("2) Guitare")
    print("3) Batterie")
    print("q) Quitter")
    print()

def afficher_menu_modes():
    print("\n=== Choix du mode de jeu ===")
    print("1) Aléatoire")
    print("2) Notes au clavier")
    print("3) À partir d’un fichier")
    print("q) Quitter")
    print()

def normaliser(texte: str) -> str:
    return texte.strip().lower()

def choisir_instrument():
    while True:
        afficher_menu_instruments()
        choix = normaliser(input("Entrez le numéro ou le nom de l'instrument : "))

        if choix in ("1", "flute", "flûte"):
            return "flûte"
        elif choix in ("2", "guitare"):
            return "guitare"
        elif choix in ("3", "batterie", "drum", "drums"):
            return "batterie"
        elif choix in ("q", "quit", "exit"):
            return None
        else:
            print("❌ Entrée invalide, réessayez.\n")

def choisir_mode():
    while True:
        afficher_menu_modes()
        choix = normaliser(input("Entrez le numéro ou le nom du mode : "))

        if choix in MODES:
            return MODES[choix]
        elif choix in ("q", "quit", "exit"):
            return None
        else:
            print("❌ Entrée invalide, réessayez.\n")

def mode_aleatoire(instrument):
    notes = random.sample(list(note_to_frequency.keys()), 5)
    print(f"🎲 Notes générées aléatoirement : {notes}")
    for note in notes:
        instrument.jouer(note, 0.5)

def mode_clavier(instrument):
    print("⌨️ Entrez des notes (ex: C4, E4, A3). Tapez 'q' pour quitter.")
    while True:
        note = input("Note : ").strip()
        if note.lower() == "q":
            break
        if note in note_to_frequency:
            instrument.jouer(note, 0.7)
        else:
            print("❌ Note inconnue.")

def mode_fichier(instrument):
    chemin = input("Entrez le chemin du fichier de notes (.txt) : ").strip()
    try:
        with open(chemin, "r") as f:
            notes = [line.strip() for line in f if line.strip()]
        print(f"📂 Notes lues : {notes}")
        for note in notes:
            if note in note_to_frequency:
                instrument.jouer(note, 0.7)
            else:
                print(f"❌ Note '{note}' inconnue, ignorée.")
    except FileNotFoundError:
        print("❌ Fichier introuvable.")

if __name__ == "__main__":
    instrument_nom = choisir_instrument()
    if instrument_nom:
        mp = MusicPlayer()
        instrument_class = INSTRUMENTS[instrument_nom]
        instrument = instrument_class(mp)

        print(f"\n🎶 Vous avez choisi l’instrument : {instrument.nom}")
        mode = choisir_mode()
        if mode == "aléatoire":
            mode_aleatoire(instrument)
        elif mode == "clavier":
            mode_clavier(instrument)
        elif mode == "fichier":
            mode_fichier(instrument)
        else:
            print("Fin du programme.")
    else:
        print("Fin du programme.")
