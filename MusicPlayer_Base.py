# installer avec: pip install pygame
#                 pip install numpy 
      
import numpy as np
import pygame

from note_frequence_base import note_to_frequency

# classe qui permet de jouer de la musique grâce à pygame
class MusicPlayer:
    def __init__(self, sample_rate=44100):
        pygame.mixer.init(frequency=44100, size=-16, channels=2)
        self.sample_rate = sample_rate

    # c'est le tone passé en entrée qu'il faudra modifier en fonction de l'instrument joué
    # cette méthode pourra être appelée ensuite quelque soit l'instrument choisis
    def _play_tone(self, tone, duration):
        stereo_tone = np.vstack((tone, tone)).T
        contiguous_tone = np.ascontiguousarray((32767 * stereo_tone).astype(np.int16))
        sound = pygame.sndarray.make_sound(contiguous_tone)
        sound.set_volume(0.05)  # Réglez le volume
        sound.play()
        pygame.time.delay(int(duration * 1000)) #tenir la note la durée voulue

    # Exemple de tonalité, extraire ce qui va bien pour pouvoir faire varier, pour simuler différents instruments
    def play(self, frequency, duration):
        # Créer une onde sinusoïdale à la fréquence spécifiée
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        tone = np.sin(frequency * 2 * np.pi * t)

        # Créer un tableau stéréo (2D) en dupliquant le ton
        stereo_tone = np.vstack((tone, tone)).T

        # S'assurer que le tableau est contigu en mémoire
        contiguous_tone = np.ascontiguousarray((32767 * stereo_tone).astype(np.int16))

        # Convertir l'onde sinusoïdale en un format audio et jouer
        sound = pygame.sndarray.make_sound(contiguous_tone)
        sound.set_volume(0.05)  # Réglez le volume
        sound.play()
        pygame.time.delay(int(duration * 500)) 



# code exemple pour jouer des notes :

if __name__ == "__main__" :
    mp = MusicPlayer()
    mp.play(note_to_frequency["F7"], 1)
    mp.play(note_to_frequency["B3"], 4)
    mp.play(note_to_frequency["E5"], 0.5)