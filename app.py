from flask import Flask, request, jsonify
import requests
from textblob import TextBlob

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
# @authorization_access
def hello_world():
    return jsonify({"message": "Hello, World!"}), 200

@app.route('/news/', methods=['GET'])
# @authorization_access
def news():
    base_url = "https://api.webz.io/newsApiLite?token=b5d22bb0-af58-4e7f-b59f-d3d4c02c5ee4&q="
    
    stock_names = ['SBI Healthcare', 'Aditya Birla Sun Life']
    stock_results = []

    for stock in stock_names:
        url = base_url + stock.replace(" ", "%20")  # Encode spaces for URL
        r = requests.get(url)
        
        if r.status_code == 200:
            data = r.json()
            stock_data = {
                "stock_name": stock,
                "news": []
            }
            
            for post in data.get("posts", []):
                title = post.get("title", "")
                sentiment = post.get("sentiment", "neutral")
                
                # Use NLP to calculate news seriousness
                analysis = TextBlob(title)
                polarity = analysis.sentiment.polarity  # Ranges from -1 to 1
                subjectivity = analysis.sentiment.subjectivity  # Ranges from 0 to 1

                if polarity < -0.3:
                    rating = "high_negative"
                elif polarity < 0:
                    rating = "low_negative"
                elif polarity == 0:
                    rating = "neutral"
                elif polarity < 0.3:
                    rating = "low_positive"
                else:
                    rating = "high_positive"
                
                stock_data["news"].append({
                    "title": title,
                    "sentiment": sentiment,
                    "polarity": polarity,
                    "subjectivity": subjectivity,
                    "rating": rating
                })
            
            stock_results.append(stock_data)
        else:
            return jsonify({"error": f"Failed to fetch news for {stock}"}), r.status_code

    return jsonify({"stocks": stock_results}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
