from piano.keyboard_layout import KeyboardLayout


class Piano:

    def __init__(self):

        self.keys = []

        self.current_width = 0

        # Keeps track of currently pressed notes
        self.previous_notes = set()

    # ------------------------------------
    # Create keyboard dynamically
    # ------------------------------------
    def create(self, frame_width):

        if frame_width != self.current_width:

            self.current_width = frame_width

            self.keys = KeyboardLayout.create_keyboard(frame_width)

    # ------------------------------------
    # Draw piano
    # ------------------------------------
    def draw(self, frame):

        # White keys first
        for key in self.keys:

            if not key.is_black:
                key.draw(frame)

        # Black keys on top
        for key in self.keys:

            if key.is_black:
                key.draw(frame)

    # ------------------------------------
    # Update pressed notes
    # ------------------------------------
    def update(self, fingertips):

        # Reset key states
        for key in self.keys:

            key.is_pressed = False

        current_notes = set()

        # Black keys get priority
        sorted_keys = sorted(
            self.keys,
            key=lambda k: k.is_black,
            reverse=True
        )

        # Check every fingertip
        for _, (x, y) in fingertips.items():

            for key in sorted_keys:

                if key.contains(x, y):

                    key.is_pressed = True

                    current_notes.add(key.note)

                    break

        # Newly pressed notes only
        new_notes = current_notes - self.previous_notes

        # Store current notes
        self.previous_notes = current_notes.copy()

        return new_notes, current_notes