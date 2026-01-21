# JARVIS AI Assistant - System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         JARVIS AI ASSISTANT                          │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                          FRONTEND LAYER                              │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                    React + Vite UI                          │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │    │
│  │  │   Chat   │  │  Upload  │  │  Status  │  │ Knowledge│  │    │
│  │  │Interface │  │  Files   │  │ Monitor  │  │   Base   │  │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │    │
│  │                                                             │    │
│  │  Features: Glassmorphism, Real-time Chat, File Upload     │    │
│  └────────────────────────────────────────────────────────────┘    │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ HTTP/REST API
                            │ (localhost:5173 → localhost:8000)
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         BACKEND LAYER                                │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                    FastAPI Server                           │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │    │
│  │  │   Chat   │  │ Document │  │   RAG    │  │  Vector  │  │    │
│  │  │Endpoint  │  │Processing│  │  Engine  │  │  Search  │  │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │    │
│  │                                                             │    │
│  │  Endpoints: /chat, /upload, /health, /knowledge           │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────┬──────────────────┬──────────────────┬─────────────────────────┘
      │                  │                  │
      ▼                  ▼                  ▼
┌──────────┐      ┌─────────────┐    ┌──────────────┐
│  Ollama  │      │  Sentence   │    │   Pinecone   │
│  LLaMA   │      │Transformers │    │  Vector DB   │
│          │      │             │    │              │
│ • llama2 │      │ • Embedding │    │ • Semantic   │
│ • Local  │      │ • MiniLM-L6 │    │   Search     │
│ • Self   │      │ • 384-dim   │    │ • Storage    │
│   Hosted │      │   vectors   │    │ • Retrieval  │
└──────────┘      └─────────────┘    └──────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW                                    │
└─────────────────────────────────────────────────────────────────────┘

1. USER QUERY FLOW:
   User Input → Frontend → Backend → RAG Engine
                                      ├─→ Vector Search (Pinecone)
                                      │   └─→ Retrieve Context
                                      └─→ LLM Query (Ollama/LLaMA)
                                          └─→ Generate Response
   Response ← Frontend ← Backend ← Combined Output

2. DOCUMENT UPLOAD FLOW:
   File Upload → Frontend → Backend → Document Processor
                                      ├─→ Text Extraction
                                      ├─→ Chunking (500 chars)
                                      ├─→ Generate Embeddings
                                      └─→ Store in Vector DB

3. KNOWLEDGE RETRIEVAL (RAG):
   Query → Embedding → Vector Search → Top-K Results → Context
                                                         ↓
   LLM Prompt = Context + Query + History → Response

┌─────────────────────────────────────────────────────────────────────┐
│                      TECHNOLOGY STACK                                │
└─────────────────────────────────────────────────────────────────────┘

Frontend:
  • React 18
  • Vite (Build tool)
  • CSS3 (Glassmorphism, Gradients)
  • Fetch API

Backend:
  • Python 3.8+
  • FastAPI (Web framework)
  • Uvicorn (ASGI server)
  • Pydantic (Data validation)

AI/ML:
  • Ollama (LLM serving)
  • LLaMA 2 (Language model)
  • SentenceTransformers (Embeddings)
  • all-MiniLM-L6-v2 (Embedding model)

Database:
  • Pinecone (Vector database)
  • In-memory fallback

┌─────────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────────┘

Development:
  Frontend: http://localhost:5173
  Backend:  http://localhost:8000
  Ollama:   http://localhost:11434

Production Options:
  • Frontend: Vercel, Netlify, GitHub Pages
  • Backend: Railway, Render, AWS EC2
  • Ollama: Self-hosted server, cloud GPU
  • Pinecone: Managed cloud service

┌─────────────────────────────────────────────────────────────────────┐
│                      SECURITY & PRIVACY                              │
└─────────────────────────────────────────────────────────────────────┘

• Self-hosted LLM (data never leaves your infrastructure)
• CORS protection
• Environment variables for secrets
• Optional Pinecone encryption
• No data logging by default

┌─────────────────────────────────────────────────────────────────────┐
│                      SCALABILITY                                     │
└─────────────────────────────────────────────────────────────────────┘

• Horizontal: Multiple backend instances
• Vertical: Larger LLM models, more RAM
• Caching: Redis for frequent queries
• Load balancing: Nginx/HAProxy
• Database: Pinecone auto-scales
```
