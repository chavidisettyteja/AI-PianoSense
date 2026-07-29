import streamlit as st


# ----------------------------------------
# Header
# ----------------------------------------

def draw_header():

    st.markdown(
        """
        <div style="
            background:#111827;
            padding:18px;
            border-radius:12px;
            margin-bottom:15px;
            text-align:center;
        ">
            <h1 style="color:white;margin:0;">
                🎹 AI PianoSense
            </h1>

            <p style="color:#9CA3AF;">
                Real-Time Hand Tracking Piano using MediaPipe
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ----------------------------------------
# Sidebar
# ----------------------------------------

def draw_sidebar():

    with st.sidebar:

        st.title("🎹 AI PianoSense")

        st.markdown("---")

        st.subheader("Controls")

        st.write("✔ Webcam")

        st.write("✔ Hand Tracking")

        st.write("✔ Piano")

        st.write("✔ Chord Detection")

        st.markdown("---")

        st.subheader("Settings")

        show_landmarks = st.checkbox(
            "Show Hand Landmarks",
            value=True
        )

        dark_mode = st.checkbox(
            "Dark Theme",
            value=True
        )

        st.markdown("---")

        st.caption("Version 1.0")


# ----------------------------------------
# Status Panel
# ----------------------------------------

def draw_status(hands, notes, chord, fps):

    st.markdown("## 📊 Status")

    st.metric(
        label="Hands",
        value=hands
    )

    if len(notes) == 0:

        note_text = "--"

    else:

        note_text = ", ".join(sorted(notes))

    st.metric(
        label="Notes",
        value=note_text
    )

    if chord == "":

        chord = "--"

    st.metric(
        label="Chord",
        value=chord
    )

    st.metric(
        label="FPS",
        value=fps
    )

    st.markdown("---")

    st.success("Application Running")


# ----------------------------------------
# Footer
# ----------------------------------------

def draw_footer():

    st.markdown(
        """
        <hr>

        <center>

        Developed by <b>Teja</b>

        <br>

        AI PianoSense © 2026

        </center>
        """,
        unsafe_allow_html=True
    )