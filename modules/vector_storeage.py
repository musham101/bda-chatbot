from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
# from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.retrievers import ContextualCompressionRetriever

# Instantiate embeddings and compressor globally
embeddings = OllamaEmbeddings(model="llama3.1:latest")
# compressor = FlashrankRerank()

class VectorStorage:
    def load_vectorstore(persist_directory="vector_store"):
        """
        Loads a persisted vector store from the given directory.

        Parameters:
        - persist_directory (str, optional): Directory path where the vector store is saved. Defaults to "vector_store".

        Returns:
        - Chroma: An instance of the Chroma vector store loaded with the given embeddings.
        """
        vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory=persist_directory,
        )
        return vector_store

    def insert_chunks_to_vectordb(doc_text_splits, persist_directory="vector_store"):
        """
        Inserts document chunks into the vector store in batches.

        Parameters:
        - doc_text_splits (List[Document]): A list of Document objects (chunks) to be inserted into the vector database.
        - persist_directory (str, optional): Directory where the vector store persists. Defaults to "vector_store".

        Returns:
        - Chroma: The updated Chroma vector store after inserting all document chunks.

        Notes:
        - Documents are inserted in batches of 10 for better performance.
        - Prints a message after each batch insertion.
        """
        vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory=persist_directory,
        )
        chunk_size = 10
        for i in range(0, len(doc_text_splits), chunk_size):
            chunk = doc_text_splits[i:i + chunk_size]
            vector_store.add_documents(documents=chunk)
            print(f"- Inserted {len(chunk)} documents to vectorstore...")
        return vector_store
    
    # def get_rerank_retriever(retriever):
    #     """
    #     Creates a reranking retriever using a compressor over an existing retriever.

    #     Parameters:
    #     - retriever (BaseRetriever): A retriever object that fetches initial documents.

    #     Returns:
    #     - ContextualCompressionRetriever: A retriever that reranks documents after initial retrieval using FlashrankRerank.

    #     Notes:
    #     - The reranker improves the relevance of the retrieved documents based on context.
    #     """
    #     compressor = FlashrankRerank()
    #     compression_retriever = ContextualCompressionRetriever(
    #         base_compressor=compressor,
    #         base_retriever=retriever
    #     )
    #     return compression_retriever

    # def insert_docs_to_vectordb(all_splits):
    #     """
    #     Inserts all document splits directly into a new vector store and prepares a retriever with MMR search strategy.
    #     
    #     Parameters:
    #     - all_splits (List[Document]): All document chunks to be inserted into a new Chroma vector store.
    #     
    #     Returns:
    #     - Retriever: A retriever object based on the new vector store with search_type="mmr" and custom search parameters.
    #     """
    #     vectorstore = Chroma.from_documents(documents=all_splits, embedding=embeddings)
    #     retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 5, 'fetch_k': 50})
    #     return retriever
