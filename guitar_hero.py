import random
import time
from note_frequence_base import note_to_frequency
from MusicPlayer_base_original import MusicPlayer


def choose_notes():
    notes = list(note_to_frequency.keys())
    return random.sample(notes, 5)


def has_note_been_pressed(key_to_press, pressed_key):
    return key_to_press == pressed_key


def has_time_elapsed(start_time, duration):
    return (time.time() + duration) <= (start_time + duration)


def get_duration(mode):
    match mode:
        case "court":
            return 0.5
        case "moyen":
            return 1.5
        case "long":
            return 3.0
        case "mixte":
            return random.uniform(0.5, 3.0)


def play_guitar_hero(mode):
    print("Bienvenue dans le jeu Guitar Hero !")
    keys = ["A", "Z", "E", "R", "T"]
    correct = 0
    errors = 0
    mp = MusicPlayer()
    notes = choose_notes()
    time_in_seconds = input("Combien de secondes voulez-vous jouer ? ")
    time_in_seconds = int(time_in_seconds)
    nb_notes = time_in_seconds / get_duration(mode)
    keys_and_notes = [(note, key) for note, key in zip(
        random.choices(notes, k=nb_notes), random.choices(keys, k=nb_notes))]
    for i in range(nb_notes):
        duration = get_duration(mode)
        print(
            f"{keys_and_notes[i][1]} pour jouer {keys_and_notes[i][0]}")
        mp.play(note_to_frequency[keys_and_notes[i]
                                  [0]], duration)
        pressed_key = input()

        if has_note_been_pressed(keys_and_notes[i][1], pressed_key):
            print("Correct!")
            correct += 1
            continue
        else:
            print("Raté !")
            errors += 1

    print("Jeu terminé ! Vous avez eu", correct,
          "corrects et", errors, "erreurs.")
