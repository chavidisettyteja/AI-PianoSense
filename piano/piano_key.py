import cv2


class PianoKey:

    def __init__(self, note, x, y, width, height, is_black=False):

        self.note = note

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.is_black = is_black

        self.is_pressed = False

    def draw(self, frame):

        if self.is_black:

            color = (30, 30, 30)

            if self.is_pressed:
                color = (0, 0, 255)

        else:

            color = (255, 255, 255)

            if self.is_pressed:
                color = (0, 255, 0)

        # Fill key
        cv2.rectangle(
            frame,
            (self.x, self.y),
            (self.x + self.width, self.y + self.height),
            color,
            -1
        )

        # Border
        cv2.rectangle(
            frame,
            (self.x, self.y),
            (self.x + self.width, self.y + self.height),
            (0, 0, 0),
            2
        )

        # Note label
        text_color = (255, 255, 255) if self.is_black else (0, 0, 0)

        cv2.putText(
            frame,
            self.note,
            (self.x + 5, self.y + self.height - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            text_color,
            1
        )

    def contains(self, px, py):

        return (
            self.x <= px <= self.x + self.width
            and
            self.y <= py <= self.y + self.height
        )