import streamlit as st
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables FIRST before any other imports
load_dotenv()

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from simple.simple_vector_store import get_vector_store
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Page config
st.set_page_config(
    page_title="RAG Cosmos Ollama - Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #667eea;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .source-box {
        background-color: #e7f3ff;
        border-left: 4px solid #0066cc;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
    /* Error messages only */
    .stAlert, .stException {
        background-color: #ffebee !important;
        color: #d32f2f !important;
        border: 2px solid #f44336 !important;
        padding: 1rem !important;
    }
    
    /* Force text color in chat messages */
    .stChatMessage {
        color: #1a1a1a !important;
    }
    
    .stChatMessage p, .stChatMessage div, .stChatMessage span {
        color: #1a1a1a !important;
    }
    
    /* User messages - Blue background */
    .stChatMessage[data-testid="user-message"] {
        background-color: #e3f2fd !important;
        border-left: 4px solid #2196f3 !important;
        padding: 1rem !important;
    }
    
    /* Assistant messages - White background with border */
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #ffffff !important;
        border-left: 4px solid #4caf50 !important;
        padding: 1rem !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    /* Fix code blocks - better contrast */
    .stChatMessage pre, .stChatMessage code {
        background-color: #1e1e1e !important;
        color: #d4d4d4 !important;
        border: 1px solid #444 !important;
    }
    
    /* Code block syntax highlighting */
    .stChatMessage pre code {
        color: #d4d4d4 !important;
    }
    
    /* Inline code */
    .stChatMessage code {
        background-color: #2d2d2d !important;
        color: #e6db74 !important;
        padding: 2px 6px !important;
        border-radius: 3px !important;
    }
    
    /* Chat input */
    .stChatInput textarea {
        color: #000 !important;
        background-color: #fff !important;
    }
    
    /* Remove red styling from normal content */
    .element-container .stMarkdown {
        background-color: transparent !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🤖 RAG Cosmos Ollama</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Retrieval-Augmented Generation with Local LLMs</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Vector store selection
    vector_store_type = st.selectbox(
        "Vector Store",
        ["FAISS (Simple)", "Cosmos DB (Production)"],
        help="Choose between local FAISS or Azure Cosmos DB"
    )
    
    # Model settings
    st.subheader("🧠 Model Settings")
    embeddings_model = st.text_input(
        "Embeddings Model",
        value=os.getenv("EMBEDDINGS_MODEL", "mxbai-embed-large"),
        help="Ollama embedding model"
    )
    
    chat_model = st.text_input(
        "Chat Model",
        value=os.getenv("CHAT_MODEL", "llama3"),
        help="Ollama chat model"
    )
    
    top_k = st.slider(
        "Top K Results",
        min_value=1,
        max_value=10,
        value=int(os.getenv("TOP_K", 5)),
        help="Number of documents to retrieve"
    )
    
    st.divider()
    
    # System info
    st.subheader("📊 System Info")
    st.info(f"**Vector Store**: {vector_store_type.split()[0]}")
    st.info(f"**Embeddings**: {embeddings_model}")
    st.info(f"**Chat Model**: {chat_model}")
    st.info(f"**Top-K**: {top_k}")
    
    st.divider()
    
    # Quick actions
    if st.button("🔄 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("📖 View Documentation"):
        st.markdown("[GitHub Repository](https://github.com/DuongCaoNhan/rag-cosmos-ollama)")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

# Initialize RAG chain
@st.cache_resource
def initialize_rag_chain(vector_store_type, chat_model, top_k):
    """Initialize RAG chain with caching (exceptions are not cached, so failures can be retried)"""
    # Get vector store
    if vector_store_type.startswith("FAISS"):
        vector_store = get_vector_store()
    else:
        # Import Cosmos DB vector store
        from cosmosdb.cosmosdb_vector_store import get_vector_store as get_cosmos_vector_store
        vector_store = get_cosmos_vector_store()

    # Create retriever
    retriever = vector_store.as_retriever(k=top_k, search_kwargs={"k": top_k})  # Cosmos retriever reads k, FAISS reads search_kwargs

    # Create prompt template
    template = """You are a helpful AI assistant that answers questions based on the provided context.
Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Answer: """

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    # Create LLM
    llm = ChatOllama(model=chat_model, num_ctx=int(os.getenv("NUM_CTX", "4096")))

    # Create simple chain
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Simple retrieval chain
    class SimpleRAGChain:
        def __init__(self, retriever, llm, prompt):
            self.retriever = retriever
            self.llm = llm
            self.prompt = prompt

        def __call__(self, inputs):
            query = inputs.get("query", "")
            docs = self.retriever.invoke(query)  # Changed from get_relevant_documents to invoke
            context = format_docs(docs)
            prompt_text = self.prompt.format(context=context, question=query)
            response = self.llm.invoke(prompt_text)
            return {
                "result": response.content if hasattr(response, 'content') else str(response),
                "source_documents": docs
            }

    chain = SimpleRAGChain(retriever, llm, prompt)

    return chain

# Initialize chain if not already done or if settings changed
current_config = f"{vector_store_type}_{chat_model}_{top_k}"
if "last_config" not in st.session_state:
    st.session_state.last_config = None

if st.session_state.rag_chain is None or st.session_state.last_config != current_config:
    with st.spinner("🔄 Initializing RAG chain..."):
        try:
            st.session_state.rag_chain = initialize_rag_chain(
                vector_store_type,
                chat_model,
                top_k
            )
        except Exception as e:
            st.session_state.rag_chain = None
            st.error(f"Error initializing RAG chain: {str(e)}")
        st.session_state.last_config = current_config
        if st.session_state.rag_chain:
            st.success("✅ RAG chain initialized successfully!")

# Main chat interface
st.subheader("💬 Chat Interface")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📚 Source Documents"):
                for i, doc in enumerate(message["sources"], 1):
                    st.markdown(f"**Source {i}:**")
                    st.text(doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content)
                    if doc.metadata:
                        st.caption(f"Metadata: {doc.metadata}")
                    st.divider()

# Only show sample questions if not currently processing
if not hasattr(st.session_state, 'current_question'):
    # Sample questions
    st.markdown("**💡 Sample Questions:**")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("What is vector search?"):
            st.session_state.current_question = "What is vector search in Cosmos DB?"
            st.rerun()

    with col2:
        if st.button("Vector embedding policy?"):
            st.session_state.current_question = "Show me an example of a vector embedding policy"
            st.rerun()

    with col3:
        if st.button("Index types?"):
            st.session_state.current_question = "What are the different vector index types available?"
            st.rerun()

# Chat input
if prompt := st.chat_input("Ask a question about the documents..."):
    st.session_state.current_question = prompt
    st.rerun()

# Process question (only if not already processed)
if hasattr(st.session_state, 'current_question') and st.session_state.current_question:
    question = st.session_state.current_question
    
    # Check if this question is already in messages (avoid duplicate processing)
    if not st.session_state.messages or st.session_state.messages[-1].get("content") != question:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Generate response
        if st.session_state.rag_chain:
            try:
                result = st.session_state.rag_chain({"query": question})
                answer = result["result"]
                sources = result.get("source_documents", [])
                
                # Add to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
                
            except Exception as e:
                import traceback
                error_msg = f"Error: {str(e)}"
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "RAG chain not initialized. Please check your configuration."
            })
    
    # Clear current question and rerun to display
    del st.session_state.current_question
    st.rerun()

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    Built with ❤️ using Streamlit, Ollama, LangChain, and Azure Cosmos DB<br>
    <a href="https://github.com/DuongCaoNhan/rag-cosmos-ollama" target="_blank">View on GitHub</a>
</div>
""", unsafe_allow_html=True)
