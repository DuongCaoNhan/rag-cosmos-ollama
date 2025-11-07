import streamlit as st
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from simple.simple_vector_store import get_vector_store
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
def initialize_rag_chain(_vector_store_type, _chat_model, _top_k):
    """Initialize RAG chain with caching"""
    try:
        # Get vector store
        if _vector_store_type.startswith("FAISS"):
            vector_store = get_vector_store()
        else:
            # Import Cosmos DB vector store
            from cosmosdb.cosmosdb_vector_store import get_vector_store as get_cosmos_vector_store
            vector_store = get_cosmos_vector_store()
        
        # Create retriever
        retriever = vector_store.as_retriever(search_kwargs={"k": _top_k})
        
        # Create prompt template
        template = """You are a helpful AI assistant that answers questions based on the provided context.
Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Answer: """
        
        prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        
        # Create LLM
        llm = OllamaLLM(model=_chat_model)
        
        # Create RAG chain
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
        
        return chain
    except Exception as e:
        st.error(f"Error initializing RAG chain: {str(e)}")
        return None

# Initialize chain if not already done
if st.session_state.rag_chain is None:
    with st.spinner("🔄 Initializing RAG chain..."):
        st.session_state.rag_chain = initialize_rag_chain(
            vector_store_type,
            chat_model,
            top_k
        )
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

# Sample questions
st.markdown("**💡 Sample Questions:**")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("What is vector search?"):
        st.session_state.current_question = "What is vector search in Cosmos DB?"

with col2:
    if st.button("Vector embedding policy?"):
        st.session_state.current_question = "Show me an example of a vector embedding policy"

with col3:
    if st.button("Index types?"):
        st.session_state.current_question = "What are the different vector index types available?"

# Chat input
if prompt := st.chat_input("Ask a question about the documents..."):
    st.session_state.current_question = prompt

# Process question
if hasattr(st.session_state, 'current_question') and st.session_state.current_question:
    question = st.session_state.current_question
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(question)
    
    # Generate response
    if st.session_state.rag_chain:
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    result = st.session_state.rag_chain({"query": question})
                    answer = result["result"]
                    sources = result.get("source_documents", [])
                    
                    # Display answer
                    st.markdown(answer)
                    
                    # Display sources
                    if sources:
                        with st.expander("📚 Source Documents"):
                            for i, doc in enumerate(sources, 1):
                                st.markdown(f"**Source {i}:**")
                                st.text(doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content)
                                if doc.metadata:
                                    st.caption(f"Metadata: {doc.metadata}")
                                st.divider()
                    
                    # Add to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
    else:
        st.error("RAG chain not initialized. Please check your configuration.")
    
    # Clear current question
    delattr(st.session_state, 'current_question')
    st.rerun()

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    Built with ❤️ using Streamlit, Ollama, LangChain, and Azure Cosmos DB<br>
    <a href="https://github.com/DuongCaoNhan/rag-cosmos-ollama" target="_blank">View on GitHub</a>
</div>
""", unsafe_allow_html=True)
