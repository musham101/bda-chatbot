
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import platform, os
from datetime import datetime

class Utils:
    def get_text_from_files(file_path):
        pdf_file_docs = PyPDFLoader(file_path).load()
        return pdf_file_docs
    
    # def split_text_to_chunks(docs):
    #     text_splitter = RecursiveCharacterTextSplitter(
    #         chunk_size=1000, chunk_overlap=20
    #     )
    #     doc_split = text_splitter.split_documents(docs)
    #     return doc_split
    
    def split_text_to_chunks(doc_text):
        text_splitter = RecursiveCharacterTextSplitter(separators="\n",chunk_size=400, chunk_overlap=20)
        doc_text_splits = text_splitter.split_documents(doc_text)
        for index, _ in enumerate(doc_text_splits):
            if platform.system() == "Windows":
                doc_text_splits[index].metadata["file_name"] = doc_text_splits[index].metadata["source"].split("/")[-1]
            else:
                doc_text_splits[index].metadata["file_name"] = doc_text_splits[index].metadata["source"].split("/")[-1]
            doc_text_splits[index].metadata["created_date"] = datetime.fromtimestamp(os.path.getctime(doc_text_splits[index].metadata["source"])).strftime('%Y-%m-%d %H:%M:%S')
            doc_text_splits[index].metadata["modified_date"] = datetime.fromtimestamp(os.path.getctime(doc_text_splits[index].metadata["source"])).strftime('%Y-%m-%d %H:%M:%S')
            doc_text_splits[index].page_content = f"""Document Content:\n{doc_text_splits[index].page_content}\n\nDoument Name:'{doc_text_splits[index].metadata["file_name"]}'"""
        return doc_text_splits