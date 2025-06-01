from langchain_community.document_loaders import PyPDFLoader,PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import OpenAIEmbeddingModel, FastEmbeddingModel
from constants import SOURCE_PDF_FILE_PATH, VECTORDB_FILE_PATH

class CreateAndLoadVectorDB:

    def __init__(self):
        # self.embeddings = OpenAIEmbeddingModel()
        self.embeddings = FastEmbeddingModel()

    def load_pdf_file(self, pdf_file_path):
        loader = PyMuPDFLoader(pdf_file_path)
        documents = loader.load()
        return documents

    def chunk_documents(self, documents, chunk_size=1000, chunk_overlap=20):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents(documents)
        return chunks

    def create_vector_db(self, chunks, embeddings):
        vector_db = FAISS.from_documents(chunks, embeddings)
        return vector_db

    def save_vector_db(self, vector_db, vector_db_path):
        vector_db.save_local(vector_db_path)

    def create_and_save_vector_db(self, pdf_file_path, vector_db_path, chunk_size=1000, chunk_overlap=20):
        
        pdf_file_path = SOURCE_PDF_FILE_PATH
        vector_db_path = VECTORDB_FILE_PATH
        documents = self.load_pdf_file(pdf_file_path)
        chunks = self.chunk_documents(documents, chunk_size, chunk_overlap)
        embeddings = self.embeddings.load_embedding_model()
        vector_db = self.create_vector_db(chunks, embeddings)
        self.save_vector_db(vector_db, vector_db_path)
        return vector_db

    def load_vector_db(self, vector_db_path):
        embeddings = self.embeddings.load_embedding_model()
        vector_db = FAISS.load_local(vector_db_path, embeddings, allow_dangerous_deserialization=True)
        return vector_db

    def query_vector_db(self, vector_db, query, top_k=5):
        # vector_db = self.load_vector_db(vector_db_path)
        docs = vector_db.similarity_search(query)
        return docs


    
    