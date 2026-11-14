"""Common prompts used across the application"""

RAG_PROMPT_TEMPLATE = """You are a helpful AI assistant that answers questions about Azure Cosmos DB based on the provided context.
Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know.

Context:
{context}

Question: {question}

Answer: """