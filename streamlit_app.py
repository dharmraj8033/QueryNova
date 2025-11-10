import sys
import os
import json
from datetime import datetime
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import streamlit as st
import asyncio
from modules.search import search
from modules.crawl import crawl_pages

st.set_page_config(
    page_title='QueryNova - AI Search',
    page_icon='',
    layout='wide'
)

st.markdown('''
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e1e2e 0%, #27273a 100%);
}
.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border: none;
}
.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}
</style>
''', unsafe_allow_html=True)

if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'results_cache' not in st.session_state:
    st.session_state.results_cache = {}

def safe_rank_pages(query, pages):
    try:
        from modules.ai_filter import rank_pages
        return rank_pages(query, pages)
    except Exception as e:
        st.warning(' AI ranking unavailable. Using basic ranking.')
        ranked = []
        for i, page in enumerate(pages):
            ranked.append({
                'title': page.get('title', 'No Title'),
                'url': page.get('url', ''),
                'summary': page.get('text', '')[:300] + '...' if page.get('text') else 'No content available',
                'score': 1.0 - (i * 0.1)
            })
        return ranked

def add_to_history(query, results_count):
    entry = {
        'query': query,
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'results_count': results_count
    }
    st.session_state.search_history.insert(0, entry)
    st.session_state.search_history = st.session_state.search_history[:10]

with st.sidebar:
    st.title(' QueryNova')
    st.markdown('###  API Status')
    serpapi_key = os.getenv('SERPAPI_API_KEY') or st.secrets.get('SERPAPI_API_KEY', '')
    openai_key = os.getenv('OPENAI_API_KEY') or st.secrets.get('OPENAI_API_KEY', '')
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown('' if serpapi_key and serpapi_key != 'your_serpapi_key_here' else '')
    with col2:
        st.text('SerpAPI')
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown('' if openai_key and openai_key != 'sk-your_openai_key_here' else '')
    with col2:
        st.text('OpenAI')
    st.divider()
    if st.session_state.search_history:
        st.markdown('###  Recent Searches')
        for entry in st.session_state.search_history[:5]:
            if st.button(f' {entry[\"query\"][:30]}...', key=f'hist_{entry[\"timestamp\"]}', use_container_width=True):
                st.session_state.rerun_query = entry['query']
                st.rerun()
            st.caption(f'{entry[\"timestamp\"]}  {entry[\"results_count\"]} results')
    st.divider()
    if st.session_state.search_history:
        st.markdown('###  Stats')
        st.metric('Searches', len(st.session_state.search_history))
        total_results = sum(h['results_count'] for h in st.session_state.search_history)
        st.metric('Results Found', total_results)
    st.divider()
    st.caption('Built with  using Streamlit')

st.title(' QueryNova Search')
st.markdown('**AI-powered search with intelligent ranking**')

tab1, tab2 = st.tabs([' Search', ' Export'])

with tab1:
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input('Search', placeholder='Enter your search query...', label_visibility='collapsed', value=st.session_state.get('rerun_query', ''))
        if 'rerun_query' in st.session_state:
            del st.session_state.rerun_query
    with col2:
        st.markdown('<br>', unsafe_allow_html=True)
        search_button = st.button(' Search', type='primary', use_container_width=True)
    with st.expander(' Options'):
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            num_results = st.slider('Results', 5, 20, 10)
        with col_opt2:
            use_cache = st.checkbox('Use Cache', value=True)

with tab2:
    if 'last_results' in st.session_state and st.session_state.last_results:
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            json_data = json.dumps(st.session_state.last_results, indent=2)
            st.download_button(' Download JSON', json_data, f'querynova_{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}.json', 'application/json', use_container_width=True)
        with col_exp2:
            csv_data = 'Rank,Title,URL,Score,Summary\n'
            for i, item in enumerate(st.session_state.last_results, 1):
                title = item['title'].replace('\"', '\"\"')
                summary = item['summary'].replace('\"', '\"\"')
                csv_data += f'{i},\"{title}\",\"{item[\"url\"]}\",{item.get(\"score\", 0):.2f},\"{summary}\"\n'
            st.download_button(' Download CSV', csv_data, f'querynova_{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}.csv', 'text/csv', use_container_width=True)
        st.success(f' {len(st.session_state.last_results)} results ready')
    else:
        st.info(' Perform a search first to export results')

if search_button and query.strip():
    serpapi_key = os.getenv('SERPAPI_API_KEY') or st.secrets.get('SERPAPI_API_KEY', '')
    if not serpapi_key or serpapi_key == 'your_serpapi_key_here':
        st.error(' SerpAPI key not configured')
        st.info('Add +SERPAPI_API_KEY to app secrets')
    else:
        cache_key = f'{query}_{num_results}'
        if use_cache and cache_key in st.session_state.results_cache:
            st.info(' Loading from cache...')
            ranked = st.session_state.results_cache[cache_key]
            time.sleep(0.3)
        else:
            with st.status('Processing...', expanded=True) as status:
                try:
                    st.write(' Searching...')
                    results = search(query, num=num_results)
                    if not results:
                        status.update(label='No results', state='error')
                        st.error(' No results found')
                        ranked = None
                    else:
                        st.write(f' Found {len(results)} results')
                        st.write(' Crawling pages...')
                        urls = [r['link'] for r in results]
                        pages = asyncio.run(crawl_pages(urls))
                        st.write(' Ranking with AI...')
                        ranked = safe_rank_pages(query, pages)
                        status.update(label=' Complete!', state='complete')
                        if use_cache:
                            st.session_state.results_cache[cache_key] = ranked
                except Exception as e:
                    st.error(f' Error: {str(e)}')
                    ranked = None
        if ranked:
            add_to_history(query, len(ranked))
            st.session_state.last_results = ranked
            st.divider()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric('Results', len(ranked))
            with col2:
                avg = sum(r.get('score', 0) for r in ranked) / len(ranked)
                st.metric('Avg Score', f'{avg:.0%}')
            with col3:
                high = len([r for r in ranked if r.get('score', 0) > 0.7])
                st.metric('High Quality', high)
            st.divider()
            for i, item in enumerate(ranked, 1):
                score = item.get('score', 0)
                emoji = '' if score > 0.7 else '' if score > 0.4 else ''
                with st.expander(f'{emoji} **#{i}** - {item[\"title\"]}', expanded=(i <= 3)):
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.markdown(f'** [{item[\"url\"]}]({item[\"url\"]})**')
                    with col_b:
                        st.metric('Score', f'{score:.0%}')
                    st.markdown('**Summary:**')
                    st.write(item['summary'])
elif search_button:
    st.warning(' Enter a search query')

st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption(' Powered by SerpAPI')
with col2:
    st.caption(' OpenAI Embeddings')
with col3:
    st.caption(f' {datetime.now().strftime(\"%H:%M\")}')
