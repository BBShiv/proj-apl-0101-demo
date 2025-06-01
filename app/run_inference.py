from create_vector_db import CreateAndLoadVectorDB
from models import OpenAILLMModel,GeminiLLMModel
from constants import VECTORDB_FILE_PATH

class RunInference:
    def __init__(self):
        self.vectors = CreateAndLoadVectorDB()
        # self.llm = OpenAILLMModel()
        self.llm = GeminiLLMModel()

    def retrieve_context(self, query, vector_db_path):
        
        loaded_vectordb = self.vectors.load_vector_db(vector_db_path)
        retrieved_docs = self.vectors.query_vector_db(loaded_vectordb, query, top_k=5)
        return retrieved_docs

    def format_docs(self, retrieved_docs): 
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    def create_prompt(self, context, query):

        template = f""" 
        Answer the question based only on the following context: {context}
        Question: {query}
        Only respond from the context, don't make things up, if you don't know just \
            say I don't know.
        """
        return template,context

    def run_inference(self, query):
        retrieved_docs = self.retrieve_context(query,VECTORDB_FILE_PATH)
        context = self.format_docs(retrieved_docs)
        prompt,context = self.create_prompt(context, query)
        
        llm = self.llm.load_model()
        response = llm.invoke(prompt)
        generated_output = response.content
        return generated_output,context
