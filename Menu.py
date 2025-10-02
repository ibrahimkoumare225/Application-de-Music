#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI orientée objet : Choix d'un instrument + mode de jeu
"""
from MusicPlayer_base_original import MusicPlayer

def normaliser(texte: str) -> str:
        return texte.strip().lower()

class Menu:
    INSTRUMENTS = {
        "flute": "flûte",
        "flûte": "flûte",
        "guitare": "guitare",
        "batterie": "batterie",
        "piano": "piano",
        "drums": "batterie",
        "drum": "batterie"
    }

    MODES = {
        
        "1": "clavier",
        "2": "aléatoire",
        "3": "fichier",
        "aleatoire": "aléatoire",
        "aléatoire": "aléatoire",
        "clavier": "clavier",
        "fichier": "fichier"
    }

    def __init__(self):
        self.instrument = None
        self.mode = None

    def afficher_menu_instruments(self):
        print("=== Choix de l'instrument ===")
        print("1) Piano")
        print("2) Guitare")
        print("3) Batterie")
        print("4) Flûte")
        print("q) Quitter")
        print()

    def afficher_menu_modes(self):
        print("\n=== Choix du mode de jeu ===")
        print("1) Notes au clavier")
        print("2) Aléatoire")
        print("3) À partir d’un fichier")
        print("q) Quitter")
        print()

    def choisir_instrument(self):
        while True:
            self.afficher_menu_instruments()
            choix = normaliser(input("Entrez le numéro ou le nom de l'instrument : "))

            if choix in ("1", "piano"):
                return "piano"
            elif choix in ("2", "guitare"):
                return "guitare"
            elif choix in ("3", "batterie", "drum", "drums"):
                return "batterie"
            elif choix in ("4", "flute", "flûte"):
                return "flûte"
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
        if self.instrument:
            print(f"\n🎶 Vous avez choisi l’instrument : {self.instrument}")
            self.mode = self.choisir_mode()
            if "fichier" in self.mode:
                menu_fichier(["pirate", "mario"])

            if self.mode:
                print(f"👉 Mode sélectionné : {self.mode}")
            else:
                print("Fin du programme.")
        else:
            print("Fin du programme.")

def menu_fichier(file_list):
    for i, file in enumerate(file_list, start=1):
        print(f"{i}. {file}")
    while True:
        choix = input("Taper le chiffre du fichier que vous souhaiter jouer: ")
        mp = MusicPlayer()
        match choix: 
            case "1":
                mp.play_from_file("pirate.txt")
                return None
            case "2":
                mp.play_from_file("mario.txt")
                return None
            case _: 
                print("Le chiffre choisi n'est pas valide")
    
if __name__ == "__main__":
    jeu = Menu()
    jeu.lancer()
