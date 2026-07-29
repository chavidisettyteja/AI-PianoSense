import time
import cv2
import av
import streamlit as st

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
    draw_status,
    draw_footer
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI PianoSense",
    page_icon="🎹",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main{
    background:#0e1117;
}

.block-container{
    padding-top:1rem;
}

.metric-container{
    background:#161b22;
    border-radius:15px;
    padding:15px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {

    "notes": set(),
    "hands": 0,
    "fps": 0,
    "chord": "",

    "instrument": "Piano",

    "octave": 4,

    "volume": 100,

    "sustain": False,

    "frame_count": 0,

    "last_time": time.time(),

    "record": False

}

for k, v in defaults.items():

    if k not in st.session_state:

        st.session_state[k] = v


# ============================================================
# HEADER
# ============================================================

draw_header()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🎛 Controls")

    st.markdown("---")

    instrument = st.selectbox(

        "Instrument",

        [

            "Piano",

            "Organ",

            "Electric Piano",

            "Synth",

            "Strings"

        ],

        index=0

    )

    octave = st.slider(

        "Starting Octave",

        3,

        5,

        4

    )

    volume = st.slider(

        "Volume",

        0,

        100,

        100

    )

    sustain = st.toggle(

        "Sustain Mode",

        False

    )

    show_fps = st.toggle(

        "Show FPS",

        True

    )

    show_keyboard = st.toggle(

        "Show Keyboard",

        True

    )

    mirror = st.toggle(

        "Mirror Camera",

        True

    )

    st.markdown("---")

    st.info(
        """
        🎹 AI PianoSense

        ✔ Two-Hand Tracking

        ✔ Chord Detection

        ✔ Multi-Octave Support

        ✔ Real-time Audio
        """
    )

st.session_state.instrument = instrument
st.session_state.octave = octave
st.session_state.volume = volume
st.session_state.sustain = sustain


# ============================================================
# CACHE RESOURCES
# ============================================================

@st.cache_resource
def load_components():

    detector = HandDetector()

    piano = Piano()

    audio = AudioEngine()

    chord_detector = ChordDetector()

    return detector, piano, audio, chord_detector


with st.spinner("Loading AI PianoSense..."):

    detector, piano, audio, chord_detector = load_components()


# ============================================================
# WEBRTC CONFIG
# ============================================================

RTC_CONFIGURATION = RTCConfiguration({

    "iceServers":[

        {

            "urls":[

                "stun:stun.l.google.com:19302"

            ]

        }

    ]

})
# ============================================================
# VIDEO PROCESSOR
# ============================================================

class PianoProcessor(VideoProcessorBase):

    def __init__(self):

        self.last_frame_time = time.perf_counter()

        self.frame_counter = 0

        self.fps = 0

    def recv(self, frame):

        try:

            image = frame.to_ndarray(format="bgr24")

            # Mirror camera if enabled
            if mirror:
                image = cv2.flip(image, 1)

            height, width = image.shape[:2]

            # Create keyboard according to frame width
            piano.create(width)

            # Detect hands
            image = detector.detect_hands(image)

            # Fingertips dictionary
            fingertips = detector.get_fingertips(image)

            # Piano Logic
            new_notes, current_notes = piano.update(fingertips)

            # ----------------------------
            # Audio
            # ----------------------------

            # Set mixer volume (0.0 - 1.0)
            try:
                for sound in audio.sounds.values():
                    sound.set_volume(
                        st.session_state.volume / 100
                    )
            except Exception:
                pass

            # Play only newly pressed notes
            for note in new_notes:
                audio.play(   note,
                    st.session_state.volume / 100
                )

            # ----------------------------
            # Chord Detection
            # ----------------------------

            chord = chord_detector.detect(current_notes)

            # ----------------------------
            # Draw Keyboard
            # ----------------------------

            if show_keyboard:
                piano.draw(image)

            # ----------------------------
            # Number of Hands
            # ----------------------------

            if (
                hasattr(detector, "results")
                and detector.results
                and detector.results.multi_hand_landmarks
            ):
                st.session_state.hands = len(
                    detector.results.multi_hand_landmarks
                )
            else:
                st.session_state.hands = 0

            # ----------------------------
            # Store Session Values
            # ----------------------------

            st.session_state.notes = current_notes
            st.session_state.chord = chord

            # ----------------------------
            # FPS
            # ----------------------------

            self.frame_counter += 1

            current = time.perf_counter()

            elapsed = current - self.last_frame_time

            if elapsed >= 1:

                self.fps = self.frame_counter / elapsed

                st.session_state.fps = round(
                    self.fps,
                    1
                )

                self.frame_counter = 0

                self.last_frame_time = current

            # Draw FPS
            if show_fps:

                cv2.putText(

                    image,

                    f"FPS : {st.session_state.fps}",

                    (20, 35),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.8,

                    (0, 255, 0),

                    2

                )

            # Draw active notes
            cv2.putText(

                image,

                "Notes : " +
                (
                    ", ".join(sorted(current_notes))
                    if current_notes
                    else "-"
                ),

                (20, 70),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.65,

                (255, 255, 255),

                2

            )

            # Draw chord
            cv2.putText(

                image,

                f"Chord : {chord if chord else '-'}",

                (20, 105),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.65,

                (0, 255, 255),

                2

            )

            # Draw hand count
            cv2.putText(

                image,

                f"Hands : {st.session_state.hands}",

                (20, 140),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.65,

                (255, 200, 0),

                2

            )

            return av.VideoFrame.from_ndarray(
                image,
                format="bgr24"
            )

        except Exception as e:

            error = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            )

            cv2.putText(

                error,

                str(e),

                (20, 50),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.7,

                (255, 0, 0),

                2

            )

            return av.VideoFrame.from_ndarray(
                error,
                format="rgb24"
            )
        # ============================================================
# MAIN LAYOUT
# ============================================================

st.markdown("---")

left, right = st.columns([3.5, 1.2])

# ------------------------------------------------------------
# Webcam
# ------------------------------------------------------------

with left:

    st.subheader("🎥 Live AI Piano")

    webrtc_streamer(

        key="ai-pianosense",

        rtc_configuration=RTC_CONFIGURATION,

        video_processor_factory=PianoProcessor,

        media_stream_constraints={
            "video": {
                "width": {"ideal": 1280},
                "height": {"ideal": 720},
                "frameRate": {"ideal": 30}
            },
            "audio": False
        },

        async_processing=True,

    )

# ------------------------------------------------------------
# Status Panel
# ------------------------------------------------------------

with right:

    st.subheader("🎼 Performance")

    st.metric(
        "Hands",
        st.session_state.hands
    )

    st.metric(
        "FPS",
        st.session_state.fps
    )

    st.metric(
        "Instrument",
        st.session_state.instrument
    )

    st.metric(
        "Octave",
        st.session_state.octave
    )

    st.metric(
        "Volume",
        f"{st.session_state.volume}%"
    )

    st.metric(
        "Sustain",
        "ON" if st.session_state.sustain else "OFF"
    )

    st.markdown("---")

    st.subheader("🎵 Current Notes")

    if st.session_state.notes:

        for note in sorted(st.session_state.notes):
            st.success(note)

    else:

        st.info("No notes pressed")

    st.markdown("---")

    st.subheader("🎶 Detected Chord")

    if st.session_state.chord:

        st.success(st.session_state.chord)

    else:

        st.info("No chord detected")

    st.markdown("---")

    draw_status(
        st.session_state.hands,
        st.session_state.notes,
        st.session_state.chord,
        st.session_state.fps
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

draw_footer()

# ============================================================
# INFORMATION
# ============================================================

with st.expander("ℹ About AI PianoSense"):

    st.markdown(
        """
### Features

- 🎹 Virtual Piano
- 🤚 Two-Hand MediaPipe Tracking
- 🎵 Real-time Audio Playback
- 🎼 Chord Detection
- 📈 Live FPS Counter
- 🎚 Volume Control
- 🎹 Multi-Octave Support
- ☁ Streamlit Cloud Compatible

**Built with**
- Streamlit
- OpenCV
- MediaPipe
- streamlit-webrtc
- pygame
        """
    )

# ============================================================
# DEBUG PANEL
# ============================================================

with st.expander("🐞 Debug"):

    st.write("Hands:", st.session_state.hands)
    st.write("Notes:", sorted(st.session_state.notes))
    st.write("Chord:", st.session_state.chord)
    st.write("FPS:", st.session_state.fps)
    st.write("Instrument:", st.session_state.instrument)
    st.write("Octave:", st.session_state.octave)
    st.write("Volume:", st.session_state.volume)
    st.write("Sustain:", st.session_state.sustain)