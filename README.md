# AICTE-AI-Lecture-Voice-to-Notes-Generator
An AI-based educational web application built with Streamlit and Google Gemini API that generates summaries and MCQs from YouTube links or audio files. Requires user-provided API key.

An AI-powered Streamlit web application that generates structured study materials, summaries, and MCQs from YouTube videos or uploaded audio files using Google's Gemini API.

---

## 🚀 Features

- 📺 Generate study notes from YouTube URLs  
- 🎧 Upload audio files (MP3, WAV, M4A)  
- 📝 Automatically generate MCQs  
- 🎯 Select difficulty level (Easy / Medium / Difficult)  
- 🎨 Custom dark-themed UI  
- 🔐 Secure API key input (User provides their own Gemini API key)

---

## 🔐 IMPORTANT – Gemini API Key Required

⚠️ **This project does NOT include any API key.**

To use this application:

1. Create your own Gemini API key from Google AI Studio.
2. Enter your API key inside the app or code .

👉 The API key is entered by the user in code.  
👉 The developer's personal API key is NOT shared, stored, or hardcoded.  

This ensures security, privacy, and best development practices.

---

## 🛠 Installation (Run Locally)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the application

```bash
streamlit run app.py
```

The app will open in your browser.

---

## 📦 Deployment (Streamlit Community Cloud)

When deploying:

- Select `app.py` as the main file.
- Ensure `requirements.txt` is included.
- Users must enter their own Gemini API key inside the app.

---

## 🧠 Technologies Used

- Python  
- Streamlit  
- Google Gemini API  
- YouTube Transcript API  
- Pytube  
- MoviePy  

---

## 📌 Project Domain

Artificial Intelligence (AI)  
Educational Technology (EdTech)  

---

## ⚠️ Security Note

- No API keys are stored in this repository.
- Do NOT upload `.env` files.
- Do NOT hardcode your personal API keys.

---

## 👨‍💻 Author

Developed as an AI domain project using modern generative AI tools.
