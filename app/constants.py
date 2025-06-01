import os
# from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
# load_dotenv()


# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# SECRET_KEY = os.getenv("SECRET_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Define constants for file paths
SOURCE_PDF_FILE_PATH = r"data/report2.pdf"
VECTORDB_FILE_PATH = r"data/pdf-vectorstore"

# SOURCE_PDF_FILE_PATH =  r"data\report2.pdf"
# VECTORDB_FILE_PATH = r"data\pdf-vectorstore-fastemb"


