import os
from datetime import datetime, timedelta, timezone
import sqlite3
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
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
app.config['SECRET_KEY'] = 'your_super_secret_key_change_this' # CHANGE THIS IN PRODUCTION!
app.config['JWT_EXPIRATION_MINUTES'] = 60 # Token expires in 60 minutes
DATABASE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

# Initialize the database when the app starts
with app.app_context():
    init_db()

# JWT Decorator for protected routes
def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1] # Bearer <token>
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    hashed_password = generate_password_hash(password)

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username already exists'}), 409
    except Exception as e:
        return jsonify({'message': f'Error registering user: {e}'}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    with get_db_connection() as conn:
        cursor = conn.cursor()
        user = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401

    if check_password_hash(user['password_hash'], password):
        expiration = datetime.now(timezone.utc) + timedelta(minutes=app.config['JWT_EXPIRATION_MINUTES'])
        token = jwt.encode(
            {
                'username': user['username'],
                'exp': expiration
            },
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/create_vector_db', methods=['GET'])
@jwt_required
def create_vector_db_endpoint(current_user):
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
@jwt_required
def run_inference_endpoint(current_user):
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

