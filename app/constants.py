import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(r"../.env")

GEMINI_API_KEY = os.getenv("GEMINI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_KEY")

SOURCE_PDF_FILE_PATH =  r"data\report2.pdf"
VECTORDB_FILE_PATH = r"data\pdf-vectorstore"


