import os
import pygame


class AudioEngine:

    def __init__(self):

        pygame.mixer.init(
            frequency=44100,
            size=-16,
            channels=2,
            buffer=512
        )

        # Plenty of channels for chords
        pygame.mixer.set_num_channels(64)

        self.sounds = {}
        self.channels = {}

        self.load_sounds()

    def load_sounds(self):

        base_path = os.path.dirname(os.path.abspath(__file__))

        octaves = [3, 4, 5]

        notes = [
            "C", "Db", "D", "Eb", "E", "F",
            "Gb", "G", "Ab", "A", "Bb", "B"
        ]

        channel = 0

        for octave in octaves:

            for note in notes:

                note_name = f"{note}{octave}"

                file_path = os.path.join(
                    base_path,
                    note_name + ".wav"
                )

                if os.path.exists(file_path):

                    self.sounds[note_name] = pygame.mixer.Sound(file_path)
                    self.channels[note_name] = pygame.mixer.Channel(channel)

                    print(f"Loaded {note_name}")

                    channel += 1

                else:

                    print(f"Missing {note_name}")

            def play(self, note, volume=1.0):

                if note not in self.sounds:
                    return

                sound = self.sounds[note]
                sound.set_volume(volume)

                channel = self.channels[note]
                channel.stop()
                channel.play(sound)