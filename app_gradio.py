import gradio as gr
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from simple.simple_vector_store import get_vector_store
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

# Global variables
vector_store = None
rag_chain = None

def initialize_rag(vector_store_type="FAISS"):
    """Initialize RAG chain"""
    global vector_store, rag_chain
    
    try:
        # Get vector store based on type
        if vector_store_type == "FAISS":
            from simple.simple_vector_store import get_vector_store
            vector_store = get_vector_store()
        else:
            from cosmosdb.cosmosdb_vector_store import get_vector_store as get_cosmos_vector_store
            vector_store = get_cosmos_vector_store()
        
        # Create retriever
        retriever = vector_store.as_retriever(
            k=int(os.getenv("TOP_K", 5)),  # Cosmos retriever reads k, FAISS reads search_kwargs
            search_kwargs={"k": int(os.getenv("TOP_K", 5))}
        )
        
        # Create prompt template
        from prompts import RAG_PROMPT_TEMPLATE
        prompt = PromptTemplate(template=RAG_PROMPT_TEMPLATE, input_variables=["context", "question"])
        
        # Create LLM
        llm = ChatOllama(model=os.getenv("CHAT_MODEL", "llama3"), num_ctx=int(os.getenv("NUM_CTX", "4096")))
        
        # Create simple chain
        class SimpleRAGChain:
            def __init__(self, retriever, llm, prompt):
                self.retriever = retriever
                self.llm = llm
                self.prompt = prompt
            
            def __call__(self, query):
                docs = self.retriever.invoke(query)
                context = "\n\n".join(doc.page_content for doc in docs)
                prompt_text = self.prompt.format(context=context, question=query)
                response = self.llm.invoke(prompt_text)
                answer = response.content if hasattr(response, 'content') else str(response)
                
                # Format sources
                sources_text = "\n\n📚 **Sources:**\n"
                for i, doc in enumerate(docs, 1):
                    sources_text += f"\n**Source {i}:**\n"
                    sources_text += doc.page_content[:200] + "...\n"
                    if doc.metadata:
                        sources_text += f"*Metadata: {doc.metadata}*\n"
                
                return answer + "\n\n" + sources_text
        
        rag_chain = SimpleRAGChain(retriever, llm, prompt)
        return "✅ RAG system initialized successfully!"
    
    except Exception as e:
        return f"❌ Error initializing RAG: {str(e)}"

def chat(message, history):
    """Process chat message"""
    global rag_chain
    
    if rag_chain is None:
        return "⚠️ Please initialize the RAG system first using the 'Initialize' button."
    
    try:
        response = rag_chain(message)
        return response
    except Exception as e:
        return f"❌ Error: {str(e)}"

def add_sample_question(question):
    """Return sample question to chat"""
    return question

# Create Gradio interface
with gr.Blocks(title="RAG Cosmos Ollama", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🤖 RAG Cosmos Ollama
    ### Retrieval-Augmented Generation with Local LLMs
    
    Ask questions about Azure Cosmos DB documentation using local Ollama models.
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            # Vector store selector
            vector_store_type = gr.Radio(
                choices=["FAISS", "Cosmos DB"],
                value="FAISS",
                label="Vector Store",
                info="Choose between local FAISS or Azure Cosmos DB"
            )
            
            # Chat interface
            chatbot = gr.Chatbot(
                label="Chat",
                height=500,
                show_copy_button=True
            )
            
            msg = gr.Textbox(
                label="Your Question",
                placeholder="Ask a question about the documents...",
                lines=2
            )
            
            with gr.Row():
                submit_btn = gr.Button("Send", variant="primary")
                clear_btn = gr.Button("Clear")
            
            # Sample questions
            gr.Markdown("### 💡 Sample Questions")
            with gr.Row():
                q1_btn = gr.Button("What is vector search?", size="sm")
                q2_btn = gr.Button("Vector embedding policy?", size="sm")
                q3_btn = gr.Button("Index types?", size="sm")
        
        with gr.Column(scale=1):
            # System info
            gr.Markdown("### ⚙️ Configuration")
            
            init_btn = gr.Button("🔄 Initialize RAG System", variant="secondary")
            init_status = gr.Textbox(label="Status", value="Not initialized", lines=2)
            
            gr.Markdown("### 📊 System Info")
            system_info = gr.Markdown(f"""
            - **Vector Store**: FAISS (Simple)
            - **Embeddings**: {os.getenv("EMBEDDINGS_MODEL", "mxbai-embed-large")}
            - **Chat Model**: {os.getenv("CHAT_MODEL", "llama3")}
            - **Top-K**: {os.getenv("TOP_K", "5")}
            """)
            
            gr.Markdown("### 📖 Links")
            gr.Markdown("[GitHub Repository](https://github.com/DuongCaoNhan/rag-cosmos-ollama)")
    
    # Event handlers
    def on_vector_store_change(vs_type):
        if vs_type == "FAISS":
            return "- **Vector Store**: FAISS (Simple)\n- **Embeddings**: " + os.getenv("EMBEDDINGS_MODEL", "mxbai-embed-large") + "\n- **Chat Model**: " + os.getenv("CHAT_MODEL", "llama3") + "\n- **Top-K**: " + os.getenv("TOP_K", "5")
        else:
            return "- **Vector Store**: Cosmos DB (Production)\n- **Embeddings**: " + os.getenv("EMBEDDINGS_MODEL", "mxbai-embed-large") + "\n- **Chat Model**: " + os.getenv("CHAT_MODEL", "llama3") + "\n- **Top-K**: " + os.getenv("TOP_K", "5")
    
    vector_store_type.change(on_vector_store_change, vector_store_type, system_info)
    
    init_btn.click(initialize_rag, inputs=vector_store_type, outputs=init_status)
    
    def respond(message, chat_history):
        bot_message = chat(message, chat_history)
        chat_history.append((message, bot_message))
        return "", chat_history
    
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit_btn.click(respond, [msg, chatbot], [msg, chatbot])
    clear_btn.click(lambda: None, None, chatbot, queue=False)
    
    # Sample question handlers
    q1_btn.click(lambda: "What is vector search in Cosmos DB?", None, msg)
    q2_btn.click(lambda: "Show me an example of a vector embedding policy", None, msg)
    q3_btn.click(lambda: "What are the different vector index types available?", None, msg)

if __name__ == "__main__":
    print("🚀 Starting RAG Cosmos Ollama with Gradio...")
    print("📝 Make sure Ollama is running: ollama serve")
    print("🔗 Opening browser at: http://localhost:7860")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
