from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.retrievers import ContextualCompressionRetriever

embeddings = OllamaEmbeddings(model="llama3.1:latest")
compressor = FlashrankRerank()

class VectorStorage:
    def load_vectorstore(persist_directory="vector_store"):
        vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory=persist_directory,
        )
        return vector_store

    def insert_chunks_to_vectordb(doc_text_splits, persist_directory="vector_store"):
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
    
    def get_rerank_retriever(retriever):
        compressor = FlashrankRerank()
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=retriever
        )
        return compression_retriever
    


    # def insert_docs_to_vectordb(all_splits):
    #     vectorstore = Chroma.from_documents(documents=all_splits, embedding=embeddings)
    #     retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 5, 'fetch_k': 50})
    #     return retriever