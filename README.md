# 🎤 Voice AI Agent

An end-to-end AI-powered Voice Assistant that converts speech to text, understands user intent using LLMs, and performs real-world actions such as file creation, code generation, and summarization through an interactive Streamlit UI.

---

## 🚀 Features

- 🎙️ **Voice Input**
  - Microphone recording (local)
  - Audio file upload (WAV, MP3, AAC)

- 🧠 **Intent Detection**
  - Uses LLM (Groq API) to classify user intent:
    - `create_file`
    - `write_code`
    - `summarize`
    - `chat`

- ⚙️ **Action Execution**
  - Create files
  - Generate and save code
  - Summarize text
  - Answer queries

- 🔄 **Compound Commands**
  - Supports multi-step instructions  
  - Example: *"Summarize this and save it to summary.txt"*

- 👤 **Human-in-the-Loop**
  - Confirmation before file operations

- 🧠 **Session Memory**
  - Stores interaction history in UI

- ⚠️ **Graceful Error Handling**
  - Handles unclear audio
  - Handles LLM failures
  - Fallback to chat response

---

## 🏗️ Architecture
Audio Input (Mic / File)
↓
Speech-to-Text (STT)
↓
LLM (Intent Detection + Parsing)
↓
Agent Logic (Decision Making)
↓
Tool Execution (File / Code / Summary)
↓
Streamlit UI (Display Result)


### Components

- **STT Module (`stt.py`)**
  - Converts audio → text

- **LLM Module (`llm.py`)**
  - Extracts structured JSON (intent, filename, etc.)

- **Agent (`agent.py`)**
  - Core decision-making logic
  - Handles compound commands and fallback

- **Tools (`tools.py`)**
  - Executes actions (file creation, code writing, summarization)

- **Frontend (`app.py`)**
  - Streamlit UI
  - Handles user interaction and display

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Groq API (LLM + STT)
- Pydub (audio processing)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/priya-kanade/voice-ai-agent.git
cd voice-ai-agent
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4.Add API Key

Create a .env file:

GROQ_API_KEY=your_api_key_here

### 5.Run the App
```bash
streamlit run app.py
```
## ⚠️ Hardware / Environment Notes

- 🎤 Microphone recording works only locally  
- 🌐 Hugging Face deployment supports file upload only  
- 🔄 AAC audio files are automatically converted to WAV using `pydub`  

---

## 📌 Example Commands

- “Create a file notes.txt”  
- “Write python code for binary search”  
- “Summarize what is machine learning”  
- “Summarize this and save it to summary.txt”  

---

## 🔮 Future Improvements

- Support advanced multi-command chaining  
- Add conversational memory with context awareness  
- Enable real-time microphone support in deployed environments  

