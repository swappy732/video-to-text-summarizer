import streamlit as st
from moviepy.editor import VideoFileClip
import whisper
from transformers import pipeline
import tempfile
import os

st.set_page_config(page_title="Video Summarizer", layout="wide")

st.title("🎥 Video to Text Summarizer (Advanced)")

video_file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])

if video_file:
st.video(video_file)

temp_video = tempfile.NamedTemporaryFile(delete=False)
temp_video.write(video_file.read())
video_path = temp_video.name

st.info("🔊 Extracting audio...")
video = VideoFileClip(video_path)
audio_path = "audio.wav"
video.audio.write_audiofile(audio_path)

st.info("🧠 Transcribing using Whisper...")
model = whisper.load_model("base")
result = model.transcribe(audio_path)
transcript = result["text"]

st.subheader("📄 Transcript")
st.write(transcript)

st.download_button(
    "⬇️ Download Transcript",
    transcript,
    file_name="transcript.txt"
)

st.info("✂️ Summarizing...")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Handle long text safely
chunks = [transcript[i:i+1000] for i in range(0, len(transcript), 1000)]
summary = ""

for chunk in chunks:
    result = summarizer(chunk, max_length=120, min_length=40, do_sample=False)
    summary += result[0]["summary_text"] + " "

st.subheader("📝 Summary")
st.write(summary)

st.download_button(
    "⬇️ Download Summary",
    summary,
    file_name="summary.txt"
)

os.remove(video_path)