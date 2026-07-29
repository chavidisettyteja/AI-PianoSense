from piano.piano_key import PianoKey


class KeyboardLayout:

    @staticmethod
    def create_keyboard(frame_width):

        keys = []

        # -----------------------------
        # Layout Settings
        # -----------------------------
        margin = 20
        start_y = 20

        total_white_keys = 21  # 3 octaves × 7 white keys

        white_width = (frame_width - margin * 2) // total_white_keys
        white_height = 170

        black_width = int(white_width * 0.6)
        black_height = 110

        # White notes in one octave
        white_notes = [
            "C", "D", "E", "F", "G", "A", "B"
        ]

        # Black notes and their positions
        black_notes = [
            ("Db", 0),
            ("Eb", 1),
            ("Gb", 3),
            ("Ab", 4),
            ("Bb", 5)
        ]

        octaves = [3, 4, 5]

        current_white = 0

        # =============================
        # WHITE KEYS
        # =============================
        for octave in octaves:

            for note in white_notes:

                x = margin + current_white * white_width

                keys.append(
                    PianoKey(
                        f"{note}{octave}",
                        x,
                        start_y,
                        white_width,
                        white_height,
                        False
                    )
                )

                current_white += 1

        # =============================
        # BLACK KEYS
        # =============================
        current_white = 0

        for octave in octaves:

            octave_start = current_white

            for note, index in black_notes:

                x = (
                    margin
                    + (octave_start + index) * white_width
                    + white_width
                    - black_width // 2
                )

                keys.append(
                    PianoKey(
                        f"{note}{octave}",
                        x,
                        start_y,
                        black_width,
                        black_height,
                        True
                    )
                )

            current_white += 7

        return keys