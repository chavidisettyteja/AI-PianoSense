import cv2
import mediapipe as mp


class HandDetector:

    def __init__(self):

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.results = None

    def detect_hands(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(rgb)

        if self.results.multi_hand_landmarks:

            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

        return frame

    def get_fingertips(self, frame):

        fingertips = {}

        if not self.results or not self.results.multi_hand_landmarks:
            return fingertips

        h, w, _ = frame.shape

        tip_ids = {
            "Thumb": 4,
            "Index": 8,
            "Middle": 12,
            "Ring": 16,
            "Pinky": 20
        }

        for hand_index, hand_landmarks in enumerate(self.results.multi_hand_landmarks):

            hand_name = f"H{hand_index+1}"

            for finger_name, tip_id in tip_ids.items():

                landmark = hand_landmarks.landmark[tip_id]

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                fingertips[f"{hand_name}_{finger_name}"] = (x, y)

        return fingertips