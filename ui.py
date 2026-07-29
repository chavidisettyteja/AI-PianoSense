import streamlit as st


# ============================================================
# HEADER
# ============================================================

def draw_header():

    st.markdown("""
    <style>

    .main-header{
        background:linear-gradient(90deg,#0f172a,#1e3a8a);
        padding:25px;
        border-radius:15px;
        text-align:center;
        margin-bottom:20px;
        box-shadow:0 0 20px rgba(0,0,0,.3);
    }

    .main-header h1{
        color:white;
        margin:0;
        font-size:40px;
    }

    .main-header p{
        color:#d1d5db;
        font-size:17px;
        margin-top:8px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-header">

    <h1>🎹 AI PianoSense</h1>

    <p>
    Real-Time AI Virtual Piano using
    MediaPipe • OpenCV • Streamlit
    </p>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

def draw_sidebar():

    with st.sidebar:

        st.title("🎛 AI PianoSense")

        st.markdown("---")

        st.markdown("### Features")

        st.success("✔ Two-Hand Tracking")
        st.success("✔ Chord Detection")
        st.success("✔ Real-time Piano")
        st.success("✔ Multi-Octave")
        st.success("✔ Live FPS")

        st.markdown("---")

        st.markdown("### Tips")

        st.info(
            """
• Keep your hands inside the camera frame.

• Use your fingertips to press keys.

• Multiple fingers create chords.

• Ensure good lighting for better tracking.
"""
        )

        st.markdown("---")

        st.caption("Version 2.0")


# ============================================================
# STATUS PANEL
# ============================================================

def draw_status(hands, notes, chord, fps):

    st.markdown("## 📊 Live Status")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🤚 Hands", hands)

    with col2:
        st.metric("⚡ FPS", fps)

    st.markdown("### 🎵 Active Notes")

    if notes:
        st.success(", ".join(sorted(notes)))
    else:
        st.info("No notes pressed")

    st.markdown("### 🎼 Chord")

    if chord:
        st.success(chord)
    else:
        st.info("No chord detected")

    st.markdown("---")

    if hands > 0:
        st.success("🟢 Camera Tracking Active")
    else:
        st.warning("🟡 Waiting for hands...")


# ============================================================
# FOOTER
# ============================================================

def draw_footer():

    st.markdown("---")

    st.markdown(
        """
<div style="text-align:center;color:gray">

### 🎹 AI PianoSense

Built with ❤️ using

**Streamlit • MediaPipe • OpenCV • Pygame**

<br>

Developed by **Teja**

© 2026 AI PianoSense

</div>
""",
        unsafe_allow_html=True
    )