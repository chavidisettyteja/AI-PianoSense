import cv2
import numpy as np


class Dashboard:

    def __init__(self):

        self.width = 1600
        self.height = 900

        self.bg = (35, 35, 35)
        self.header = (70, 90, 170)

    def create(self):

        canvas = np.full(
            (self.height, self.width, 3),
            self.bg,
            dtype=np.uint8
        )

        # ================= HEADER =================
        cv2.rectangle(
            canvas,
            (0, 0),
            (self.width, 70),
            self.header,
            -1
        )

        cv2.putText(
            canvas,
            "AI PianoSense",
            (30, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (255, 255, 255),
            3
        )

        # ================= LEFT PANEL =================

        cv2.rectangle(
            canvas,
            (20, 90),
            (260, 690),
            (55, 55, 55),
            -1
        )

        cv2.rectangle(
            canvas,
            (20, 90),
            (260, 690),
            (120, 120, 120),
            2
        )

        # ================= CAMERA =================

        cv2.rectangle(
            canvas,
            (280, 90),
            (1580, 690),
            (120, 120, 120),
            2
        )

        # ================= PIANO =================

        cv2.rectangle(
            canvas,
            (20, 720),
            (1580, 890),
            (60, 60, 60),
            2
        )

        return canvas

    def draw_camera(self, canvas, frame):

        camera = cv2.resize(frame, (1260, 560))

        canvas[
            110:670,
            300:1560
        ] = camera

        return canvas

    def draw_status(
        self,
        canvas,
        notes,
        chord,
        hands,
        fps
    ):

        y = 140

        cv2.putText(
            canvas,
            "STATUS",
            (50, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        y += 60

        cv2.putText(
            canvas,
            f"Hands : {hands}",
            (40, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        y += 60

        cv2.putText(
            canvas,
            "Notes",
            (40, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        y += 40

        text = ", ".join(sorted(notes))

        cv2.putText(
            canvas,
            text[:18],
            (40, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        y += 70

        cv2.putText(
            canvas,
            "Chord",
            (40, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 180, 0),
            2
        )

        y += 40

        cv2.putText(
            canvas,
            chord if chord else "-",
            (40, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        y += 80

        cv2.putText(
            canvas,
            f"FPS : {fps}",
            (40, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        return canvas