from flask import Flask, request, jsonify
from scraper import scrape_threads

app = Flask(__name__)

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()
    urls = data.get("threads", [])
    result = scrape_threads(urls)
    return jsonify(result)

@app.route("/test", methods=["GET"])
def test():
    return {"status": "ok"}

@app.route("/selftest", methods=["GET"])
def selftest():
    import requests
    r = requests.post(
        "https://amino-scraper.onrender.com/scrape",
        json={"threads": ["https://forum.academywave.com/showthread.php?t=456"]}
    )
    return r.text
