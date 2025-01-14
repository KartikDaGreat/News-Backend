from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"}), 200

# @app.route('/api/process', methods=['POST'])
# def process_data():
#     try:
#         data = request.get_json()
#         if not data:
#             return jsonify({"error": "No JSON data provided"}), 400
#         processed_data = {"received": data, "status": "Processed"}
#         return jsonify(processed_data), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# Expose WSGI app as 'app'
if __name__ == "__main__":
    app.run(debug=True)
