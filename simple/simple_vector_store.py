from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
import os
import logging

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def get_embeddings_model_name():
    """Get embeddings model name from environment"""
    embeddings_model_name = os.getenv("EMBEDDINGS_MODEL", "mxbai-embed-large")
    return embeddings_model_name

def get_instance(create_container: bool = False):
    """Get a FAISS vector store instance for testing purposes."""
    embeddings_model_name = get_embeddings_model_name()
    logger.info(f"Using FAISS in-memory vector store with embedding model: {embeddings_model_name}")

    try:
        embeddings = OllamaEmbeddings(model=embeddings_model_name)
        
        # Create a simple FAISS store with dummy documents for initialization
        from langchain_core.documents import Document
        dummy_docs = [Document(page_content="dummy", metadata={"source": "test"})]
        store = FAISS.from_documents(dummy_docs, embeddings)
        
        logger.info("Successfully created FAISS vector store instance")
        return store

    except Exception as e:
        logger.error(f"Failed to create FAISS vector store instance: {str(e)}")
        raise

def get_vector_store():
    """Load existing FAISS vector store from disk"""
    embeddings_model_name = get_embeddings_model_name()
    vector_store_path = "./vector_store"
    
    if not os.path.exists(vector_store_path):
        raise FileNotFoundError(
            f"Vector store not found at {vector_store_path}. "
            "Please run 'python simple/simple_load_data.py' first to create the vector store."
        )
    
    try:
        embeddings = OllamaEmbeddings(model=embeddings_model_name)
        vector_store = FAISS.load_local(
            vector_store_path,
            embeddings,
            allow_dangerous_deserialization=True
        )
        logger.info(f"Successfully loaded FAISS vector store from {vector_store_path}")
        return vector_store
    except Exception as e:
        logger.error(f"Failed to load FAISS vector store: {str(e)}")
        raise