import requests
import sys
import os
from serpapi import search as serpapi_search

# Add the parent directory to sys.path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.config import SERPAPI_API_KEY

def search(query, num=10):
    params = {
        'api_key': SERPAPI_API_KEY,
        'engine': 'google',
        'q': query,
        'num': num
    }
    results = serpapi_search(params).get('organic_results', [])
    return [{'title': r.get('title'), 'link': r.get('link'), 'snippet': r.get('snippet')} for r in results]
