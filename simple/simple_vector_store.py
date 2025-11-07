from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
import os
import logging

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Validate required environment variables
required_env_vars = ["EMBEDDINGS_MODEL"]
missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
if missing_vars:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )

embeddings_model_name = os.environ["EMBEDDINGS_MODEL"]

def get_instance(create_container: bool = False):
    """Get a FAISS vector store instance for testing purposes."""
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