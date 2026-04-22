import streamlit as st
import tempfile
import hashlib
import whisper
from transformers import pipeline
import firebase_admin
from firebase_admin import credentials, firestore, auth

# ---------------- FIREBASE INIT ----------------
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Video Summarizer", page_icon="🎬", layout="wide")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "last_file" not in st.session_state:
    st.session_state.last_file = None

# ---------------- CSS ----------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}
section[data-testid="stSidebar"] {
    background: #020617;
}
.main-card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 15px;
}
.stButton>button {
    background: #6366f1;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- CACHE ----------------
@st.cache_resource
def load_whisper():
    return whisper.load_model("tiny")

@st.cache_resource
def load_summarizer():
    return pipeline("summarization")

@st.cache_data
def transcribe(path):
    model = load_whisper()
    return model.transcribe(path)["text"]

@st.cache_data
def summarize(text):
    summarizer = load_summarizer()
    return summarizer(text[:1000], max_length=150, min_length=40, do_sample=False)[0]["summary_text"]

# ---------------- AUTH ----------------
def login():
    st.title("🔐 Login / Signup")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    # LOGIN
    with col1:
        if st.button("Login"):
            try:
                user = auth.get_user_by_email(email)
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success("Logged in!")
                st.rerun()
            except:
                st.error("User not found")

    # SIGNUP
    with col2:
        if st.button("Sign Up"):
            try:
                auth.create_user(email=email, password=password)
                st.success("Account created! Now login.")
            except Exception as e:
                st.error(str(e))

# ---------------- APP ----------------
def app():

    st.sidebar.title("🚀 Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "History", "About"])

    st.sidebar.write(f"👤 {st.session_state.user_email}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.rerun()

    # -------- DASHBOARD --------
    if page == "Dashboard":

        st.markdown('<div class="main-card">', unsafe_allow_html=True)

        st.title("🎬 AI Video Summarizer")

        uploaded_file = st.file_uploader("Upload video", type=["mp4", "mov", "avi"])

        if uploaded_file:

            # SAFE READ
            file_bytes = uploaded_file.read()

            if not file_bytes:
                st.error("Invalid file")
                st.stop()

            file_hash = hashlib.md5(file_bytes).hexdigest()

            # SAVE TEMP FILE
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                tmp.write(file_bytes)
                temp_path = tmp.name

            # PROCESS
            if st.session_state.last_file != file_hash:

                with st.spinner("Processing... ⏳"):
                    text = transcribe(temp_path)
                    summary = summarize(text)

                    st.session_state.last_file = file_hash
                    st.session_state.text = text
                    st.session_state.summary = summary

                    # SAVE TO FIRESTORE
                    db.collection("users")\
                      .document(st.session_state.user_email)\
                      .collection("history")\
                      .add({
                          "summary": summary
                      })

            else:
                text = st.session_state.text
                summary = st.session_state.summary

            st.success("Done ✅")

            st.subheader("📄 Transcript")
            st.write(text)

            st.subheader("🧠 Summary")
            st.write(summary)

            # DOWNLOAD
            st.download_button(
                "⬇ Download Summary",
                summary,
                file_name="summary.txt"
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # -------- HISTORY --------
    elif page == "History":

        st.title("📜 Your History")

        docs = db.collection("users")\
                 .document(st.session_state.user_email)\
                 .collection("history")\
                 .stream()

        found = False
        for i, doc in enumerate(docs):
            found = True
            data = doc.to_dict()
            st.write(f"### Video {i+1}")
            st.write(data["summary"])
            st.write("---")

        if not found:
            st.info("No history yet")

    # -------- ABOUT --------
    else:
        st.title("ℹ️ About")
        st.write("AI Video Summarizer with Firebase + Whisper + NLP")

# ---------------- RUN ----------------
if not st.session_state.logged_in:
    login()
else:
    app()