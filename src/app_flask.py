from flask import Flask, request, jsonify
import asyncio
from modules.search import search
from modules.crawl import crawl_pages
from modules.ai_filter import rank_pages

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search_route():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    results = search(query)
    urls = [r['link'] for r in results]
    pages = asyncio.run(crawl_pages(urls))
    ranked = rank_pages(query, pages)
    return jsonify(ranked)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
