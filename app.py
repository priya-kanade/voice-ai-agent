import streamlit as st
import tempfile
import os
from modules.stt import transcribe_audio
from modules.agent import run_agent
from pydub import AudioSegment
from audiorecorder import audiorecorder

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Voice AI Agent", layout="centered")

# ---------------- SIMPLE CLEAN UI FIX ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #ffffff;
    color: #111827;
}

/* Fix text visibility */
body, p, label, span {
    color: #111827 !important;
}

/* Fix radio visibility */
div[role="radiogroup"] label {
    color: #111827 !important;
    font-weight: 600;
}

/* Fix uploader */
section[data-testid="stFileUploader"] {
    background-color: #f3f4f6 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 10px !important;
    padding: 12px !important;
}

/* Buttons */
button {
    background-color: #4f46e5 !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
}

/* Headings */
h1 {
    text-align: center;
    color: #111827 !important;
}

h2, h3 {
    color: #1f2937 !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1>🎤 Voice AI Agent</h1>", unsafe_allow_html=True)

# ---------------- MEMORY ----------------
if "history" not in st.session_state:
    st.session_state.history = []

audio_path = None

# Detect Hugging Face
def is_hf():
    return os.getenv("SPACE_ID") is not None

# ---------------- INPUT MODE ----------------
if not is_hf():
    mode = st.radio(
        "Input Mode",
        ["Upload Audio", "Record Mic"],
        label_visibility="collapsed"
    )
else:
    mode = "Upload Audio"

# ---------------- FILE UPLOAD ----------------
if mode == "Upload Audio":
    st.subheader("Upload Audio")

    file = st.file_uploader(
        "Upload Audio File",
        type=["wav", "mp3", "aac"],
        label_visibility="collapsed"
    )

    if file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            if file.type == "audio/aac" or file.name.endswith(".aac"):
                audio = AudioSegment.from_file(file, format="aac")
                audio.export(tmp.name, format="wav")
                audio_path = tmp.name
            else:
                tmp.write(file.read())
                audio_path = tmp.name

# ---------------- MIC RECORDING ----------------
elif mode == "Record Mic":
    st.subheader("🎤 Record Voice")

    audio = audiorecorder("Start Recording", "Stop Recording")

    if len(audio) > 0:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio.export(tmp.name, format="wav")
            audio_path = tmp.name

        st.audio(audio_path)

# ---------------- PROCESS ----------------
if audio_path:
    st.info("Processing audio...")

    try:
        with st.spinner("Transcribing..."):
            text = transcribe_audio(audio_path)

        st.success(f"Transcription: {text}")

        # Graceful handling
        if not text or len(text.strip()) < 3:
            st.error("Could not understand audio. Please try again.")
            st.stop()

        temp_intent, temp_result = run_agent(text)

        # Human-in-the-loop
        if temp_intent in ["create_file", "write_code"]:
            st.warning(f"Action detected: {temp_intent}")

            confirm = st.radio(
                "Confirm Action",
                ["No", "Yes"],
                label_visibility="collapsed"
            )

            if confirm == "Yes":
                intent, result = temp_intent, temp_result
            else:
                intent = "cancelled"
                result = {
                    "message": "Action cancelled",
                    "file_path": None,
                    "content": ""
                }
        else:
            intent, result = temp_intent, temp_result

        # ---------------- OUTPUT ----------------
        st.subheader("Result")

        st.write("**Transcription:**", text)
        st.write("**Intent:**", intent)
        st.write("**Action:**", result.get("message", ""))

        if result.get("file_path"):
            st.write("**File Location:**")
            st.code(result["file_path"])

        if result.get("content"):
            st.write("**Output:**")
            if intent == "write_code":
                st.code(result["content"], language="python")
            else:
                st.write(result["content"])

        # Store history
        st.session_state.history.append({
            "text": text,
            "intent": intent,
            "result": result.get("message", "")
        })

    except Exception as e:
        st.error(f"Error: {str(e)}")

# ---------------- HISTORY ----------------
st.subheader("Conversation History")

for item in st.session_state.history[::-1]:
    st.write("You:", item["text"])
    st.write("Intent:", item["intent"])
    st.write("Result:", item["result"])
    st.write("---")