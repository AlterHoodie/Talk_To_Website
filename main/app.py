from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return "Flask API Server is running!"

@app.route('/crawl', methods=['GET'])
def crawl():

    ## Creating a config json payload to start crawling a website
    query_param = request.args.get('website', '')
    print(query_param)
    match = query_param+"**"
    print(match)
    payload = {
        "url": query_param,
        "match": match,## Crawls other webpages within the same domain
        "maxPagesToCrawl": 5,##Max Number of webpages it will crawl 
        "selector": "",
        "outputFileName": "output1.json",
        "maxTokens": 2000000
    }

    try:

        ## Sending request to crawler
        headers = {'Content-Type': 'application/json'}
        response = requests.post('http://localhost:3000/crawl', json=(payload),headers=headers)
        print(response)
        ## Sending request to database server to populate it
        response_json = response.json()
        target_url = 'http://localhost:3002/populate_db'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(target_url, json=response_json, headers=headers)
        return f"Data Crawled and Populated"
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/populate_db', methods=['POST'])
def populate_db():
    # Handle POST request with JSON body
    try:
        data = request.json  # Assuming JSON data is sent in the request body
        
        # Example: Forward the request to another API endpoint (localhost:3002/populate_db)
        target_url = 'http://localhost:3002/populate_db'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(target_url, json=data, headers=headers)
        
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/query', methods=['GET'])
def query():
    # Querying the database server 
    try:
        query_param = request.args.get('query', '')  # Get 'query' parameter from URL
        
        # Example: Forward the request to another API endpoint (localhost:3002/query)
        target_url = f'http://localhost:3002/query?query={query_param}'
        response = requests.get(target_url)
        
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(port=3001, debug=True)
