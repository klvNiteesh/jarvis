# 🤖 JARVIS - Personal AI Assistant

![Jarvis AI](https://img.shields.io/badge/AI-Powered-purple?style=for-the-badge)
![LLaMA](https://img.shields.io/badge/LLaMA-Model-blue?style=for-the-badge)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector_DB-green?style=for-the-badge)

A powerful personal AI assistant powered by **self-hosted LLaMA** (via Ollama), with **Pinecone vector database** for knowledge storage and retrieval, featuring a beautiful conversational chatbot UI.

## ✨ Features

- 🧠 **Self-Hosted LLaMA Model** - Run AI locally using Ollama
- 📚 **Vector Database Integration** - Pinecone for semantic search and RAG
- 💬 **Conversational Interface** - Beautiful, responsive chatbot UI
- 📄 **Document Processing** - Upload and process documents for knowledge base
- 🔍 **Contextual Responses** - Retrieval Augmented Generation (RAG)
- 🎨 **Premium Design** - Glassmorphism, gradients, and smooth animations

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   React UI      │ ───▶ │  FastAPI Backend │ ───▶ │  Ollama/LLaMA   │
│  (Frontend)     │ ◀─── │    (Python)      │ ◀─── │   (Local AI)    │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    Pinecone     │
                         │  (Vector DB)    │
                         └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v18 or higher)
- **Python** (3.8 or higher)
- **Ollama** (for LLaMA model)

### Step 1: Install Ollama and LLaMA

```bash
# Install Ollama from https://ollama.ai/

# Pull LLaMA model
ollama pull llama2

# Start Ollama server (if not already running)
ollama serve
```

### Step 2: Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Configure Pinecone
# Copy .env.example to .env and add your Pinecone API key
cp .env.example .env
# Edit .env and add: PINECONE_API_KEY=your_key_here

# Start backend server
python app.py
```

The backend will be running at `http://localhost:8000`

### Step 3: Setup Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be running at `http://localhost:5173`

## 📖 Usage

1. **Open the app** in your browser at `http://localhost:5173`
2. **Check system status** in the sidebar to ensure all components are connected
3. **Start chatting** with Jarvis in the main chat interface
4. **Upload documents** to add knowledge to the assistant's knowledge base
5. **Ask questions** and get contextual responses based on uploaded documents

## 🎯 Key Components

### Frontend (React + Vite)
- Modern, responsive UI with glassmorphism design
- Real-time chat interface
- File upload for knowledge base
- System status monitoring

### Backend (FastAPI)
- RESTful API endpoints
- LLaMA integration via Ollama
- Vector database integration (Pinecone)
- Document processing and chunking
- Retrieval Augmented Generation (RAG)

### AI Stack
- **LLM**: LLaMA 2 (via Ollama) - Self-hosted
- **Embeddings**: all-MiniLM-L6-v2 (SentenceTransformers)
- **Vector DB**: Pinecone (optional, falls back to in-memory)

## 🔧 Configuration

### Pinecone Setup (Optional)

1. Sign up for free at [pinecone.io](https://www.pinecone.io/)
2. Create an API key
3. Add to `backend/.env`:
   ```
   PINECONE_API_KEY=your_api_key_here
   ```

**Note**: The app works without Pinecone using in-memory storage, but Pinecone provides better scalability and persistence.

### Ollama Models

You can use different LLaMA models:

```bash
# LLaMA 2 (default)
ollama pull llama2

# LLaMA 3 (if available)
ollama pull llama3

# Mistral (alternative)
ollama pull mistral
```

Update `backend/app.py` line 128 to change the model:
```python
model='llama2'  # Change to 'llama3' or 'mistral'
```

## 📡 API Endpoints

- `GET /health` - Health check and system status
- `POST /chat` - Send message and get AI response
- `POST /upload` - Upload document to knowledge base
- `GET /knowledge` - Get knowledge base statistics

Full API documentation available at `http://localhost:8000/docs`

## 🎨 Features Showcase

### Conversational AI
- Natural language understanding
- Context-aware responses
- Conversation history tracking

### Knowledge Management
- Document upload and processing
- Automatic text chunking
- Semantic search with embeddings
- RAG for accurate, contextual answers

### Beautiful UI
- Dark theme with vibrant gradients
- Glassmorphism effects
- Smooth animations
- Responsive design (mobile-friendly)

## 🛠️ Development

### Project Structure

```
jarvis-ai-assistant/
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.jsx        # Main component
│   │   ├── App.css        # Styles
│   │   └── index.css      # Base styles
│   └── package.json
├── backend/               # Python backend
│   ├── app.py            # FastAPI server
│   ├── requirements.txt  # Dependencies
│   └── .env.example      # Environment template
└── README.md
```

### Tech Stack

**Frontend:**
- React 18
- Vite
- CSS3 (Glassmorphism, Gradients)

**Backend:**
- FastAPI
- Ollama (LLaMA)
- Pinecone
- SentenceTransformers

## 🐛 Troubleshooting

### Backend won't connect
- Ensure Python server is running: `python backend/app.py`
- Check if port 8000 is available
- Verify CORS settings if accessing from different domain

### Ollama errors
- Make sure Ollama is installed and running: `ollama serve`
- Pull the model: `ollama pull llama2`
- Check Ollama status: `ollama list`

### Slow responses
- LLaMA models require significant compute power
- Consider using smaller models for faster responses
- Ensure your system meets minimum requirements (8GB RAM recommended)

## 📝 License

MIT License - Feel free to use this project for learning and development!

## 🙏 Acknowledgments

- **Meta** - LLaMA model
- **Ollama** - Local LLM serving
- **Pinecone** - Vector database
- **FastAPI** - Backend framework
- **React** - Frontend framework

## 🚀 Future Enhancements

- [ ] Voice input/output
- [ ] Multi-modal support (images, videos)
- [ ] Custom model fine-tuning
- [ ] Advanced RAG techniques
- [ ] User authentication
- [ ] Conversation persistence
- [ ] Mobile app

---

**Built with ❤️ for the AI community**

*Duration: 40 minutes | Tool: VS Code + Co-pilot*
