# 🤖 JARVIS - Personal AI Assistant

![JARVIS](https://img.shields.io/badge/AI-Powered-purple?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Gemini-2.0_Flash-blue?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-green?style=for-the-badge)

A powerful personal AI assistant powered by **Google Gemini 2.0 Flash**, with **ChromaDB vector database** for knowledge storage and retrieval, featuring a beautiful conversational chatbot UI.

## ✨ Features

- 🧠 **Gemini 2.0 Flash AI** - Latest Google AI model
- 📚 **ChromaDB Vector Database** - Local semantic search and RAG
- 💬 **Beautiful Conversational UI** - Modern, responsive chatbot interface
- 📄 **Document Processing** - Upload and process documents for knowledge base
- 🔍 **Contextual Responses** - Retrieval Augmented Generation (RAG)
- 🎨 **Premium Design** - Glassmorphism, gradients, and smooth animations

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React UI      │────▶│  FastAPI Server │────▶│  Gemini 2.0     │
│  (Frontend)     │     │   (Backend)     │     │   Flash AI      │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │    ChromaDB     │
                        │  (Vector Store) │
                        └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v18 or higher)
- **Python** (3.8 or higher)
- **Gemini API Key** (free from Google)

### Step 1: Get Gemini API Key (FREE)

1. Go to: **https://makersuite.google.com/app/apikey**
2. Click **"Create API Key"**
3. Copy the API key

### Step 2: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/klvNiteesh/jarvis.git
cd jarvis

# Setup Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements_new.txt

# Configure API Key
# Edit backend/.env and add:
GEMINI_API_KEY=your_api_key_here

# Start Backend
python app_gemini.py
```

### Step 3: Setup Frontend

```bash
# In a new terminal
cd frontend
npm install
npm run dev
```

### Step 4: Open the App

Open your browser and go to: **http://localhost:5173**

## 📖 Usage

1. **Open the app** in your browser at `http://localhost:5173`
2. **Check system status** in the sidebar to ensure all components are connected
3. **Start chatting** with JARVIS in the main chat interface
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
- Gemini 2.0 Flash integration
- ChromaDB vector database
- Document processing and chunking
- Retrieval Augmented Generation (RAG)

### AI Stack
- **LLM**: Gemini 2.0 Flash (Google AI)
- **Embeddings**: all-MiniLM-L6-v2 (SentenceTransformers)
- **Vector DB**: ChromaDB (local, persistent)

## 🔧 Configuration

### Gemini API Key

1. Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `backend/.env`:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

### ChromaDB

ChromaDB runs locally and stores data in `backend/chroma_db/`. No additional configuration needed!

## 📡 API Endpoints

- `GET /health` - Health check and system status
- `POST /chat` - Send message and get AI response
- `POST /upload` - Upload document to knowledge base
- `GET /knowledge` - Get knowledge base statistics

Full API documentation available at `http://localhost:8000/docs`

## 🎨 Features Showcase

### Conversational AI
- Natural language understanding with Gemini 2.0 Flash
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
jarvis/
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.jsx        # Main component
│   │   ├── App.css        # Styles
│   │   └── index.css      # Base styles
│   └── package.json
├── backend/               # Python backend
│   ├── app_gemini.py     # FastAPI server with Gemini
│   ├── requirements_new.txt  # Dependencies
│   ├── .env              # Environment variables
│   └── chroma_db/        # Vector database storage
├── README.md
└── SETUP-GEMINI.md       # Detailed setup guide
```

### Tech Stack

**Frontend:**
- React 18
- Vite
- CSS3 (Glassmorphism, Gradients)

**Backend:**
- FastAPI
- Google Gemini 2.0 Flash
- ChromaDB
- SentenceTransformers

## 🐛 Troubleshooting

### Backend won't connect
- Ensure Python server is running: `python app_gemini.py`
- Check if port 8000 is available
- Verify Gemini API key in `.env` file

### Gemini API errors
- Make sure you have a valid API key
- Check your API quota at [Google AI Studio](https://makersuite.google.com/)
- Ensure you're using the correct model name

### ChromaDB errors
- Delete `backend/chroma_db/` folder and restart
- Reinstall ChromaDB: `pip install --upgrade chromadb`

## 📝 License

MIT License - Feel free to use this project for learning and development!

## 🙏 Acknowledgments

- **Google** - Gemini AI
- **ChromaDB** - Vector database
- **FastAPI** - Backend framework
- **React** - Frontend framework

## 🚀 Future Enhancements

- [ ] Voice input/output
- [ ] Multi-modal support (images, videos)
- [ ] Advanced RAG techniques
- [ ] User authentication
- [ ] Conversation persistence
- [ ] Mobile app
- [ ] Multiple language support

## 📊 System Requirements

### Minimum
- CPU: 4 cores
- RAM: 8GB
- Storage: 5GB free
- OS: Windows 10+, macOS 10.15+, Linux

### Recommended
- CPU: 8 cores
- RAM: 16GB
- Storage: 10GB free
- Internet: Stable connection for Gemini API

## 🎯 Why This Stack?

| Feature | Benefit |
|---------|---------|
| **Gemini 2.0 Flash** | Latest AI model, fast responses, free tier |
| **ChromaDB** | Local storage, no cloud costs, privacy-first |
| **FastAPI** | Modern, fast, auto-documented APIs |
| **React** | Component-based, responsive, beautiful UI |

## 🌟 Star History

If you find this project helpful, please give it a ⭐!

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the [Setup Guide](SETUP-GEMINI.md)
- Review API docs at `http://localhost:8000/docs`

---

**Built with ❤️ by [Niteesh](https://github.com/klvNiteesh)**

*A modern AI assistant for everyone!*
