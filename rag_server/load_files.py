# load_files.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader

def load_documents(dir_path):
    loader = DirectoryLoader(dir_path, glob="**/*.pdf", loader_cls=PyMuPDFLoader, show_progress=True)
    repo_files = loader.load()
    print(f"Number of files loaded: {len(repo_files)}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
    documents = text_splitter.split_documents(repo_files)
    print(f"Number of documents: {len(documents)}")

    return documents
