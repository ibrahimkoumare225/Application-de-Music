import numpy as np
import pygame
from MusicPlayer_base_original import MusicPlayer
from note_frequence_base import note_to_frequency


class Instrument:
    """Classe de base pour tous les instruments"""

    def __init__(self, player: MusicPlayer, nom: str):
        self.nom = nom
        self.player = player

    def _note_to_freq(self, note: str):
        if not note:
            return 440
        if note in note_to_frequency:
            return note_to_frequency[note]
        note_up = note.upper()
        if note_up in note_to_frequency:
            return note_to_frequency[note_up]
        return 440

    def jouer(self, note: str, duration: float = 0.5):
        freq = self._note_to_freq(note)
        self.player.play(freq, duration)


# --------------------- Instruments spécifiques ---------------------
class Flute(Instrument):
    def __init__(self, player):
        super().__init__(player, "Flûte")

    def jouer(self, note: str, duration: float = 0.5):
        freq = self._note_to_freq(note)
        t = np.linspace(0, duration, int(self.player.sample_rate * duration), False)
        vibrato = 1.0 + 0.003 * np.sin(2 * np.pi * 5 * t)
        tone = np.sin(2 * np.pi * freq * t * vibrato)
        self.player._play_tone(tone, duration)


class Guitare(Instrument):
    def __init__(self, player):
        super().__init__(player, "Guitare")

    def jouer(self, note: str, duration: float = 0.5):
        freq = self._note_to_freq(note)
        t = np.linspace(0, duration, int(self.player.sample_rate * duration), False)
        tone = (0.6 * np.sin(2 * np.pi * freq * t) +
                0.3 * np.sin(2 * np.pi * 2 * freq * t) +
                0.1 * np.sin(2 * np.pi * 3 * freq * t))
        env = np.minimum(1, 5 * t) * np.exp(-3 * t)
        tone = tone * env
        self.player._play_tone(tone, duration)


class Piano(Instrument):
    ...
    def interface_piano(self):
        """Interface graphique du piano"""
        pygame.init()
        window_width = 14 * 60
        window_height = 300
        window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Clavier Piano")
        font = pygame.font.SysFont(None, 24)
        running = True

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        BLUE = (50, 150, 255)

        white_keys_list = [
            pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j,
            pygame.K_k, pygame.K_l, pygame.K_SEMICOLON, pygame.K_QUOTE, pygame.K_z, pygame.K_x, pygame.K_c
        ]
        black_keys_list = [
            pygame.K_w, pygame.K_e, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_o, pygame.K_p,
            pygame.K_1, pygame.K_2, pygame.K_3
        ]
        pressed_keys = set()
        black_positions = [0, 1, 3, 4, 5, 7, 8, 10, 11, 12, 14, 15, 16]

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.note_sounds:
                        self.note_sounds[event.key].play()
                        pressed_keys.add(event.key)
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.KEYUP:
                    pressed_keys.discard(event.key)

            window.fill((30, 30, 30))
            # touches blanches
            for i, key in enumerate(white_keys_list):
                color = RED if key in pressed_keys else WHITE
                pygame.draw.rect(window, color, (i*60,0,60,250))
                pygame.draw.rect(window, BLACK, (i*60,0,60,250),2)
            # touches noires
            for i,key in enumerate(black_keys_list):
                x = black_positions[i]*60 + 60 - 35//2
                color = BLUE if key in pressed_keys else BLACK
                pygame.draw.rect(window,color,(x,0,35,150))
            pygame.display.flip()
        pygame.quit()
    
  
class Batterie(Instrument):
    def __init__(self, player):
        super().__init__(player, "Batterie")
        self.NOTE_DURATION = 0.5
        self.SAMPLE_RATE = player.sample_rate
        self.drum_sounds = {}
        pygame.mixer.init(frequency=self.SAMPLE_RATE, size=-16, channels=2)
        pygame.init()
        self._prepare_sounds()

    def _prepare_sounds(self):
        """Génération des sons synthétiques pour la batterie"""
        for drum in ["kick", "snare", "hihat", "crash", "tom1", "tom2", "tom3", "ride"]:
            t = np.linspace(0, self.NOTE_DURATION, int(self.SAMPLE_RATE * self.NOTE_DURATION), False)
            if drum == "kick":
                freq = 60
                wave = np.sin(2 * np.pi * freq * t) * np.exp(-5 * t)
            elif drum == "snare":
                wave = np.random.uniform(-1, 1, len(t)) * np.exp(-12 * t)
            elif drum == "hihat":
                wave = np.random.uniform(-0.3, 0.3, len(t)) * np.exp(-20 * t)
            elif drum == "crash":
                wave = np.random.uniform(-0.5, 0.5, len(t)) * np.exp(-8 * t)
            else:
                freq = 100 + 50 * ["tom1", "tom2", "tom3", "ride"].index(drum)
                wave = np.sin(2 * np.pi * freq * t) * np.exp(-8 * t)
            wav = np.column_stack((wave, wave))
            wav = np.ascontiguousarray((32767 * wav).astype(np.int16))
            self.drum_sounds[drum] = pygame.sndarray.make_sound(wav)

    def jouer(self, note: str = None, duration: float = 0.5):
        """Jouer un son de batterie générique (bruit)"""
        t = np.linspace(0, duration, int(self.SAMPLE_RATE * duration), False)
        noise = np.random.uniform(-1, 1, len(t))
        envelope = np.exp(-8 * t)
        tone = noise * envelope
        self.player._play_tone(tone, duration)

    def interface_drum(self):
        """Interface graphique de la batterie"""
        from Menu import interface_drum
        interface_drum(self)
