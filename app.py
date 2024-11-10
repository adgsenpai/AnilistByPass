from flask import Flask, request, jsonify
import requests
import json
from functools import lru_cache
import hashlib

app = Flask(__name__)

# Target GraphQL endpoint
TARGET_URL = "https://graphql.anilist.co/"

# Define the headers and cookies to forward with the request
HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://studio.apollographql.com",
    "Referer": "https://studio.apollographql.com/sandbox/explorer",
    "Sec-CH-UA": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

COOKIES = {
    "laravel_session": "AFnOgLFxSdjiBfEyJaYUcqTXUvimeuabLCM3"  # Replace with the actual cookie value
}

# Simple caching mechanism using LRU cache
@lru_cache(maxsize=128)
def cached_request(hash_key):
    try:
        response = requests.post(
            TARGET_URL,
            headers=HEADERS,
            cookies=COOKIES,
            json=json.loads(hash_key),
            timeout=10
        )
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route('/graphql', methods=['POST'])
def graphql_proxy():
    # Extract the incoming JSON payload
    incoming_payload = request.get_json()
    if not incoming_payload:
        return jsonify({"error": "Invalid request, JSON body required"}), 400

    # Create a hash key for caching based on the request payload
    hash_key = json.dumps(incoming_payload, sort_keys=True)
    hash_key = hashlib.md5(hash_key.encode('utf-8')).hexdigest()

    # Get the cached response or make a new request
    cached_response = cached_request(json.dumps(incoming_payload, sort_keys=True))

    if "error" in cached_response:
        return jsonify({"error": cached_response["error"]}), 500

    return jsonify(cached_response)

@app.route('/', methods=['POST'])
def graphql_proxy2():
    # Extract the incoming JSON payload
    incoming_payload = request.get_json()
    if not incoming_payload:
        return jsonify({"error": "Invalid request, JSON body required"}), 400

    # Create a hash key for caching based on the request payload
    hash_key = json.dumps(incoming_payload, sort_keys=True)
    hash_key = hashlib.md5(hash_key.encode('utf-8')).hexdigest()

    # Get the cached response or make a new request
    cached_response = cached_request(json.dumps(incoming_payload, sort_keys=True))

    if "error" in cached_response:
        return jsonify({"error": cached_response["error"]}), 500

    return jsonify(cached_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
