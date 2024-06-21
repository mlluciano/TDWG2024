from flask import Flask, jsonify, request
# from llm_extraction import generate_query
from flask_cors import CORS
import time

app = Flask(__name__)

CORS(app)

@app.route('/api', methods=['GET'])
def home():
    return jsonify({"message": "Hello, World!"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    print(data)
    time.sleep(1)
    return {"text": "This is an automated response. Implement the LLM calling!"}

if __name__ == '__main__':
    app.run(debug=True, port=8080)


