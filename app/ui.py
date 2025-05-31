from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy RAG logic (replace this with your actual RAG code)
def rag_pipeline(query):
    # Replace this with actual RAG logic
    response = f"Retrieved and generated answer for: {query}"
    return response

@app.route('/rag', methods=['POST'])
def handle_query():
    data = request.get_json()
    query = data.get("query", "")
    result = rag_pipeline(query)
    return jsonify({"response": result})

if __name__ == '__main__':
    app.run(port=5000)
