# JARVIS AI Assistant - Quick Start Guide

## 🎯 Objective
Build a personal AI assistant powered by self-hosted LLaMA with vector database integration.

## 📋 Prerequisites Checklist

- [ ] Node.js installed (v18+)
- [ ] Python installed (3.8+)
- [ ] Ollama installed
- [ ] LLaMA model downloaded

## 🚀 Installation Steps

### 1. Install Ollama (5 minutes)

**Windows/Mac/Linux:**
```bash
# Visit https://ollama.ai/ and download the installer
# Or use package manager:

# Mac
brew install ollama

# Linux
curl https://ollama.ai/install.sh | sh
```

### 2. Download LLaMA Model (5 minutes)

```bash
# Pull LLaMA 2 model (default)
ollama pull llama2

# Start Ollama server
ollama serve
```

### 3. Setup Project (5 minutes)

**Automated Setup (Windows):**
```bash
# Run the setup script
setup.bat
```

**Manual Setup:**

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 4. Configure Pinecone (Optional - 5 minutes)

1. Sign up at https://www.pinecone.io/ (free tier available)
2. Create an API key
3. Copy `backend/.env.example` to `backend/.env`
4. Add your API key:
   ```
   PINECONE_API_KEY=your_key_here
   ```

**Note:** App works without Pinecone using in-memory storage!

### 5. Start the Application (1 minute)

**Automated (Windows):**
```bash
start.bat
```

**Manual:**

Terminal 1 - Backend:
```bash
cd backend
venv\Scripts\activate
python app.py
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

### 6. Access the Application

- **Frontend UI:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 🎨 Using JARVIS

### Basic Chat
1. Open http://localhost:5173
2. Type your message in the input box
3. Press Enter or click Send
4. Get AI-powered responses!

### Upload Documents
1. Click "Upload Documents" in the Knowledge Base section
2. Select .txt, .pdf, or .doc files
3. Documents are processed and added to the knowledge base
4. Ask questions about the uploaded content!

### Check System Status
- Green dots = All systems operational
- Red/Gray dots = Component offline or not configured

## 🔧 Troubleshooting

### "Backend Offline" Error
**Solution:**
```bash
# Make sure backend is running
cd backend
venv\Scripts\activate
python app.py
```

### "Ollama Error" in Chat
**Solution:**
```bash
# Ensure Ollama is running
ollama serve

# Verify model is downloaded
ollama list

# If llama2 not listed:
ollama pull llama2
```

### Slow Responses
**Causes:**
- LLaMA models are compute-intensive
- First response is slower (model loading)

**Solutions:**
- Use smaller models: `ollama pull tinyllama`
- Ensure adequate RAM (8GB+ recommended)
- Close other applications

### Port Already in Use
**Backend (8000):**
```bash
# Change port in backend/app.py, line 172:
uvicorn.run(app, host="0.0.0.0", port=8001)  # Change 8000 to 8001
```

**Frontend (5173):**
```bash
# Vite will automatically use next available port
# Or specify in frontend/vite.config.js
```

## 📊 System Requirements

### Minimum
- CPU: 4 cores
- RAM: 8GB
- Storage: 10GB free
- OS: Windows 10+, macOS 10.15+, Linux

### Recommended
- CPU: 8 cores
- RAM: 16GB
- Storage: 20GB free (for multiple models)
- GPU: Optional but improves performance

## 🎯 Testing the System

### 1. Basic Functionality
```
You: Hello, who are you?
Jarvis: I'm Jarvis, your personal AI assistant...
```

### 2. Knowledge Base
```
1. Upload a text file about Python
2. Ask: "What is Python?"
3. Jarvis should reference the uploaded document
```

### 3. Context Awareness
```
You: What's the weather like?
Jarvis: [Response]
You: What about tomorrow?
Jarvis: [Should understand context from previous message]
```

## 📚 Next Steps

1. **Customize the UI** - Edit `frontend/src/App.css`
2. **Try Different Models** - `ollama pull mistral`
3. **Add More Features** - Voice input, image support
4. **Deploy** - Host on cloud platforms

## 🆘 Getting Help

- Check the main README.md for detailed documentation
- Review API docs at http://localhost:8000/docs
- Check Ollama docs: https://ollama.ai/docs
- Pinecone docs: https://docs.pinecone.io/

## ✅ Success Checklist

- [ ] Ollama installed and running
- [ ] LLaMA model downloaded
- [ ] Backend server running (port 8000)
- [ ] Frontend server running (port 5173)
- [ ] Can send messages and get responses
- [ ] Can upload documents
- [ ] System status shows all green

---

**Estimated Total Time: 20-30 minutes**

**You're ready to build your own Jarvis! 🚀**
