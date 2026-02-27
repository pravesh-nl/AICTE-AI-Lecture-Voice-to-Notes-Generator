import streamlit as st
from google import genai
import json
import os
from datetime import datetime
import yt_dlp
import tempfile
import base64

# ==========================================
# 🔑 PUT YOUR GEMINI API KEY HERE
# ==========================================
GEMINI_API_KEY = "AIzaSyDKw5_bOL41cnxs4NHa1i10wggeMexWnXg"

client = genai.Client(api_key=GEMINI_API_KEY)

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Lecture Voice-to-Notes AI",
    page_icon="🎙",
    layout="wide"
)

# ==========================================
# SIMPLE PROFESSIONAL UI
# ==========================================
st.markdown("""
<style>

/* ============================= */
/* NAVY BACKGROUND */
/* ============================= */
.stApp {
    background-color: #0b1f3a;
}

/* ============================= */
/* ALL NORMAL TEXT WHITE */
/* ============================= */
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li,
div[data-testid="stMarkdownContainer"] span,
label {
    color: white !important;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

/* ============================= */
/* INLINE CODE ( .py , git push ) */
/* ============================= */
code {
    background-color: #132a4d !important;
    color: #ffcc00 !important;   /* Yellow code text */
    padding: 4px 6px;
    border-radius: 6px;
}

/* ============================= */
/* SUCCESS ALERT NORMAL */
/* ============================= */
div[data-testid="stAlert"] {
    color: inherit !important;
}

/* ============================= */
/* FILE UPLOADER */
/* ============================= */
section[data-testid="stFileUploader"] {
    background-color: #132a4d !important;
    border: 2px dashed #1f3c88 !important;
    border-radius: 12px;
    padding: 20px;
}

/* 🔴 Drag & Drop + Limit text */
section[data-testid="stFileUploader"] span {
    color: red !important;
}

/* 🟡 Browse Button */
section[data-testid="stFileUploader"] button {
    background-color: #ffcc00 !important;
    color: black !important;
    border-radius: 8px;
    font-weight: 600;
    border: none;
}

/* ============================= */
/* SELECTBOX */
/* ============================= */

/* Closed select */
div[data-baseweb="select"] > div {
    background-color: #132a4d !important;
    color: red !important;
}

/* Dropdown options */
ul[role="listbox"] li {
    background-color: #132a4d !important;
    color: red !important;
}

/* ============================= */
/* INPUT FIELDS */
/* ============================= */
input, textarea {
    background-color: #132a4d !important;
    color: white !important;
}

/* ============================= */
/* MAIN BUTTON */
/* ============================= */
.stButton>button {
    background-color: #ffcc00;
    color: black !important;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-weight: 600;
    border: none;
}

.stButton>button:hover {
    background-color: #ffd84d;
    color: black !important;
}

</style>
""", unsafe_allow_html=True)
# ==========================================
# HISTORY SETUP
# ==========================================
HISTORY_FILE = "history.json"

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def save_history(entry):
    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)
    data.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_history():
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def delete_entry(index):
    data = load_history()
    data.pop(index)
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ==========================================
# YOUTUBE AUDIO DOWNLOAD
# ==========================================
def download_youtube_audio(url):
    try:
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, "audio.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        return file_path
    except Exception as e:
        print("Download Error:", e)
        return None

# ==========================================
# MAIN TABS
# ==========================================
tab1, tab2, tab3 = st.tabs(
    ["🎙 Generate Notes", "📂 Previous Works", "🧠 About"]
)

# ==========================================
# TAB 1 — GENERATE NOTES
# ==========================================
with tab1:

    st.title("🎙 Lecture Voice-to-Notes Generator")
    st.divider()

    

    st.subheader("Upload Audio File")
    audio_file = st.file_uploader("Upload .mp3, .wav, .m4a", type=["mp3", "wav", "m4a"])

    st.markdown('<div class="or-divider">OR</div>', unsafe_allow_html=True)

    st.subheader("Enter YouTube Link")
    youtube_link = st.text_input("Paste YouTube URL")

    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    mcq_count = st.slider("Number of MCQs", 3, 15, 5)
    difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

    generate_btn = st.button("🚀 Generate Study Content")

    if generate_btn:

        if not audio_file and not youtube_link:
            st.warning("Please upload audio or provide YouTube link.")
            st.stop()

        with st.spinner("Processing..."):

            transcript_text = ""
            audio_bytes = None
            mime_type = None

            # AUDIO UPLOAD
            if audio_file:
                audio_bytes = audio_file.read()
                mime_type = audio_file.type

            # YOUTUBE LINK
            elif youtube_link:
                file_path = download_youtube_audio(youtube_link)

                if not file_path:
                    st.error("❌ Failed to download YouTube audio.")
                    st.stop()

                with open(file_path, "rb") as f:
                    audio_bytes = f.read()

                mime_type = "audio/mp4"

            # ======================================
            # TRANSCRIPTION USING GEMINI 2.5 FLASH
            # ======================================
            try:
                encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        {
                            "role": "user",
                            "parts": [
                                {"text": "Transcribe this lecture audio clearly."},
                                {
                                    "inline_data": {
                                        "mime_type": mime_type,
                                        "data": encoded_audio
                                    }
                                }
                            ]
                        }
                    ]
                )

                if not response or not response.text:
                    st.error("Transcription failed: Empty response.")
                    st.stop()

                transcript_text = response.text

            except Exception as e:
                st.error(f"Transcription failed: {e}")
                st.stop()

            # ======================================
            # STUDY CONTENT GENERATION
            # ======================================
            try:
                result = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"""
                    Based on this lecture transcript:

                    {transcript_text}

                    Provide clearly separated sections:

                    1. Short Summary
                    2. Detailed Study Notes
                    3. {mcq_count} {difficulty} MCQs with answers
                    4. Flashcards (Q&A format)
                    5. Key Concepts List
                    """
                )

                if not result or not result.text:
                    st.error("Study generation failed: Empty response.")
                    st.stop()

            except Exception as e:
                st.error(f"Study generation failed: {e}")
                st.stop()

            st.success("✅ Study Material Generated Successfully!")

            t1, t2 = st.tabs(["📜 Transcript", "📘 Study Content"])

            with t1:
                st.write(transcript_text)

            with t2:
                st.write(result.text)

            save_history({
                "title": transcript_text[:50],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "content": result.text
            })

# ==========================================
# TAB 2 — HISTORY
# ==========================================
with tab2:

    st.title("📂 Previous Generated Works")
    st.divider()

    history = load_history()

    if history:
        for i, item in enumerate(reversed(history)):
            with st.expander(f"{item['title']} ({item['timestamp']})"):
                st.write(item["content"])
                if st.button("Delete", key=i):
                    delete_entry(len(history) - 1 - i)
                    st.rerun()
    else:
        st.info("No previous works yet.")

# ==========================================
# TAB 3 — ABOUT
# ==========================================
with tab3:

    st.title("🧠 About This Project")
    st.divider()

    st.markdown("""
    AI-powered Lecture Voice-to-Notes Generator.

    Features:
    • Audio Transcription  
    • YouTube Audio Download  
    • Summary  
    • Detailed Notes  
    • MCQs  
    • Flashcards  
    • Persistent History  

    Built using:
    • Python  
    • Streamlit  
    • Google Gemini 2.5  
    • yt-dlp  
    """)