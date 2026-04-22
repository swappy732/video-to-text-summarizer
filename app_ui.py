import streamlit as st
import tempfile
import whisper
from transformers import pipeline

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Video Summarizer",
    page_icon="🎬",
    layout="wide"
)

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "history" not in st.session_state:
    st.session_state.history = []

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

/* BACKGROUND */
html, body, [class*="css"] {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* CARD */
.main-card {
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(14px);
    border-radius: 16px;
    padding: 30px;
    box-shadow: 0px 8px 32px rgba(0,0,0,0.6);
}

/* HEADINGS */
h1, h2, h3 {
    color: white;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background-color: #111827;
    border: 2px dashed #334155;
    border-radius: 12px;
    padding: 20px;
}

/* BUTTON */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white !important;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
}

/* DOWNLOAD BUTTON */
[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #22c55e, #4ade80);
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------- LOGIN PAGE ----------
def login():
    st.title("🔐 Login to AI Video Summarizer")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------- MAIN APP ----------
def main_app():

    # SIDEBAR
    st.sidebar.title("🚀 Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "History", "About"])

    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # ---------- DASHBOARD ----------
    if page == "Dashboard":

        st.markdown('<div class="main-card">', unsafe_allow_html=True)

        st.title("🎬 AI Video Summarizer")
        st.write("Upload a video and get transcript + summary")

        uploaded_file = st.file_uploader(
            "Upload video",
            type=["mp4", "mov", "avi"]
        )

        if uploaded_file:
            st.success("✅ Uploaded!")

            st.video(uploaded_file)

            # Save temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                tmp.write(uploaded_file.read())
                video_path = tmp.name

            with st.spinner("Processing..."):
                try:
                    model = whisper.load_model("base")
                    result = model.transcribe(video_path)
                    transcript = result["text"]

                    summarizer = pipeline(
                        "summarization",
                        model="facebook/bart-large-cnn"
                    )

                    summary = summarizer(
                        transcript,
                        max_length=130,
                        min_length=30,
                        do_sample=False
                    )[0]['summary_text']

                    # SAVE HISTORY
                    st.session_state.history.append({
                        "name": uploaded_file.name,
                        "transcript": transcript,
                        "summary": summary
                    })

                    # TABS
                    tab1, tab2 = st.tabs(["📄 Transcript", "🧠 Summary"])

                    with tab1:
                        st.write(transcript)

                    with tab2:
                        st.write(summary)

                        st.download_button(
                            "📥 Download Summary",
                            summary,
                            file_name="summary.txt"
                        )

                except Exception as e:
                    st.error(f"Error: {e}")

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------- HISTORY ----------
    elif page == "History":

        st.title("📂 Your History")

        if len(st.session_state.history) == 0:
            st.info("No history yet.")
        else:
            for item in st.session_state.history[::-1]:
                with st.expander(f"📁 {item['name']}"):
                    st.write("Transcript:")
                    st.write(item["transcript"])

                    st.write("Summary:")
                    st.write(item["summary"])

    # ---------- ABOUT ----------
    elif page == "About":
        st.title("ℹ️ About")
        st.write("""
        This AI app:
        - Converts video → text using Whisper
        - Summarizes using NLP (BART)
        - Built with Streamlit
        """)

# ---------- RUN ----------
if not st.session_state.logged_in:
    login()
else:
    main_app()