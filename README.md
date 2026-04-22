🎬 AI Video Summarizer

An AI-powered web application that converts video content into text transcripts and concise summaries in seconds. Built using modern NLP models and deployed with an interactive UI for seamless user experience.

---

🚀 Features

- 🎥 Upload videos (MP4, MOV, AVI)
- 🧠 Automatic speech-to-text using OpenAI Whisper
- ✍️ Text summarization using HuggingFace Transformers
- ⚡ Optimized performance with caching (fast processing)
- 📜 Session-based history tracking
- 🔐 Basic authentication system (login/logout)
- 🎨 Clean and responsive UI using Streamlit + custom CSS

---

🛠️ Tech Stack

- Frontend/UI: Streamlit
- Backend Logic: Python
- AI Models:
  - Whisper (Speech-to-Text)
  - Transformers (Summarization)
- Optimization: Streamlit caching ("@st.cache_resource", "@st.cache_data")
- Version Control: Git + GitHub

---

⚡ Performance Optimizations

- Cached AI models to prevent reloading on every run
- Cached transcription and summarization outputs
- File hashing to avoid duplicate processing
- Lightweight Whisper model ("tiny") for faster inference

---

📂 Project Structure

video-to-text-summarizer/
│
├── app_ui.py           # Main Streamlit application
├── requirements.txt    # Dependencies
├── firebase_key.json   # (Optional) Firebase config
├── .gitignore
└── README.md

---

▶️ Installation & Setup

1. Clone the repository

git clone https://github.com/your-username/video-to-text-summarizer.git
cd video-to-text-summarizer

2. Install dependencies

pip install -r requirements.txt

3. Run the application

streamlit run app_ui.py

---

🔐 Demo Login Credentials

Username: admin  
Password: 1234

---

📸 How It Works

1. Upload a video file
2. Whisper extracts speech → text
3. Transformer model generates summary
4. Results are displayed instantly
5. History is stored for session tracking

---

🌟 Future Enhancements

- 🔥 Firebase authentication (real users)
- ☁️ Cloud storage for videos & transcripts
- 📊 User dashboard with analytics
- ⚡ GPU acceleration for faster processing
- 📱 Mobile-responsive UI

---

🤝 Contributing

Contributions are welcome!
Feel free to fork this repo and submit a pull request.

---

📜 License

This project is open-source and available under the MIT License.

---

👨‍💻 Author

Swapnil Shukla
B.Tech CSE | AI/ML Enthusiast

---

⭐ Support

If you like this project, give it a ⭐ on GitHub!
