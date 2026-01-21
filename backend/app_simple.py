from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime

app = FastAPI(title="Jarvis AI Assistant API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory storage
knowledge_base = []

# Pydantic models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[Message] = []

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = None

# Demo responses
DEMO_RESPONSES = [
    "I'm JARVIS, your personal AI assistant! I'm currently running in demo mode. To enable full AI capabilities, you'll need to set up Ollama with LLaMA.",
    "That's an interesting question! In demo mode, I can provide basic responses. For advanced AI-powered answers, please configure Ollama.",
    "I understand your query. Currently running without the LLaMA model, but I'm here to help demonstrate the interface!",
    "Great question! This is a demo response. The full AI experience requires Ollama to be properly configured.",
    "I'm processing your request in demo mode. For intelligent AI responses powered by LLaMA, please complete the Ollama setup."
]

response_index = 0

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ollama": False,
        "pinecone": False,
        "embeddings": False,
        "mode": "demo",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint - demo mode"""
    global response_index
    
    # Cycle through demo responses
    response = DEMO_RESPONSES[response_index % len(DEMO_RESPONSES)]
    response_index += 1
    
    # Add context if user asks specific questions
    message_lower = request.message.lower()
    
    if "who are you" in message_lower or "what are you" in message_lower:
        response = "I'm JARVIS, your personal AI assistant! I'm built with React, FastAPI, and designed to work with LLaMA AI models. Currently running in demo mode."
    elif "help" in message_lower:
        response = "I can help you with various tasks! Right now I'm in demo mode. To unlock full AI capabilities: 1) Install Ollama, 2) Pull LLaMA model, 3) Start Ollama server. Check the documentation for details!"
    elif "how" in message_lower and "work" in message_lower:
        response = "I use a RAG (Retrieval Augmented Generation) architecture with LLaMA for natural language understanding, Pinecone for vector storage, and FastAPI for the backend. The beautiful UI is built with React!"
    elif "thank" in message_lower:
        response = "You're welcome! Happy to help! 😊"
    
    return ChatResponse(response=response, sources=None)

@app.post("/upload")
async def upload_file(file: dict):
    """Upload endpoint - demo mode"""
    knowledge_base.append({
        "filename": "demo_file.txt",
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "message": "File uploaded successfully (demo mode)",
        "chunks": 1,
        "id": len(knowledge_base)
    }

@app.get("/knowledge")
async def get_knowledge():
    """Get knowledge base statistics"""
    return {
        "total_documents": len(knowledge_base),
        "vector_db_active": False,
        "embedding_model": None,
        "mode": "demo"
    }

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 JARVIS AI Assistant Backend Server (DEMO MODE)")
    print("="*60)
    print("✓ FastAPI server starting...")
    print("⚠️  Ollama: Not available (demo mode)")
    print("⚠️  Pinecone: Not configured (demo mode)")
    print("⚠️  Embeddings: Not loaded (demo mode)")
    print("="*60)
    print("\n🚀 Server running at: http://localhost:8000")
    print("📚 API docs at: http://localhost:8000/docs")
    print("\n💡 This is DEMO MODE - responses are pre-programmed.")
    print("   To enable full AI: Install Ollama + LLaMA model\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
