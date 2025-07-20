import openai
import numpy as np
import sys
import os

# Add the parent directory to sys.path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.config import OPENAI_API_KEY

# Initialize OpenAI client with the new API format
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_embedding(text):
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
    # Embed the query
    query_emb = get_embedding(query)
    ranked = []
    for page in pages:
        text = page.get('text', '')[:2000]
        emb = get_embedding(text)
        score = cosine_similarity(query_emb, emb)
        # Generate summary
        summary_resp = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {'role': 'system', 'content': 'Summarize the following text in a short paragraph:'},
                {'role': 'user', 'content': text}
            ],
            max_tokens=150
        )
        summary = summary_resp['choices'][0]['message']['content']
        ranked.append({'url': page['url'], 'title': page.get('title', ''), 'summary': summary, 'score': score})
    # Sort by score descending
    ranked.sort(key=lambda x: x['score'], reverse=True)
    return ranked
