from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import platform
import os, shutil, base64
from datetime import datetime

class Utils:
    def file_to_base64(file_path):
        """
        Converts a file to a Base64-encoded string.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Base64-encoded string of the file contents.
        """
        with open(file_path, 'rb') as file:
            encoded_string = base64.b64encode(file.read()).decode('utf-8')
        return encoded_string
    
    def delete_folder(folder_path):
        """
        Deletes a folder and all its contents.

        Args:
            folder_path (str): The path to the folder to delete.
        """
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' deleted successfully.")
        else:
            print(f"Folder '{folder_path}' does not exist.")

    def get_text_from_files(file_path):
        """
        Loads text content from a PDF file and returns a list of documents.

        Parameters:
        - file_path (str): The full path to the PDF file to be loaded.

        Returns:
        - List[Document]: A list of Document objects, each representing a portion of the PDF content.
        
        Notes:
        - Uses the PyPDFLoader from langchain_community to extract content.
        """
        pdf_file_docs = PyPDFLoader(file_path).load()
        return pdf_file_docs
    
    def split_text_to_chunks(doc_text):
        """
        Splits documents into smaller chunks for easier processing.

        Parameters:
        - doc_text (List[Document]): A list of Document objects to be split.

        Returns:
        - List[Document]: A list of smaller Document chunks with updated metadata including:
            - 'file_name': The file name extracted from the source path.
            - 'created_date': The file creation timestamp (formatted as 'YYYY-MM-DD HH:MM:SS').
            - 'modified_date': The file modification timestamp (formatted as 'YYYY-MM-DD HH:MM:SS').

        Notes:
        - Chunking is based on line breaks ('\\n') with a chunk size of 400 characters and 20 characters overlap.
        - Platform-specific path handling (Windows/Linux/Mac) is included to correctly extract file names.
        - Adds document metadata and modifies page content by embedding the document name.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            separators="\n", chunk_size=400, chunk_overlap=20
        )
        doc_text_splits = text_splitter.split_documents(doc_text)
        
        for index, _ in enumerate(doc_text_splits):
            if platform.system() == "Windows":
                doc_text_splits[index].metadata["file_name"] = doc_text_splits[index].metadata["source"].split("/")[-1]
            else:
                doc_text_splits[index].metadata["file_name"] = doc_text_splits[index].metadata["source"].split("/")[-1]
            
            doc_text_splits[index].metadata["created_date"] = datetime.fromtimestamp(
                os.path.getctime(doc_text_splits[index].metadata["source"])
            ).strftime('%Y-%m-%d %H:%M:%S')
            
            doc_text_splits[index].metadata["modified_date"] = datetime.fromtimestamp(
                os.path.getctime(doc_text_splits[index].metadata["source"])
            ).strftime('%Y-%m-%d %H:%M:%S')
            
            doc_text_splits[index].page_content = f"""Document Content:\n{doc_text_splits[index].page_content}\n\nDocument Name:'{doc_text_splits[index].metadata["file_name"]}'"""
        
        return doc_text_splits
