from langchain_community.document_loaders import PyPDFLoader,PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import OpenAIEmbeddingModel, FastEmbeddingModel
from constants import SOURCE_PDF_FILE_PATH, VECTORDB_FILE_PATH
import logging
import apl_logger
logger = logging.getLogger(__name__)

class CreateAndLoadVectorDB:

    def __init__(self):
        logger.info("Initializing CreateAndLoadVectorDB...")
        self.embeddings = OpenAIEmbeddingModel()
        #self.embeddings = FastEmbeddingModel()
        logger.info("Done : CreateAndLoadVectorDB initialized...")

    def load_pdf_file(self, pdf_file_path):
        logger.info("Loading PDF file...")
        loader = PyMuPDFLoader(pdf_file_path)
        documents = loader.load()
        logger.info("Done : PDF file loaded...")
        return documents

    def chunk_documents(self, documents, chunk_size=1000, chunk_overlap=20):
        logger.info("Chunking documents...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents(documents)
        logger.info("Done : Documents chunked...")
        return chunks

    def create_vector_db(self, chunks, embeddings):
        logger.info("Creating vector database...")
        vector_db = FAISS.from_documents(chunks, embeddings)
        logger.info("Done : Vector database created...")
        return vector_db

    def save_vector_db(self, vector_db, vector_db_path):
        logger.info("Saving vector database...")
        vector_db.save_local(vector_db_path)
        logger.info("Done : Vector database saved...")

    def create_and_save_vector_db(self, pdf_file_path, vector_db_path, chunk_size=1000, chunk_overlap=20):
        logger.info("Creating and saving vector database...")
        pdf_file_path = SOURCE_PDF_FILE_PATH
        vector_db_path = VECTORDB_FILE_PATH
        documents = self.load_pdf_file(pdf_file_path)
        chunks = self.chunk_documents(documents, chunk_size, chunk_overlap)
        embeddings = self.embeddings.load_embedding_model()
        vector_db = self.create_vector_db(chunks, embeddings)
        self.save_vector_db(vector_db, vector_db_path)
        logger.info("Done : Vector database created and saved...")
        return vector_db

    def load_vector_db(self, vector_db_path):
        logger.info("Loading vector database...")
        embeddings = self.embeddings.load_embedding_model()
        vector_db = FAISS.load_local(vector_db_path, embeddings, allow_dangerous_deserialization=True)
        logger.info("Done : Vector database loaded...")
        return vector_db

    def query_vector_db(self, vector_db, query, top_k=5):
        logger.info("Querying vector database...")
        # vector_db = self.load_vector_db(vector_db_path)
        docs = vector_db.similarity_search(query)
        logger.info("Done : Vector database queried...")
        return docs


    
    