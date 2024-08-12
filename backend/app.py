from flask import Flask, jsonify, request
# from llm_extraction import generate_query
from flask_cors import CORS
import time, json

app = Flask(__name__)
CORS(app)


@app.route('/api', methods=['GET'])
def home():
    return jsonify({"message": "Hello, World!"})


@app.route('/generate_rq', methods=['POST'])
def chat():
    data = request.json
    print(data)
    # user_text = data['messages'][0]['text']
    # generated_query = json.dumps(generate_query(user_text).model_dump(exclude_none=True, by_alias=True))
    
    return {
        "input": "Ursus arctos in North America",
        "rq": {
            "genus": "Ursus",
            "specificepithet": "arctos",
            "continent": "North America"
        },
        "result": "success",
        "message": ""
    }


if __name__ == '__main__':
    app.run(debug=True, port=9080)


