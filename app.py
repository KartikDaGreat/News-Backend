from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def authorization_access(func):
    def wrapper(*args, **kwargs):
        user_name = request.headers.get("username")
        password = request.headers.get("password")

        if user_name == "kartik" and password == "kartik":
            return func(*args, **kwargs)
        else:
            return jsonify({"message": "Unauthorized"}), 403 
    return wrapper

@app.route('/', methods=['GET'])
@authorization_access
def hello_world():
    return jsonify({"message": "Hello, World!"}), 200

@app.route('/news/<info>', methods=['GET'])
@authorization_access
def news(info):
    base_url = "https://api.webz.io/newsApiLite?token=b5d22bb0-af58-4e7f-b59f-d3d4c02c5ee4&q="
    url = base_url + info
    
    # Make the request to the external news API
    r = requests.get(url)
    
    if r.status_code == 200:
        data = r.json()
        return jsonify(data), 200  # Use 200 status code for successful request
    else:
        return jsonify({"error": "Failed to fetch news"}), r.status_code  # Return appropriate error if request fails

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
