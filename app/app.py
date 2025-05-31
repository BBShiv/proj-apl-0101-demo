from flask import Flask, request, jsonify
import random
import math
from create_vector_db import CreateAndLoadVectorDB
from run_inference import RunInference
from constants import SOURCE_PDF_FILE_PATH, VECTORDB_FILE_PATH

app = Flask(__name__)


@app.route('/create_vector_db', methods=['GET'])
def create_vector_db_endpoint():
    """
    Endpoint to create and save vector database.
    """

    pdf_file_path = SOURCE_PDF_FILE_PATH
    vector_db_path = VECTORDB_FILE_PATH
    vectors = CreateAndLoadVectorDB()
    vector_db = vectors.create_and_save_vector_db(pdf_file_path, vector_db_path, chunk_size=1000, chunk_overlap=20)

    return jsonify({
        "message": "Vector Database created successfully.",
    }), 200


@app.route('/inference', methods=['POST'])
def run_inference_endpoint():
    """
    Endpoint to run inference.
    Expects JSON input: {"query": "Your question or query text here"}
    Returns the response from LLM.
    """
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    query_text = data['query']

    inference = RunInference()
    response_output = inference.run_inference(query_text)
    
    # Return the top_k results
    return jsonify({
        "query": query_text,
        "results": response_output
    }), 200

if __name__ == '__main__':
    # Run the Flask application
    # In a production environment, you would use a WSGI server like Gunicorn or uWSGI
    app.run(debug=True, port=5000)