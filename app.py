import cv2
import time

from hand_tracking.hand_detector import HandDetector
from piano.piano import Piano
from audio.audio_engine import AudioEngine
from chords.chord_detector import ChordDetector
from ui.dashboard import Dashboard


def main():

    # -----------------------------
    # Camera
    # -----------------------------
    cap = cv2.VideoCapture(0)

    cv2.namedWindow("AI PianoSense", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("AI PianoSense", 1400, 900)

    # -----------------------------
    # Components
    # -----------------------------
    detector = HandDetector()
    piano = Piano()
    audio = AudioEngine()
    chord_detector = ChordDetector()
    dashboard = Dashboard()

    previous_time = time.time()

    while True:

        success, frame = cap.read()

        if not success:
            break

        # Mirror camera
        frame = cv2.flip(frame, 1)

        # Resize keyboard according to frame width
        height, width = frame.shape[:2]
        piano.create(width)

        # -----------------------------
        # Hand Detection
        # -----------------------------
        frame = detector.detect_hands(frame)
        fingertips = detector.get_fingertips(frame)

        # -----------------------------
        # FPS
        # -----------------------------
        current_time = time.time()

        fps = int(
            1 / max(current_time - previous_time, 0.001)
        )

        previous_time = current_time

        # -----------------------------
        # Draw Fingertips
        # -----------------------------
        for finger_name, (x, y) in fingertips.items():

            cv2.circle(
                frame,
                (x, y),
                8,
                (0, 0, 255),
                -1
            )

            cv2.putText(
                frame,
                finger_name,
                (x + 8, y - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (255, 255, 255),
                1
            )

        # -----------------------------
        # Piano Logic
        # -----------------------------
        new_notes, current_notes = piano.update(fingertips)

        # Play only newly pressed notes
        for note in new_notes:
            audio.play(note)

        # Detect Chord
        chord = chord_detector.detect(current_notes)

        # Draw Piano
        piano.draw(frame)

        # -----------------------------
        # Dashboard
        # -----------------------------
        canvas = dashboard.create()

        canvas = dashboard.draw_camera(
            canvas,
            frame
        )

        hand_count = 0

        if detector.results.multi_hand_landmarks:
            hand_count = len(
                detector.results.multi_hand_landmarks
            )

        canvas = dashboard.draw_status(
            canvas,
            current_notes,
            chord,
            hand_count,
            fps
        )

        # -----------------------------
        # Display
        # -----------------------------
        cv2.imshow(
            "AI PianoSense",
            canvas
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()