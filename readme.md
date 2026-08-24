# 🤖 JARVIS-AI

A free, modular AI voice assistant inspired by **JARVIS**.

The goal is to build a personal voice assistant that can understand natural language, remember context, search the web, and interact with the user's computer.

## 🚀 Features

* 🎙️ Speech-to-text using Whisper
* 🧠 LLM conversations using Groq
* 🔊 Text-to-speech
* 💾 Conversation memory
* 🔎 Web search
* 🖥️ Desktop automation
* 📂 File interaction
* ⏰ Reminders and tasks
* 💻 Coding assistance
* 🗣️ Wake-word activation
* ⚙️ Modular skill/command system

## 🛠️ Tech Stack

* **Python** — Core language
* **Groq** — LLM
* **faster-whisper** — Speech-to-text
* **Piper TTS** — Text-to-speech
* **FastAPI** — Backend
* **PostgreSQL + pgvector** — Database & vector memory
* **SQLAlchemy** — ORM
* **OpenWakeWord** — Wake-word detection
* **PyAutoGUI** — Desktop automation
* **Git & GitHub** — Version control

## 🏗️ Architecture

```text
                 🎤 Microphone
                       │
                       ▼
                Speech-to-Text
                (Whisper)
                       │
                       ▼
                 🧠 Groq LLM
                       │
            ┌──────────┼──────────┐
            ▼          ▼          ▼
         Memory      Tools     Web Search
            │          │          │
            └──────────┼──────────┘
                       ▼
                Response Generation
                       │
                       ▼
                 🔊 Text-to-Speech
                       │
                       ▼
                    Speaker
```

## 📁 Project Structure

```text
JARVIS-AI/
│
├── app/
│   ├── main.py
│   ├── assistant/
│   ├── voice/
│   ├── memory/
│   ├── tools/
│   └── config/
│
├── tests/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd JARVIS-AI
```

### 2. Create environment

```bash
conda create -n jarvis python=3.11
conda activate jarvis
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
DATABASE_URL=your_postgresql_url
```

### 5. Run

```bash
python app/main.py
```

## 🗺️ Development Roadmap

* [x] Whisper speech-to-text test
* [ ] Microphone input
* [ ] Groq LLM integration
* [ ] Text-to-speech
* [ ] Basic conversation loop
* [ ] Conversation memory
* [ ] PostgreSQL integration
* [ ] Web search
* [ ] Desktop automation
* [ ] Wake-word detection
* [ ] Modular skill system
* [ ] Web dashboard

## 🎯 Goal

Build a practical, modular and **zero-cost-to-start AI voice assistant** that can gradually evolve from a simple voice chatbot into a complete personal computer assistant.

