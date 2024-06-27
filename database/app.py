from flask import Flask, request, jsonify
from populate_database import add_to_db
from query_data import query_rag
app = Flask(__name__)

# Endpoint to handle POST requests
@app.route('/populate_db', methods=['POST'])
def populate_db():
    
    data = request.json

    ## Adds crawled data to db
    # print(data)
    add_to_db(data)
    # Process the received JSON data (example: just returning it as JSON)
    return jsonify(data)


# Endpoint to handle GET requests with query parameter
@app.route('/query', methods=['GET'])
def query_text():
    query_param = request.args.get('query', '')  # Get 'query' parameter from URL
    response = query_rag("query_param")
    return f"Query received: {query_param}"
if __name__ == '__main__':
    app.run(port=3002)
