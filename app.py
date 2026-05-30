from flask import Flask, request, jsonify
from flask_cors import CORS # pip install flask-cors

app = Flask(__name__)
CORS(app) # Allow requests from your extension

@app.route('/', methods=['POST'])
def receive_array():
    data = request.json
    my_array = data.get('array', [])
    
    # Process the array in Python
    print("Received Array:", my_array)
    
    return jsonify({"status": "success", "message": "Array received"}), 200

if __name__ == '__main__':
    app.run(port=5000)
