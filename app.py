import json
from flask import Flask, request, jsonify
from flask_cors import CORS 


app = Flask(__name__)
CORS(app) # Allow requests from your extension

@app.route('/', methods=['POST'])
def receive_array():
    data = request.json
    info = data.get('task', '')

    print("Received String:", info)

    # 1. Save the array to a file for later use
    with open('saved_assignments.json', 'w') as f:
        json.dump(info, f, indent=4)
        
    return jsonify({"status": "success", "message": "Array received"}), 200


if __name__ == '__main__':
    app.run(port=5000)
#change 