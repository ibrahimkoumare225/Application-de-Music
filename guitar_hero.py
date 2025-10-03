import random
import time
from note_frequence_base import note_to_frequency
from MusicPlayer_base_original import MusicPlayer
import select
import sys


def choose_notes():
    notes = list(note_to_frequency.keys())
    return random.sample(notes, 5)


def has_note_been_pressed(key_to_press, pressed_key):
    return key_to_press == pressed_key


def has_time_elapsed(start_time, duration):
    return (time.time() + duration) <= (start_time + duration)


def play_guitar_hero():
    print("Bienvenue dans le jeu Guitar Hero !")
    correct = 0
    errors = 0
    mp = MusicPlayer()
    notes = choose_notes()
    time_in_seconds = input("Combien de secondes voulez-vous jouer ? ")
    time_in_seconds = int(time_in_seconds)
    keys = ["A", "Z", "E", "R", "T"]
    keys_and_notes = [(note, key) for note, key in zip(
        random.choices(notes, k=time_in_seconds), random.choices(keys, k=time_in_seconds))]
    for i in range(time_in_seconds):
        print(
            f"{keys_and_notes[i][1]} pour jouer {keys_and_notes[i][0]}")
        mp.play(note_to_frequency[keys_and_notes[i]
                                  [0]], 1)
        ready, _, _ = select.select([sys.stdin], [], [], 1)
        if ready:
            pressed_key = sys.stdin.readline().strip()
        else:
            pressed_key = ""
            print("Raté !")
            errors += 1
        if has_note_been_pressed(keys_and_notes[i][1], pressed_key):
            print("Correct!")
            correct += 1
            continue

    print("Jeu terminé ! Vous avez eu", correct,
          "corrects et", errors, "erreurs.")
