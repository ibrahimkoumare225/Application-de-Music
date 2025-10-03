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


class Guitare:
    def __init__(self, player: MusicPlayer):
        self.nom = "Guitare"
        self.player = player
        self.SAMPLE_RATE = 44100
        self.BITS = -16
        self.CHANNELS = 2
        self.MAX_VOLUME = 0.6
        self.NOTE_DURATION = 1.5
        self.record_file = "touches_guitare.txt"
        self.recorded_notes = []

        if not pygame.get_init():
            pygame.init()
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=self.SAMPLE_RATE, size=self.BITS, channels=self.CHANNELS)

        self.KEY_NOTE_MAP = {
            pygame.K_a: "E3",
            pygame.K_z: "A3",
            pygame.K_e: "D4",
            pygame.K_r: "G4",
            pygame.K_t: "B4",
            pygame.K_y: "E5",
        }

        self.note_sounds = {}
        for key, note in self.KEY_NOTE_MAP.items():
            freq = note_to_frequency[note]
            wave = self.make_guitar_wave(freq)
            arr = self.to_stereo(wave)
            self.note_sounds[key] = pygame.sndarray.make_sound(arr)

    def make_guitar_wave(self, freq, duration=None):
        if duration is None:
            duration = self.NOTE_DURATION
        t = np.linspace(0, duration, int(self.SAMPLE_RATE * duration), False)
        wave = 0.7*np.sin(2*np.pi*freq*t) + 0.3*np.sin(2*np.pi*2*freq*t) + 0.2*np.sin(2*np.pi*3*freq*t)
        envelope = np.linspace(0, 1, int(0.005*self.SAMPLE_RATE))
        wave[:len(envelope)] *= envelope
        return wave.astype(np.float32)

    def to_stereo(self, wave, volume=None):
        if volume is None:
            volume = self.MAX_VOLUME
        wav = np.clip(wave * (32767 * volume), -32768, 32767).astype(np.int16)
        if self.CHANNELS == 2:
            wav = np.column_stack((wav, wav))
        return wav

    def interface_guitare(self):
        """Affiche l'interface guitare et enregistre les touches jouées"""
        # Ferme l'ancienne fenêtre si existante
        pygame.display.quit()
        pygame.display.init()
        window = pygame.display.set_mode((600, 200))
        pygame.display.set_caption("Clavier Guitare")
        font = pygame.font.SysFont(None, 28)

        running = True
        pressed_keys = set()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Croix fermée
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.note_sounds:
                        self.note_sounds[event.key].play()
                        pressed_keys.add(event.key)
                        self.recorded_notes.append(f"{self.KEY_NOTE_MAP[event.key]} {self.NOTE_DURATION:.3f}")
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.KEYUP:
                    pressed_keys.discard(event.key)

            window.fill((20, 20, 20))
            y = 40
            for k, note in self.KEY_NOTE_MAP.items():
                color = (255, 0, 0) if k in pressed_keys else (255, 255, 100)
                img = font.render(f"Touche {pygame.key.name(k)} -> {note}", True, color)
                window.blit(img, (20, y))
                y += 25
            pygame.display.flip()

        # Sauvegarde des notes
        with open(self.record_file, "w", encoding="utf-8") as f:
            for line in self.recorded_notes:
                f.write(line + "\n")
        print(f"💾 Enregistrement guitare sauvegardé dans {self.record_file}")

        # Ferme juste la fenêtre Pygame, pas tout Pygame
        pygame.display.quit()


# ========================= CLASSE PIANO =========================
class Piano:
    def __init__(self, player: MusicPlayer):
        self.nom = "Piano"
        self.player = player
        self.SAMPLE_RATE = 44100
        self.BITS = -16
        self.CHANNELS = 2
        self.MAX_VOLUME = 0.5
        self.NOTE_DURATION = 1.0
        self.record_file = "touches_piano.txt"
        self.recorded_notes = []

        if not pygame.get_init(): pygame.init()
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=self.SAMPLE_RATE, size=self.BITS, channels=self.CHANNELS)

        self.KEY_NOTE_MAP = {
            pygame.K_a:"C4", pygame.K_1:"C#4", pygame.K_z:"D4", pygame.K_2:"D#4",
            pygame.K_e:"E4", pygame.K_r:"F4", pygame.K_3:"F#4", pygame.K_t:"G4",
            pygame.K_4:"G#4", pygame.K_y:"A4", pygame.K_5:"A#4", pygame.K_u:"B4",
            pygame.K_i:"C5", pygame.K_6:"C#5", pygame.K_o:"D5", pygame.K_7:"D#5",
            pygame.K_p:"E5", pygame.K_f:"F5", pygame.K_8:"F#5", pygame.K_9:"G5",
            pygame.K_SEMICOLON:"G#5", pygame.K_g:"G4", pygame.K_h:"A4", pygame.K_j:"B4"
        }

        self.note_sounds = {}
        for key,note in self.KEY_NOTE_MAP.items():
            freq = note_to_frequency[note]
            wave = self.make_wave(freq)
            arr = self.to_stereo(wave)
            self.note_sounds[key] = pygame.sndarray.make_sound(arr)

    def make_wave(self,freq,duration=None):
        if duration is None: duration=self.NOTE_DURATION
        t = np.linspace(0,duration,int(self.SAMPLE_RATE*duration),False)
        wave = np.sin(2*np.pi*freq*t)
        attack = int(0.02*self.SAMPLE_RATE)
        envelope = np.ones_like(wave)
        envelope[:attack] = np.linspace(0,1,attack)
        envelope[attack:] = np.exp(-3*(t[attack:]/duration))
        return (wave*envelope).astype(np.float32)

    def to_stereo(self,wave,volume=None):
        if volume is None: volume=self.MAX_VOLUME
        wav = np.clip(wave*(32767*volume), -32768,32767).astype(np.int16)
        if self.CHANNELS==2: wav = np.column_stack((wav,wav))
        return wav

    def interface_piano(self):
        pygame.display.quit()
        pygame.display.init()
        white_keys_list=[pygame.K_a,pygame.K_z,pygame.K_e,pygame.K_r,pygame.K_t,pygame.K_y,pygame.K_u,pygame.K_i,pygame.K_o,pygame.K_p,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_j]
        black_keys_list=[pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_SEMICOLON]

        window = pygame.display.set_mode((14*60,300))
        pygame.display.set_caption("🎹 Clavier Piano")
        font = pygame.font.SysFont(None,24)
        running=True
        pressed_keys=set()
        WHITE=(255,255,255);BLACK=(0,0,0);GRAY=(50,50,50);RED=(255,0,0);BLUE_PRESSED=(50,150,255)
        white_key_width=60;white_key_height=250
        black_key_width=35;black_key_height=150
        black_positions=[0,1,3,4,5,7,8,10,11,12]

        while running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT: running=False
                elif event.type==pygame.KEYDOWN:
                    if event.key in self.note_sounds:
                        self.note_sounds[event.key].play()
                        pressed_keys.add(event.key)
                        self.recorded_notes.append(f"{self.KEY_NOTE_MAP[event.key]} {self.NOTE_DURATION:.3f}")
                    elif event.key==pygame.K_ESCAPE: running=False
                elif event.type==pygame.KEYUP:
                    pressed_keys.discard(event.key)

            window.fill((30,30,30))
            for i,key in enumerate(white_keys_list):
                color=RED if key in pressed_keys else WHITE
                pygame.draw.rect(window,color,(i*white_key_width,0,white_key_width,white_key_height))
                pygame.draw.rect(window,BLACK,(i*white_key_width,0,white_key_width,white_key_height),2)
                window.blit(font.render(pygame.key.name(key),True,BLACK),(i*white_key_width+10,white_key_height-30))
            for i,key in enumerate(black_keys_list):
                if i<len(black_positions):
                    x=black_positions[i]*white_key_width+white_key_width-black_key_width//2
                    color=BLUE_PRESSED if key in pressed_keys else BLACK
                    pygame.draw.rect(window,color,(x,0,black_key_width,black_key_height))
                    pygame.draw.rect(window,GRAY,(x,0,black_key_width,black_key_height),2)
                    window.blit(font.render(pygame.key.name(key),True,WHITE),(x+5,30))
            pygame.display.flip()

        with open(self.record_file,"w",encoding="utf-8") as f:
            for line in self.recorded_notes: f.write(line+"\n")
        print(f"💾 Enregistrement sauvegardé dans {self.record_file}")
        pygame.display.quit()


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
        "2": "fichier",
        "1": "clavier",
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
        self.enable_guitar_hero = False

    def afficher_menu_instruments(self):
        print("=== Choix de l'instrument ===")
        print("1) Piano")
        print("2) Guitare")
        print("3) Batterie")
        print("q) Quitter\n")

    def afficher_menu_modes(self):
        print("\n=== Choix du mode de jeu ===")
        print("1) Notes au clavier (a–z / interface piano)")
        print("2) À partir d’un fichier")
        print("3) Aléatoire")
        if self.enable_guitar_hero:
            print("4) Guitar Hero")
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

        while True:
            self.mode = self.choisir_mode()
            if not self.mode:
                print("Fin du programme.")
                return

            rejouer_mode = True
            while rejouer_mode:
                if self.mode == "clavier" and isinstance(self.instrument, Piano):
                    self.instrument.interface_piano()
                elif self.mode == "clavier" and isinstance(self.instrument, Guitare):
                    self.instrument.interface_guitare()
                elif self.mode == "clavier":
                    mode_clavier(self.instrument)
                elif self.mode == "aléatoire":
                    self.enable_guitar_hero = mode_aleatoire(self.instrument)
                    if self.enable_guitar_hero and not "4" in self.MODES:
                        self.MODES["4"] = "guitar hero"
                elif self.mode == "fichier":
                    menu_fichier(self.instrument)
                elif self.mode == "guitar hero" and self.enable_guitar_hero:
                    from guitar_hero import play_guitar_hero
                    play_guitar_hero()

                print(f"\n👉 Mode terminé : {self.mode}")
                choix = input(
                    "Voulez-vous [r] rejouer ce mode, [p] retour menu principal, [m] menu des modes, [q] quitter ? ").strip().lower()
                if choix == "r":
                    continue
                elif choix == "p":
                    return  # retour au menu principal
                elif choix == "m":
                    break  # retour au menu des modes
                elif choix == "q":
                    print("✅ Merci d'avoir joué, à bientôt !")
                    exit(0)


# === Modes génériques pour autres instruments ===
def mode_clavier(instrument):
    print("🎼 Mode clavier (a–z)")
    alphabet = [chr(i) for i in range(ord("a"), ord("z") + 1)]
    notes = list(note_to_frequency.keys())
    mapping = {lettre: notes[i % len(notes)]
               for i, lettre in enumerate(alphabet)}

    while True:
        touche = normaliser(input("Lettre (q pour quitter le mode) : "))
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
    enable_guitar_hero = main_sequence_rand()
    print("✅ Séquence aléatoire terminée.")
    return enable_guitar_hero


def menu_fichier(instrument):
    fichiers = ["pirate.txt", "mario.txt"]
    for i, f in enumerate(fichiers, 1):
        print(f"{i}) {f}")
    while True:
        choix = input("Votre choix (q pour quitter le mode) : ")
        if choix == "1":
            mp = MusicPlayer()
            mp.play_from_file("pirate.txt")
            break
        elif choix == "2":
            mp = MusicPlayer()
            mp.play_from_file("mario.txt")
            break
        elif choix == "q":
            break
        else:
            print("❌ Choix invalide.")


if __name__ == "__main__":
    while True:
        jeu = Menu()
        jeu.lancer()
