
import pygame
import numpy as np
from note_frequence_base import note_to_frequency

#code fonctionnel sur les touches


# --- Configuration audio ---
SAMPLE_RATE = 44100
BITS = -16
CHANNELS = 2
MAX_VOLUME = 0.5
NOTE_DURATION = 1.0   # Durée plus courte

pygame.mixer.init(frequency=SAMPLE_RATE, size=BITS, channels=CHANNELS)
pygame.init()

# Génération onde avec enveloppe type piano (attaque courte + décroissance)
def make_wave(freq, duration=NOTE_DURATION, sr=SAMPLE_RATE):
    t = np.linspace(0, duration, int(sr * duration), False)
    wave = np.sin(2 * np.pi * freq * t)

    # Enveloppe ADSR simplifiée (attaque rapide + décroissance exponentielle)
    attack = int(0.02 * sr)  # 20ms
    envelope = np.ones_like(wave)
    envelope[:attack] = np.linspace(0, 1, attack)  # montée rapide
    envelope[attack:] = np.exp(-3 * (t[attack:] / duration))  # décroissance

    return (wave * envelope).astype(np.float32)

def to_stereo(wave, volume=MAX_VOLUME):
    wav = wave * (32767 * volume)
    wav = np.clip(wav, -32768, 32767).astype(np.int16)
    if CHANNELS == 2:
        wav = np.column_stack((wav, wav))
    return wav

# --- Mapping clavier -> notes ---
KEY_NOTE_MAP = {
    pygame.K_a: "C4",
    pygame.K_s: "D4",
    pygame.K_d: "E4",
    pygame.K_f: "F4",
    pygame.K_g: "G4",
    pygame.K_h: "A4",
    pygame.K_j: "B4",
    pygame.K_k: "C5",
}

note_sounds = {}
print("Préparation des sons...")
for key, note in KEY_NOTE_MAP.items():
    freq = note_to_frequency[note]
    wave = make_wave(freq, duration=NOTE_DURATION)
    arr = to_stereo(wave)
    sound = pygame.sndarray.make_sound(arr)
    note_sounds[key] = sound

# --- Interface graphique ---
window = pygame.display.set_mode((600, 200))
pygame.display.set_caption("Clavier Piano")
font = pygame.font.SysFont(None, 24)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in note_sounds:
                note_sounds[event.key].play()
            if event.key == pygame.K_ESCAPE:
                running = False

    window.fill((0, 0, 0))
    
    #position y de l'interface
    y = 50
    for k, note in KEY_NOTE_MAP.items():
        txt = f"Touche {pygame.key.name(k)} -> {note}"
        img = font.render(txt, True, (255, 255, 255))
        window.blit(img, (20, y))
        y += 30
    pygame.display.flip()

pygame.quit()

