from flask import Flask, jsonify, request
from llm_extraction import generate_query
from flask_cors import CORS
import time, json

app = Flask(__name__)

CORS(app)

@app.route('/api', methods=['GET'])
def home():
    return jsonify({"message": "Hello, World!"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_text = data['messages'][0]['text']
    generated_query = json.dumps(generate_query(user_text).model_dump(exclude_none=True))
    
    return {"text": f"Here is the query I generated: {generated_query} "}

if __name__ == '__main__':
    app.run(debug=True, port=8080)


