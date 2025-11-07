import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from langchain_text_splitters import MarkdownTextSplitter
from langchain_community.document_loaders import WebBaseLoader
import simple_vector_store
import logging
from typing import List

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def load(urls: List[str], create_container: bool = True) -> None:
    """Load documents from URLs into simple vector store."""

    print("Loading documents from URLs:", urls)

    try:
        # Load documents from web
        loader = WebBaseLoader(urls)
        documents = loader.load()

        if not documents:
            raise ValueError("No documents were loaded from the provided URLs")

        # Split documents into chunks
        markdown_splitter = MarkdownTextSplitter(chunk_size=1500, chunk_overlap=200)
        split_docs = markdown_splitter.split_documents(documents)

        if not split_docs:
            raise ValueError("No document chunks were created after splitting")

        # Get vector store instance and add documents
        store = simple_vector_store.get_instance(create_container)
        
        # Clear existing dummy data and add real documents
        store.delete([store.index_to_docstore_id[0]])  # Remove dummy doc
        store.add_documents(split_docs)

        print(f"Successfully loaded {len(split_docs)} document chunks from {len(documents)} documents")
        print("Data loaded into in-memory vector store")
        
        # Save the store for later use
        store.save_local("./vector_store")
        print("Vector store saved to ./vector_store")

    except Exception as e:
        logger.error(f"Error during data loading: {str(e)}")
        raise


if __name__ == "__main__":
    doc_urls = [
        "https://raw.githubusercontent.com/MicrosoftDocs/azure-databases-docs/refs/heads/main/articles/cosmos-db/nosql/vector-search.md",
        "https://raw.githubusercontent.com/MicrosoftDocs/azure-databases-docs/refs/heads/main/articles/cosmos-db/nosql/multi-tenancy-vector-search.md",
    ]

    load(urls=doc_urls)