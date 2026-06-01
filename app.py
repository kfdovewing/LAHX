from flask import Flask, request, jsonify
from flask_cors import CORS 



app = Flask(__name__)
CORS(app) # Allow requests from your extension


@app.route('/', methods=['POST'])
def receive_task():
    data = request.json
    info = data.get('task', [])

    print("Received data:", info)

    # 1. Save the array to a file for later use
    with open('saved_assignments.txt', 'a', encoding='utf-8') as f:
        for task in info:
            f.write(task + "\n")
            
    return jsonify({"status": "success", "message": "Array received"}), 200


if __name__ == '__main__':
    app.run(port=5000)
#change 