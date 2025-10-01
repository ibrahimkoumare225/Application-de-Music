#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI : Choix d'un instrument + mode de jeu
"""

INSTRUMENTS = {
    "flute": "flûte",
    "flûte": "flûte",
    "guitare": "guitare",
    "batterie": "batterie",
    "drums": "batterie",
    "drum": "batterie"
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

if __name__ == "__main__":
    instrument = choisir_instrument()
    if instrument:
        print(f"\n🎶 Vous avez choisi l’instrument : {instrument}")
        mode = choisir_mode()
        if mode:
            print(f"👉 Mode sélectionné : {mode}")
        else:
            print("Fin du programme.")
    else:
        print("Fin du programme.")
