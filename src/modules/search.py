import requests
import sys
import os
from serpapi import search as serpapi_search

def get_serpapi_key():
    """Get SerpAPI key from Streamlit secrets or environment"""
    # Try Streamlit secrets first (for cloud deployment)
    try:
        import streamlit as st
        key = st.secrets.get('SERPAPI_API_KEY')
        if key and key != 'your_serpapi_key_here':
            return key
    except (ImportError, FileNotFoundError, KeyError, AttributeError):
        pass
    
    # Fallback to environment variable or config
    key = os.getenv('SERPAPI_API_KEY')
    if not key or key == 'your_serpapi_key_here':
        # Try importing from config as last resort
        try:
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            from config.config import SERPAPI_API_KEY
            key = SERPAPI_API_KEY
        except (ImportError, ValueError):
            pass
    
    return key

def search(query, num=10):
    api_key = get_serpapi_key()
    
    if not api_key or api_key == 'your_serpapi_key_here':
        raise ValueError("SERPAPI_API_KEY is not configured. Please add it to Streamlit secrets or environment variables.")
    
    params = {
        'api_key': api_key,
        'engine': 'google',
        'q': query,
        'num': num
    }
    results = serpapi_search(params).get('organic_results', [])
    return [{'title': r.get('title'), 'link': r.get('link'), 'snippet': r.get('snippet')} for r in results]
