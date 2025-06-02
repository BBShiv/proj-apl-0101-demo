from create_vector_db import CreateAndLoadVectorDB
from models import OpenAILLMModel,GeminiLLMModel
from constants import VECTORDB_FILE_PATH
import logging
import apl_logger

logger = logging.getLogger(__name__)

class RunInference:
    def __init__(self):
        logger.info("Initializing RunInference...")
        self.vectors = CreateAndLoadVectorDB()
        self.llm = OpenAILLMModel()
        #self.llm = GeminiLLMModel()
        logger.info("Done : RunInference initialized...")

    def retrieve_context(self, query, vector_db_path):
        logger.info("Retrieving context...")
        loaded_vectordb = self.vectors.load_vector_db(vector_db_path)
        retrieved_docs = self.vectors.query_vector_db(loaded_vectordb, query, top_k=5)
        
        logger.info("Done : Context retrieved...")

        return retrieved_docs

    def format_docs(self, retrieved_docs):
        logger.info("Formatting docs...")

        if not retrieved_docs:
            return "No relevant documents found."

        logger.info("Done : Docs formatted...")
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    def create_prompt(self, context, query):
        logger.info("Creating prompt...")
        template = f""" 
        Answer the question based only on the following context: {context}
        Question: {query}
        Only respond from the context, don't make things up, if you don't know just \
            say I don't know.
        """

        logger.info("Done : Prompt created...")
        return template,context

    def run_inference(self, query):
        logger.info("Running inference...")
        retrieved_docs = self.retrieve_context(query,VECTORDB_FILE_PATH)
        context = self.format_docs(retrieved_docs)
        prompt,context = self.create_prompt(context, query)
        
        llm = self.llm.load_model()
        response = llm.invoke(prompt)
        generated_output = response.content

        logger.info("Done : Inference completed...")
        return generated_output,context
