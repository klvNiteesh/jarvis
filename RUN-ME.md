# 🚀 SIMPLE RUN GUIDE

## ⚡ Quick Start (3 Terminals)

### Terminal 1: Start Ollama
```bash
ollama serve
```
**Leave this running!**

---

### Terminal 2: Start Backend
```bash
cd d:\AI\jarvis-ai-assistant\backend
.\venv\Scripts\activate
python app.py
```
**Leave this running!** Backend will be at http://localhost:8000

---

### Terminal 3: Start Frontend
```bash
cd d:\AI\jarvis-ai-assistant\frontend
npm run dev
```
**Leave this running!** Frontend will be at http://localhost:5173

---

## 🌐 Open in Browser

Go to: **http://localhost:5173**

---

## ✅ First Time Setup (Do Once)

### 1. Install Ollama
- Download from: https://ollama.ai/
- Install and run: `ollama pull llama2`

### 2. Setup Backend
```bash
cd d:\AI\jarvis-ai-assistant\backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup Frontend
```bash
cd d:\AI\jarvis-ai-assistant\frontend
npm install
```

---

## 🛑 To Stop

Press `Ctrl + C` in each terminal window.

---

## 🐛 Troubleshooting

**"Backend Offline"**
- Make sure Ollama is running: `ollama serve`
- Make sure backend is running on port 8000

**"Module not found"**
- Backend: Make sure venv is activated and dependencies installed
- Frontend: Run `npm install` in frontend directory

**Port already in use**
- Kill the process using the port
- Or restart your computer

---

**That's it! Enjoy your JARVIS AI Assistant! 🤖**
