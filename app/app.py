from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import random
import math
from create_vector_db import CreateAndLoadVectorDB
from run_inference import RunInference
from constants import SOURCE_PDF_FILE_PATH, VECTORDB_FILE_PATH
import logging
import apl_logger

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/entrypoint', methods=['GET'])
def entrypoint():
    """
    Entry point for the application.
    Returns a welcome message.
    """
    logger.info("Hello from entrypoint")
    return jsonify({"message":"Hi there"}), 200

@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint to authenticate user and return JWT token.
    Expects JSON input: {"username": "your_username", "password": "your_password"}
    """
    logger.info("Received login request")
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    if not username or not password:
        return jsonify({"error": "Missing 'username' or 'password' in request body"}), 400


    # For simplicity, we are using a static check. In production, use a database.
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route('/create_vector_db', methods=['GET'])
def create_vector_db_endpoint():
    """
    Endpoint to create and save vector database.
    """
    logger.info("Received create_vector_db request")
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
    logger.info("Received inference request")
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    query_text = data['query']

    inference = RunInference()
    response_output,context = inference.run_inference(query_text)
    
    # Return the top_k results
    return jsonify({
        "query": query_text,
        "results": response_output,
        "context": context,
    }), 200

if __name__ == '__main__':
    # Run the Flask application
    # In a production environment, you would use a WSGI server like Gunicorn or uWSGI
    logger.info("Starting app")
    app.run(host='0.0.0.0', port=5000, debug=True)