from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from datetime import datetime
import json

# Ollama integration for LLaMA
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("⚠️  Ollama not installed. Install with: pip install ollama")

# Pinecone integration
try:
    from pinecone import Pinecone, ServerlessSpec
    import hashlib
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False
    print("⚠️  Pinecone not installed. Install with: pip install pinecone-client")

# Sentence transformers for embeddings
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("⚠️  Sentence transformers not installed. Install with: pip install sentence-transformers")

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
pinecone_index = None
knowledge_base = []  # Fallback in-memory storage

if EMBEDDINGS_AVAILABLE:
    try:
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ Embedding model loaded successfully")
    except Exception as e:
        print(f"⚠️  Failed to load embedding model: {e}")

if PINECONE_AVAILABLE:
    try:
        # Initialize Pinecone (you'll need to set your API key)
        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
        if PINECONE_API_KEY:
            pc = Pinecone(api_key=PINECONE_API_KEY)
            
            # Create or connect to index
            index_name = "jarvis-knowledge"
            if index_name not in pc.list_indexes().names():
                pc.create_index(
                    name=index_name,
                    dimension=384,  # all-MiniLM-L6-v2 dimension
                    metric='cosine',
                    spec=ServerlessSpec(cloud='aws', region='us-east-1')
                )
            pinecone_index = pc.Index(index_name)
            print("✓ Pinecone connected successfully")
        else:
            print("⚠️  PINECONE_API_KEY not set. Using in-memory storage.")
    except Exception as e:
        print(f"⚠️  Pinecone initialization failed: {e}")

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

def store_in_vector_db(text: str, metadata: dict):
    """Store text in vector database"""
    if pinecone_index and embedding_model:
        try:
            embedding = get_embedding(text)
            doc_id = hashlib.md5(text.encode()).hexdigest()
            pinecone_index.upsert(vectors=[{
                'id': doc_id,
                'values': embedding,
                'metadata': {**metadata, 'text': text}
            }])
            return doc_id
        except Exception as e:
            print(f"Vector DB storage error: {e}")
    
    # Fallback to in-memory
    knowledge_base.append({'text': text, 'metadata': metadata})
    return len(knowledge_base) - 1

def search_knowledge_base(query: str, top_k: int = 3):
    """Search for relevant context in knowledge base"""
    if pinecone_index and embedding_model:
        try:
            query_embedding = get_embedding(query)
            results = pinecone_index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            return [match['metadata']['text'] for match in results['matches']]
        except Exception as e:
            print(f"Vector search error: {e}")
    
    # Fallback: simple keyword search
    relevant = []
    query_lower = query.lower()
    for item in knowledge_base:
        if any(word in item['text'].lower() for word in query_lower.split()):
            relevant.append(item['text'])
            if len(relevant) >= top_k:
                break
    return relevant

def get_llm_response(prompt: str, context: str = ""):
    """Get response from LLaMA via Ollama"""
    if OLLAMA_AVAILABLE:
        try:
            full_prompt = f"{context}\n\nUser: {prompt}\nAssistant:" if context else prompt
            
            response = ollama.chat(
                model='llama2',  # or 'llama3' if you have it
                messages=[{
                    'role': 'user',
                    'content': full_prompt
                }]
            )
            return response['message']['content']
        except Exception as e:
            print(f"Ollama error: {e}")
            return f"⚠️ LLaMA model error: {str(e)}. Make sure Ollama is running with 'ollama serve' and you have pulled llama2 with 'ollama pull llama2'"
    
    # Fallback response
    return "I'm a demo assistant. To enable full AI capabilities, please install Ollama and run 'ollama pull llama2'."

# API Routes
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ollama": OLLAMA_AVAILABLE,
        "pinecone": PINECONE_AVAILABLE and pinecone_index is not None,
        "embeddings": EMBEDDINGS_AVAILABLE,
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
        
        # Get LLM response
        response = get_llm_response(request.message, full_context)
        
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
                doc_id = store_in_vector_db(
                    chunk,
                    {
                        'filename': file.filename,
                        'chunk': i,
                        'timestamp': datetime.now().isoformat()
                    }
                )
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
    return {
        "total_documents": len(knowledge_base),
        "vector_db_active": pinecone_index is not None,
        "embedding_model": "all-MiniLM-L6-v2" if embedding_model else None
    }

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 JARVIS AI Assistant Backend Server")
    print("="*60)
    print(f"✓ FastAPI server starting...")
    print(f"{'✓' if OLLAMA_AVAILABLE else '⚠️ '} Ollama: {'Available' if OLLAMA_AVAILABLE else 'Not installed'}")
    print(f"{'✓' if PINECONE_AVAILABLE else '⚠️ '} Pinecone: {'Available' if PINECONE_AVAILABLE else 'Not installed'}")
    print(f"{'✓' if EMBEDDINGS_AVAILABLE else '⚠️ '} Embeddings: {'Available' if EMBEDDINGS_AVAILABLE else 'Not installed'}")
    print("="*60)
    print("\n🚀 Server running at: http://localhost:8000")
    print("📚 API docs at: http://localhost:8000/docs\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
