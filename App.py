from flask import Flask, request, jsonify
from scraper import scrape_threads

app = Flask(__name__)

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()
    urls = data.get("threads", [])
    result = scrape_threads(urls)
    return jsonify(result)
