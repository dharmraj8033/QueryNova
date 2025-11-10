import openai
import numpy as np
import sys
import os

def get_openai_key():
    """Get OpenAI API key from Streamlit secrets or environment"""
    # Try Streamlit secrets first (for cloud deployment)
    try:
        import streamlit as st
        key = st.secrets.get('OPENAI_API_KEY')
        if key and key != 'sk-your_openai_key_here':
            return key
    except (ImportError, FileNotFoundError, KeyError, AttributeError):
        pass
    
    # Fallback to environment variable or config
    key = os.getenv('OPENAI_API_KEY')
    if not key or key == 'sk-your_openai_key_here':
        # Try importing from config as last resort
        try:
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            from config.config import OPENAI_API_KEY
            key = OPENAI_API_KEY
        except (ImportError, ValueError):
            pass
    
    return key

def get_client():
    """Get or create OpenAI client"""
    api_key = get_openai_key()
    if not api_key or api_key == 'sk-your_openai_key_here':
        raise ValueError("OPENAI_API_KEY is not configured. Please add it to Streamlit secrets or environment variables.")
    return openai.OpenAI(api_key=api_key)

def get_embedding(text):
    client = get_client()
    response = client.embeddings.create(
        input=text,
        model='text-embedding-ada-002'
    )
    return response.data[0].embedding

def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def rank_pages(query, pages):
    if not pages:
        return []
    
    client = get_client()
    
    # Embed the query
    query_emb = get_embedding(query)
    ranked = []
    for page in pages:
        text = page.get('text', '')[:2000]
        emb = get_embedding(text)
        score = cosine_similarity(query_emb, emb)
        # Generate summary
        summary_resp = client.chat.completions.create(
            model='gpt-4',
            messages=[
                {'role': 'system', 'content': 'Summarize the following text in a short paragraph:'},
                {'role': 'user', 'content': text}
            ],
            max_tokens=150
        )
        summary = summary_resp.choices[0].message.content
        ranked.append({'url': page['url'], 'title': page.get('title', ''), 'summary': summary, 'score': score})
    # Sort by score descending
    ranked.sort(key=lambda x: x['score'], reverse=True)
    return ranked
