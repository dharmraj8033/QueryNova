from serpapi import search as serpapi_search

from src.utils.secrets import get_secret


def get_serpapi_key():
    """Resolve the SerpAPI key from Streamlit secrets or environment variables."""
    return get_secret("SERPAPI_API_KEY")

def search(query, num=10):
    api_key = get_serpapi_key()
    
    if not api_key:
        raise ValueError(
            "SERPAPI_API_KEY is not configured. Define it via Streamlit secrets or environment variables."
        )
    
    params = {
        'api_key': api_key,
        'engine': 'google',
        'q': query,
        'num': num
    }
    results = serpapi_search(params).get('organic_results', [])
    return [{'title': r.get('title'), 'link': r.get('link'), 'snippet': r.get('snippet')} for r in results]
