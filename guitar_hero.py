import random
import time
from note_frequence_base import note_to_frequency
from MusicPlayer_base_original import MusicPlayer


def duration_generator():
    return random.choice([0.5, 1, 1.5, 2])


def choose_notes():
    notes = list(note_to_frequency.keys())
    return random.sample(notes, 5)


def has_note_been_pressed(key_to_press, pressed_key):
    return key_to_press == pressed_key


def has_time_elapsed(start_time, duration):
    return (time.time() - start_time) <= (time.time() + duration)


def play_guitar_hero(iterations):
    print("Bienvenue dans le jeu Guitar Hero !")
    correct = 0
    errors = 0
    mp = MusicPlayer()
    notes = choose_notes()
    keys = ["A", "Z", "E", "R", "T"]
    keys_and_notes = [(note, key) for note, key in zip(notes, keys)]
    for i in range(iterations):
        duration = duration_generator()
        start_time = time.time()
        pressed_key = input()
        print(
            f"Appuyez sur {keys_and_notes[i][1]} pour jouer {keys_and_notes[i][0]} pendant {duration} secondes.")
        if has_note_been_pressed(keys_and_notes[i][1], pressed_key) and not has_time_elapsed(start_time, duration):
            print("Correct!")
            mp.play(note_to_frequency[keys_and_notes[i][0]])
            correct += 1
        else:
            print("Raté !")
            errors += 1

    print("Jeu terminé ! Vous avez eu", correct,
          "corrects et", errors, "erreurs.")
