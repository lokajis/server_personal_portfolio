from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from your frontend
the_database = []
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json  # Retrieve JSON data from the frontend
    name = data.get('name')
    email = data.get('email')
    description = data.get('description')
    the_database.append({name, email, description})

    # You can process the data here (send an email, store it in a DB, etc.)
    print(f"New message  {the_database}")
    # For demonstration purposes, just return a success message
    return jsonify({"message": "Message received !"}), 200

if __name__ == '__main__':
    app.run(debug=True)
