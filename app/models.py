from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from constants import OPENAI_API_KEY

class OpenAIEmbeddingModel:
    def __init__(self):
        """
        Initializes the OpenAIEmbeddingModel.

        This model wraps the OpenAI embedding model using the langchain_openai package.
        """
        pass

    def load_embedding_model(self):
        """
        Loads the OpenAI embedding model.

        Returns:
            OpenAIEmbeddings: The loaded model.
        """

        embedding_function = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
        return embedding_function

class OpenAILLMModel:
    def __init__(self):
        """
        Initializes the OpenAI model.

        This model wraps the OpenAI API using the langchain_openai package.
        """
        pass

    def load_model(self):
        
        """
        Loads the OpenAI model.

        Returns:
            ChatOpenAI: The loaded model.
        """

        llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY, temperature=0.1)
        return llm
