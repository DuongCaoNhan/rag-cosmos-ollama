import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import cosmosdb_vector_store
import logging
import os

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def create_rag_chain():
    """Create a RAG chain with Cosmos DB vector store."""
    
    # Initialize the vector store
    vector_store = cosmosdb_vector_store.get_instance(create_container=False)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    
    # Initialize the LLM
    llm = Ollama(model=os.getenv("CHAT_MODEL", "llama3"))
    
    # Create a prompt template
    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum and keep the answer as concise as possible.

    Context:
    {context}

    Question: {question}

    Helpful Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Create the RAG chain
    rag_chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain


def _format_docs(docs):
    """Format retrieved documents for the prompt."""
    return "\n\n".join(doc.page_content for doc in docs)


def main():
    """Interactive chat with RAG chain."""
    
    try:
        print("Initializing RAG chain with Cosmos DB vector store...")
        rag_chain = create_rag_chain()
        print("RAG chain initialized successfully!")
        print("\nType 'exit' to quit, 'clear' to clear history")
        print("=" * 50)
        
        conversation_history = []
        
        while True:
            question = input("\nYour question: ").strip()
            
            if question.lower() == 'exit':
                print("Goodbye!")
                break
            elif question.lower() == 'clear':
                conversation_history.clear()
                print("Conversation history cleared.")
                continue
            elif question.lower() == 'history':
                if conversation_history:
                    print("\nConversation History:")
                    for i, (q, a) in enumerate(conversation_history, 1):
                        print(f"{i}. Q: {q}")
                        print(f"   A: {a}")
                else:
                    print("No conversation history.")
                continue
            elif not question:
                continue
            
            try:
                print("\nThinking...")
                answer = rag_chain.invoke(question)
                print(f"\nAnswer: {answer}")
                
                # Store in history
                conversation_history.append((question, answer))
                
            except Exception as e:
                logger.error(f"Error processing question: {str(e)}")
                print(f"Sorry, I encountered an error: {str(e)}")
                
    except Exception as e:
        logger.error(f"Error initializing RAG chain: {str(e)}")
        print(f"Failed to initialize RAG chain: {str(e)}")


if __name__ == "__main__":
    main()
