from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ChromaDB for vector storage
try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("⚠️  ChromaDB not installed. Install with: pip install chromadb")

# Gemini AI - Updated to new package
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    try:
        import google.generativeai as genai
        GEMINI_AVAILABLE = True
    except ImportError:
        GEMINI_AVAILABLE = False
        print("⚠️  Gemini not installed. Install with: pip install google-genai")

# Sentence transformers for embeddings
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("⚠️  Sentence transformers not installed")

app = FastAPI(title="Jarvis AI Assistant API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
embedding_model = None
chroma_client = None
collection = None
gemini_model = None

# Initialize Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY and GEMINI_AVAILABLE:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        print("✓ Gemini AI (2.0 Flash) configured successfully")
    except Exception as e:
        print(f"⚠️  Gemini configuration failed: {e}")

# Initialize ChromaDB
if CHROMA_AVAILABLE:
    try:
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
        collection = chroma_client.get_or_create_collection(
            name="jarvis_knowledge",
            metadata={"description": "JARVIS knowledge base"}
        )
        print("✓ ChromaDB initialized successfully")
    except Exception as e:
        print(f"⚠️  ChromaDB initialization failed: {e}")

# Initialize embedding model
if EMBEDDINGS_AVAILABLE:
    try:
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ Embedding model loaded successfully")
    except Exception as e:
        print(f"⚠️  Failed to load embedding model: {e}")

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

# Helper functions
def get_embedding(text: str):
    """Generate embedding for text"""
    if embedding_model:
        return embedding_model.encode(text).tolist()
    return None

def store_in_chroma(text: str, metadata: dict):
    """Store text in ChromaDB"""
    if collection and embedding_model:
        try:
            embedding = get_embedding(text)
            doc_id = f"doc_{datetime.now().timestamp()}"
            collection.add(
                embeddings=[embedding],
                documents=[text],
                metadatas=[metadata],
                ids=[doc_id]
            )
            return doc_id
        except Exception as e:
            print(f"ChromaDB storage error: {e}")
    return None

def search_knowledge_base(query: str, top_k: int = 3):
    """Search for relevant context in ChromaDB"""
    if collection and embedding_model:
        try:
            query_embedding = get_embedding(query)
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            if results and results['documents']:
                return results['documents'][0]
            return []
        except Exception as e:
            print(f"ChromaDB search error: {e}")
    return []

def get_gemini_response(prompt: str, context: str = ""):
    """Get response from Gemini AI"""
    if gemini_model:
        try:
            full_prompt = f"{context}\n\nUser: {prompt}\nAssistant:" if context else prompt
            response = gemini_model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Gemini error: {e}")
            return f"⚠️ Gemini API error: {str(e)}. Please check your API key."
    
    # Fallback response
    return "I'm running in demo mode. To enable full AI capabilities, please add your Gemini API key to the .env file."

# API Routes
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "gemini": gemini_model is not None,
        "chromadb": collection is not None,
        "embeddings": embedding_model is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint with RAG"""
    try:
        # Search knowledge base for relevant context
        context_docs = search_knowledge_base(request.message)
        context = "\n\n".join([f"Context: {doc}" for doc in context_docs]) if context_docs else ""
        
        # Build conversation history
        history_text = "\n".join([
            f"{msg.role.capitalize()}: {msg.content}" 
            for msg in request.history[-5:]  # Last 5 messages
        ])
        
        # Combine context and history
        full_context = f"{context}\n\nConversation History:\n{history_text}" if history_text else context
        
        # Get Gemini response
        response = get_gemini_response(request.message, full_context)
        
        return ChatResponse(
            response=response,
            sources=[doc[:100] + "..." for doc in context_docs] if context_docs else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process documents for knowledge base"""
    try:
        # Read file content
        content = await file.read()
        text = content.decode('utf-8', errors='ignore')
        
        # Split into chunks (simple chunking)
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        
        # Store each chunk
        doc_ids = []
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                doc_id = store_in_chroma(
                    chunk,
                    {
                        'filename': file.filename,
                        'chunk': i,
                        'timestamp': datetime.now().isoformat()
                    }
                )
                if doc_id:
                    doc_ids.append(doc_id)
        
        return {
            "message": f"Successfully processed {file.filename}",
            "chunks": len(doc_ids),
            "id": doc_ids[0] if doc_ids else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/knowledge")
async def get_knowledge():
    """Get knowledge base statistics"""
    doc_count = 0
    if collection:
        try:
            doc_count = collection.count()
        except:
            pass
    
    return {
        "total_documents": doc_count,
        "vector_db_active": collection is not None,
        "embedding_model": "all-MiniLM-L6-v2" if embedding_model else None
    }

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 JARVIS AI Assistant Backend Server")
    print("="*60)
    print(f"✓ FastAPI server starting...")
    print(f"{'✓' if gemini_model else '⚠️ '} Gemini AI: {'Available' if gemini_model else 'Not configured'}")
    print(f"{'✓' if collection else '⚠️ '} ChromaDB: {'Available' if collection else 'Not installed'}")
    print(f"{'✓' if embedding_model else '⚠️ '} Embeddings: {'Available' if embedding_model else 'Not installed'}")
    print("="*60)
    print("\n🚀 Server running at: http://localhost:8000")
    print("📚 API docs at: http://localhost:8000/docs\n")
    
    if not gemini_model:
        print("💡 To enable Gemini AI:")
        print("   1. Get API key from: https://makersuite.google.com/app/apikey")
        print("   2. Add to .env file: GEMINI_API_KEY=your_key_here\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
