from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from typing import List, Optional

load_dotenv()

# Lazy imports after env load
from simple.simple_vector_store import get_vector_store as get_faiss_store

app = FastAPI(title="RAG Cosmos Ollama API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InitRequest(BaseModel):
    vector_store: str = "FAISS"  # or COSMOS
    top_k: int = int(os.getenv("TOP_K", 5))
    chat_model: Optional[str] = os.getenv("CHAT_MODEL", "llama3")

class ChatRequest(BaseModel):
    query: str

class SourceChunk(BaseModel):
    content: str
    metadata: dict

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]

# Globals
rag_chain = None
current_config = {}

def build_chain(vs_type: str, top_k: int, chat_model: str):
    if vs_type.upper().startswith("FAISS"):
        vector_store = get_faiss_store()
    else:
        try:
            from cosmosdb.cosmosdb_vector_store import get_vector_store as get_cosmos_store
            vector_store = get_cosmos_store()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Cosmos DB init failed: {e}")

    retriever = vector_store.as_retriever(k=top_k, search_kwargs={"k": top_k})  # Cosmos retriever reads k, FAISS reads search_kwargs

    from langchain_core.prompts import PromptTemplate
    from langchain_ollama import ChatOllama

    template = (
        "You are a helpful AI assistant that answers questions about Azure Cosmos DB based on the provided context.\n"
        "If you don't know the answer, say you don't know.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    )
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    llm = ChatOllama(model=chat_model or os.getenv("CHAT_MODEL", "llama3"), num_ctx=int(os.getenv("NUM_CTX", "4096")))

    def format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)

    class SimpleRAGChain:
        def __init__(self, retriever, llm, prompt):
            self.retriever = retriever
            self.llm = llm
            self.prompt = prompt
        def run(self, query: str):
            docs = self.retriever.invoke(query)
            ctx = format_docs(docs)
            ptxt = self.prompt.format(context=ctx, question=query)
            resp = self.llm.invoke(ptxt)
            answer = resp.content if hasattr(resp, 'content') else str(resp)
            return answer, docs

    return SimpleRAGChain(retriever, llm, prompt)

@app.post("/init")
def init_chain(req: InitRequest):
    global rag_chain, current_config
    try:
        chat_model = req.chat_model or os.getenv("CHAT_MODEL", "llama3")
        rag_chain = build_chain(req.vector_store, req.top_k, chat_model)
        current_config = {
            "vector_store": req.vector_store,
            "top_k": req.top_k,
            "chat_model": chat_model,
        }
        return {"status": "ok", "config": current_config}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if rag_chain is None:
        raise HTTPException(status_code=400, detail="RAG chain not initialized. Call /init first.")
    try:
        answer, docs = rag_chain.run(req.query)
        sources = [SourceChunk(content=d.page_content[:500], metadata=d.metadata or {}) for d in docs]
        return ChatResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok", "initialized": rag_chain is not None, "config": current_config}

# Serve the WebUI at http://localhost:8000/ (mounted last so API routes take precedence)
app.mount("/", StaticFiles(directory=str(Path(__file__).parent / "webui"), html=True), name="webui")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
