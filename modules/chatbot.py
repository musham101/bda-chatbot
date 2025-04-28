from langchain_ollama import OllamaLLM

# Instantiate the LLM with the model "llama3.1:latest"
llm = OllamaLLM(model="llama3.1:latest")

class Chatbot:
    def format_docs(docs):
        """
        Formats a list of documents into a single string.

        Parameters:
        - docs (List[Document]): A list of Document objects, each containing page_content.

        Returns:
        - str: A single string with each document's content separated by three newline characters.
        """
        return "\n\n\n".join(
            f"{doc.page_content}"
            for doc in docs
        )
    
    def simple_response(user_query):
        """
        Generates a simple direct response to the user's query using the LLM.

        Parameters:
        - user_query (str): The input question or prompt from the user.

        Returns:
        - str: The generated response from the LLM.
        """
        return llm.invoke(user_query)
    
    def rag_response(retriever, user_query):
        """
        Generates a RAG (Retrieval-Augmented Generation) response using a retriever and the LLM.

        Parameters:
        - retriever (BaseRetriever): A retriever object used to fetch relevant documents for the query.
        - user_query (str): The input question or prompt from the user.

        Returns:
        - Tuple[str, str]: A tuple containing:
            1. The generated response from the LLM based on the retrieved documents.
            2. The formatted string of the retrieved documents used in the prompt.
        
        Notes:
        - The final response also refers to the file paths of the documents at the end, as instructed in the prompt template.
        """
        prompt_template = """given some data, i want you to answer the user query.
documents:
{context}

user query:
{question}

make sure to refer to the files path you used at the end of your response.
"""

        # Retrieve relevant documents based on the user query
        relevant_docs = retriever.invoke(user_query)

        # Format the retrieved documents into a single string
        relevant_docs = Chatbot.format_docs(relevant_docs)

        # Generate and return the response using the formatted context and user query
        return llm.invoke(prompt_template.format(context=relevant_docs, question=user_query)), relevant_docs
