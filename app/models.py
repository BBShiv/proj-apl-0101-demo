from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from constants import OPENAI_API_KEY, GEMINI_API_KEY

import logging
import apl_logger
logger = logging.getLogger(__name__)

class OpenAIEmbeddingModel:
    def __init__(self):
        """
        Initializes the OpenAIEmbeddingModel.

        This model wraps the OpenAI embedding model using the langchain_openai package.
        """
        logger.info("Initializing OpenAIEmbeddingModel...")
        pass

    def load_embedding_model(self):
        """
        Loads the OpenAI embedding model.

        Returns:
            OpenAIEmbeddings: The loaded model.
        """
        logger.info("Loading OpenAIEmbeddingModel...")
        embedding_function = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
        
        logger.info("Done : OpenAIEmbeddingModel loaded...")
        return embedding_function
    

class OpenAILLMModel:
    def __init__(self):
        """
        Initializes the OpenAI model.

        This model wraps the OpenAI API using the langchain_openai package.
        """
        logger.info("Initializing OpenAILLMModel...")
        pass

    def load_model(self):
        
        """
        Loads the OpenAI model.

        Returns:
            ChatOpenAI: The loaded model.
        """
        logger.info("Loading OpenAILLMModel...")
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, temperature=0.1)
        
        logger.info("Done : OpenAILLMModel loaded...")

        return llm


class FastEmbeddingModel:
    def __init__(self):
        """
        Initializes the FastEmbedding.

        This model wraps the OpenAI embedding model using the langchain_openai package.
        """
        logger.info("Initializing FastEmbedding...")
        pass

    def load_embedding_model(self):
        """
        Loads the OpenAI embedding model.

        Returns:
            OpenAIEmbeddings: The loaded model.
        """
        logger.info("Loading FastEmbedding...")
        embedding_function = FastEmbedEmbeddings(model_name="BAAI/bge-large-en-v1.5")
        
        logger.info("Done : FastEmbedding loaded...")

        return embedding_function
    

class GeminiLLMModel:
    def __init__(self):
        """
        Initializes the GeminiLLMModel.

        This model wraps the Gemini API using the langchain_openai package.
        """
        logger.info("Initializing GeminiLLMModel...")
        pass

    def load_model(self):
        
        """
        Loads the OpenAI model.

        Returns:
            ChatOpenAI: The loaded model.
        """
        logger.info("Loading GeminiLLMModel...")
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
            temperature=1.0,
            api_key=GEMINI_API_KEY,
            timeout=None,
            max_retries=2,)
        
        logger.info("Done : GeminiLLMModel loaded...")

        return llm