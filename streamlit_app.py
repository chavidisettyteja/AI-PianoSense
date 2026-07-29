import streamlit as st
import cv2
import av
from streamlit_webrtc import (
    webrtc_streamer,
    VideoProcessorBase,
    RTCConfiguration
)

from hand_tracking.hand_detector import HandDetector
from piano.piano import Piano
from audio.audio_engine import AudioEngine
from chords.chord_detector import ChordDetector

from ui import (
    draw_sidebar,
    draw_header,
    draw_status
)


# ---------------------------------------
# Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="AI PianoSense",
    page_icon="🎹",
    layout="wide"
)


# ---------------------------------------
# Initialize Session State
# ---------------------------------------

if "notes" not in st.session_state:
    st.session_state.notes = set()

if "chord" not in st.session_state:
    st.session_state.chord = ""

if "hands" not in st.session_state:
    st.session_state.hands = 0

if "fps" not in st.session_state:
    st.session_state.fps = 0


# ---------------------------------------
# Sidebar
# ---------------------------------------

draw_sidebar()


# ---------------------------------------
# Header
# ---------------------------------------

draw_header()


# ---------------------------------------
# Load AI Components
# ---------------------------------------

detector = HandDetector()

piano = Piano()

audio = AudioEngine()

chord_detector = ChordDetector()


# ---------------------------------------
# Video Processor
# ---------------------------------------

class PianoProcessor(VideoProcessorBase):

    def recv(self, frame):

        image = frame.to_ndarray(format="bgr24")

        image = cv2.flip(image, 1)

        h, w = image.shape[:2]

        piano.create(w)

        image = detector.detect_hands(image)

        fingertips = detector.get_fingertips(image)

        new_notes, current_notes = piano.update(fingertips)

        for note in new_notes:
            audio.play(note)

        chord = chord_detector.detect(current_notes)

        piano.draw(image)

        if detector.results.multi_hand_landmarks:

            st.session_state.hands = len(
                detector.results.multi_hand_landmarks
            )

        else:

            st.session_state.hands = 0

        st.session_state.notes = current_notes

        st.session_state.chord = chord

        return av.VideoFrame.from_ndarray(
            image,
            format="bgr24"
        )


# ---------------------------------------
# Layout
# ---------------------------------------

left, right = st.columns([3,1])


with left:

    webrtc_streamer(

        key="piano",

        rtc_configuration=RTCConfiguration(
            {
                "iceServers": [
                    {
                        "urls": ["stun:stun.l.google.com:19302"]
                    }
                ]
            }
        ),

        video_processor_factory=PianoProcessor,

        media_stream_constraints={
            "video": True,
            "audio": False
        },

        async_processing=True

    )


with right:

    draw_status(
        st.session_state.hands,
        st.session_state.notes,
        st.session_state.chord,
        st.session_state.fps
    )

from ui import draw_footer

draw_footer()