from langchain_ollama import ChatOllama
import simple_vector_store
import os
import logging
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Validate required environment variables
required_env_vars = ["CHAT_MODEL"]
missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
if missing_vars:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )

chat_model = os.environ["CHAT_MODEL"]
# Get top_k from environment variable with default
top_k = int(os.environ.get("TOP_K", "5"))

# Simple chat history storage
chat_history: List[Dict[str, str]] = []


def format_chat_history(history: List[Dict[str, str]], max_turns: int = 5) -> str:
    if not history:
        return "No previous conversation."

    # Keep only the last max_turns conversations
    recent_history = history[-max_turns:]

    formatted = []
    for turn in recent_history:
        formatted.append(f"Human: {turn['human']}")
        formatted.append(f"Assistant: {turn['assistant']}")

    return "\n".join(formatted)


def add_to_history(human_message: str, assistant_message: str) -> None:
    """Add conversation to history."""
    chat_history.append({"human": human_message, "assistant": assistant_message})


def clear_history() -> None:
    """Clear chat history."""
    global chat_history
    chat_history = []


def answer_question(query: str) -> str:
    """Answer a question using RAG."""
    try:
        # Load the saved vector store
        from langchain_ollama import OllamaEmbeddings
        from langchain_community.vectorstores import FAISS
        embeddings = OllamaEmbeddings(model=os.environ["EMBEDDINGS_MODEL"])
        store = FAISS.load_local("./vector_store", embeddings, allow_dangerous_deserialization=True)
        
        # Get relevant documents
        docs = store.similarity_search(query, k=top_k)
        
        # Combine context
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Format chat history
        history = format_chat_history(chat_history)
        
        # Create prompt
        prompt = f"""You are a friendly assistant for question-answering tasks. Use the following retrieved context to answer the question. 
Do not start the answer with 'According to the provided context'. 
Consider the previous conversation when relevant, but ensure your answer is primarily based on the retrieved context. 
If the answer is not present in the provided context, just say so. Ensure that the answer is strictly based on the context given, 
without inferring or making assumptions. Be helpful but concise. Do not be rude. While answering, you don't need to repeat that 
you are answering based on the context.

Previous conversation:
{history}

Retrieved context:
{context}

Question: {query}

Answer:"""

        # Use LLM to generate answer
        llm = ChatOllama(model=chat_model)
        response = llm.invoke(prompt)
        
        return response.content if hasattr(response, 'content') else str(response)
        
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"


if __name__ == "__main__":
    try:
        print(f"Starting RAG chat application. Using model: {chat_model}")
        print(f"Vector search with k={top_k}")
        print("Enter your questions below. Type 'exit' to quit, 'clear' to clear chat history, 'history' to view chat history.")

        while True:
            try:
                query = input("[User]: ").strip()
                if query.lower() == "exit":
                    break
                elif query.lower() == "clear":
                    clear_history()
                    print("Chat history cleared.")
                    continue
                elif query.lower() == "history":
                    if chat_history:
                        print("\n--- Chat History ---")
                        for i, turn in enumerate(chat_history, 1):
                            print(f"{i}. [User]: {turn['human']}")
                            print(f"{i}. [Assistant]: {turn['assistant']}")
                        print("--- End History ---\n")
                    else:
                        print("No chat history available.\n")
                    continue
                elif not query:
                    continue

                print("[Assistant]: ", end="", flush=True)
                
                # Get answer using RAG
                response = answer_question(query)
                print(response)

                # Add this conversation to history
                add_to_history(query, response)

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                logger.error(f"Error during conversation: {str(e)}")
                print(f"Sorry, an error occurred: {str(e)}")

    except Exception as e:
        logger.error(f"Failed to start RAG application: {str(e)}")
        print(f"Failed to start application: {str(e)}")
        exit(1)