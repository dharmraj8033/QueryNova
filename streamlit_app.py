"""
QueryNova - AI-Powered Search Assistant
Enhanced Streamlit Cloud Entry Point with Dark Mode Support
"""
import sys
import os
import json
from datetime import datetime
import time

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import streamlit as st
import asyncio
from modules.search import search
from modules.crawl import crawl_pages

# Configure page
st.set_page_config(
    page_title="QueryNova - AI Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/dharmraj8033/QueryNova',
        'Report a bug': 'https://github.com/dharmraj8033/QueryNova/issues',
        'About': '# QueryNova 🔍\nAI-powered search with intelligent ranking'
    }
)

# Custom CSS for dark mode and improved UI
st.markdown("""
<style>
    /* Dark mode support */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e2e 0%, #27273a 100%);
    }
    
    /* Light mode support */
    @media (prefers-color-scheme: light) {
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
    }
    
    /* Search box styling */
    .stTextInput > div > div > input {
        font-size: 18px;
        border-radius: 10px;
        border: 2px solid #667eea;
        padding: 15px;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
        font-size: 18px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-size: 16px;
        font-weight: 600;
        border-radius: 10px;
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 24px;
        font-weight: bold;
    }
    
    /* Card-like containers */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid #667eea;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0px 0px;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    /* History cards */
    .history-card {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'results_cache' not in st.session_state:
    st.session_state.results_cache = {}
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

def safe_rank_pages(query, pages):
    """Fallback ranking without AI when OpenAI API is not available"""
    try:
        from modules.ai_filter import rank_pages
        return rank_pages(query, pages)
    except Exception as e:
        st.warning(f"⚠️ AI ranking unavailable: {str(e)[:100]}... Using basic ranking.")
        # Simple fallback: return pages with basic info
        ranked = []
        for i, page in enumerate(pages):
            ranked.append({
                'title': page.get('title', 'No Title'),
                'url': page.get('url', ''),
                'summary': page.get('text', '')[:300] + '...' if page.get('text') else 'No content available',
                'score': 1.0 - (i * 0.1)  # Simple decreasing score
            })
        return ranked

def add_to_history(query, results_count):
    """Add search to history"""
    history_entry = {
        'query': query,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'results_count': results_count
    }
    st.session_state.search_history.insert(0, history_entry)
    # Keep only last 10 searches
    st.session_state.search_history = st.session_state.search_history[:10]

def export_results_json(results):
    """Export results as JSON"""
    return json.dumps(results, indent=2)

def export_results_csv(results):
    """Export results as CSV format"""
    csv = "Rank,Title,URL,Score,Summary\n"
    for i, item in enumerate(results, 1):
        title = item['title'].replace('"', '""')
        summary = item['summary'].replace('"', '""')
        url = item['url']
        score = item.get('score', 0)
        csv += f'{i},"{title}","{url}",{score:.2f},"{summary}"\n'
    return csv

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/search.png", width=80)
    st.title("⚡ QueryNova")
    
    # Theme toggle
    theme_col1, theme_col2 = st.columns([1, 2])
    with theme_col1:
        st.markdown("### 🎨")
    with theme_col2:
        theme = st.selectbox(
            "Theme",
            ["🌙 Dark Mode", "☀️ Light Mode", "🌈 Auto"],
            label_visibility="collapsed"
        )
    
    st.divider()
    
    # About section
    with st.expander("📖 About QueryNova", expanded=True):
        st.markdown("""
        **QueryNova** is an AI-powered search assistant that:
        
        🔍 **Searches** the web using SerpAPI  
        🕷️ **Crawls** and extracts content  
        🧠 **Ranks** results using AI embeddings  
        ⚡ **Caches** results for faster access
        📊 **Exports** data in multiple formats
        """)
    
    # API Status
    with st.expander("🔐 API Status", expanded=True):
        serpapi_key = os.getenv('SERPAPI_API_KEY') or st.secrets.get('SERPAPI_API_KEY', '')
        openai_key = os.getenv('OPENAI_API_KEY') or st.secrets.get('OPENAI_API_KEY', '')
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if serpapi_key and serpapi_key != 'your_serpapi_key_here':
                st.markdown("✅")
            else:
                st.markdown("❌")
        with col2:
            st.text("SerpAPI")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if openai_key and openai_key != 'sk-your_openai_key_here':
                st.markdown("✅")
            else:
                st.markdown("⚠️")
        with col2:
            st.text("OpenAI (AI Ranking)")
    
    st.divider()
    
    # Search History
    if st.session_state.search_history:
        with st.expander("📜 Search History", expanded=False):
            for entry in st.session_state.search_history[:5]:
                if st.button(f"🔍 {entry['query'][:25]}...", key=f"hist_{entry['timestamp']}", use_container_width=True):
                    st.session_state.rerun_query = entry['query']
                    st.rerun()
                st.caption(f"{entry['timestamp']} • {entry['results_count']} results")
    
    st.divider()
    
    # Statistics
    if st.session_state.search_history:
        st.markdown("### 📊 Statistics")
        total_searches = len(st.session_state.search_history)
        total_results = sum(h['results_count'] for h in st.session_state.search_history)
        st.metric("Total Searches", total_searches)
        st.metric("Total Results Found", total_results)
    
    st.divider()
    st.caption("Built with ❤️ using Streamlit")
    st.caption("v2.0 • Enhanced Edition")

# Main content
col_header1, col_header2 = st.columns([4, 1])
with col_header1:
    st.title("🔍 QueryNova Search")
    st.markdown("**AI-powered search with web crawling and intelligent ranking**")
with col_header2:
    st.markdown("")
    st.markdown("")
    if st.button("🔄 Clear Cache", help="Clear cached results"):
        st.session_state.results_cache = {}
        st.success("Cache cleared!")

# Search interface with tabs
tab1, tab2, tab3 = st.tabs(["🔍 Search", "📊 Advanced", "💾 Export"])

with tab1:
    # Create columns for better layout
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "Enter your search query:", 
            placeholder="e.g., AI in healthcare, Python best practices, Latest technology trends...",
            label_visibility="collapsed",
            key="search_input",
            value=st.session_state.get('rerun_query', '')
        )
        if 'rerun_query' in st.session_state:
            del st.session_state.rerun_query
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.button("🚀 Search", type="primary", use_container_width=True)
    
    # Advanced options in expander
    with st.expander("⚙️ Advanced Options"):
        col_opt1, col_opt2, col_opt3 = st.columns(3)
        with col_opt1:
            num_results = st.slider("Number of Results", 5, 20, 10, help="Number of search results to fetch")
        with col_opt2:
            use_cache = st.checkbox("Use Cache", value=True, help="Cache results for faster retrieval")
        with col_opt3:
            auto_summarize = st.checkbox("Auto Summarize", value=True, help="Generate AI summaries")

with tab2:
    st.markdown("### 🎯 Advanced Search Features")
    
    col_adv1, col_adv2 = st.columns(2)
    
    with col_adv1:
        st.markdown("#### 🔍 Search Filters")
        search_type = st.selectbox("Search Type", ["General", "News", "Academic", "Videos"])
        date_filter = st.selectbox("Date Range", ["Any time", "Past hour", "Past 24 hours", "Past week", "Past month"])
        language = st.selectbox("Language", ["Any", "English", "Spanish", "French", "German", "Chinese"])
    
    with col_adv2:
        st.markdown("#### 🎨 Display Options")
        sort_by = st.selectbox("Sort Results By", ["Relevance", "Date", "Score"])
        show_snippets = st.checkbox("Show Snippets", value=True)
        show_scores = st.checkbox("Show Relevance Scores", value=True)
        compact_view = st.checkbox("Compact View", value=False)

with tab3:
    st.markdown("### 💾 Export Options")
    if 'last_results' in st.session_state and st.session_state.last_results:
        col_exp1, col_exp2, col_exp3 = st.columns(3)
        
        with col_exp1:
            json_data = export_results_json(st.session_state.last_results)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"querynova_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col_exp2:
            csv_data = export_results_csv(st.session_state.last_results)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"querynova_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_exp3:
            # Create a simple text report
            text_report = f"QueryNova Search Results\n{'='*50}\n\n"
            for i, item in enumerate(st.session_state.last_results, 1):
                text_report += f"{i}. {item['title']}\n"
                text_report += f"   URL: {item['url']}\n"
                text_report += f"   Score: {item.get('score', 0):.2f}\n"
                text_report += f"   Summary: {item['summary']}\n\n"
            
            st.download_button(
                label="📥 Download TXT",
                data=text_report,
                file_name=f"querynova_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        st.success(f"✅ {len(st.session_state.last_results)} results ready for export")
    else:
        st.info("🔍 Perform a search first to enable export options")

# Main search execution
if search_button:
    if query.strip():
        # Check for API key
        serpapi_key = os.getenv('SERPAPI_API_KEY') or st.secrets.get('SERPAPI_API_KEY', '')
        if not serpapi_key or serpapi_key == 'your_serpapi_key_here':
            st.error("⚠️ SerpAPI key not configured. Please add your API key in the app secrets.")
            st.info("📖 Go to App Settings → Secrets and add: `SERPAPI_API_KEY = \"your_key\"`")
        else:
            # Check cache first
            cache_key = f"{query}_{num_results}"
            if use_cache and cache_key in st.session_state.results_cache:
                st.info("⚡ Loading results from cache...")
                ranked = st.session_state.results_cache[cache_key]
                time.sleep(0.5)  # Brief delay for UX
            else:
                start_time = time.time()
                
                with st.spinner("🔮 QueryNova is working its magic..."):
                    try:
                        # Step 1: Search
                        with st.status("Processing your search...", expanded=True) as status:
                            st.write("🔍 Searching the web...")
                            results = search(query, num=num_results)
                            
                            if not results:
                                status.update(label="Search complete", state="error")
                                st.error("❌ No search results found. Please try a different query.")
                            else:
                                st.write(f"✅ Found {len(results)} search results")
                                
                                # Step 2: Crawl
                                st.write("🕷️ Crawling web pages...")
                                urls = [r['link'] for r in results]
                                pages = asyncio.run(crawl_pages(urls))
                                st.write(f"✅ Crawled {len(pages)} pages")
                                
                                # Step 3: Rank
                                if auto_summarize:
                                    st.write("🧠 Ranking results with AI...")
                                    ranked = safe_rank_pages(query, pages)
                                else:
                                    st.write("📊 Organizing results...")
                                    ranked = pages
                                
                                end_time = time.time()
                                elapsed = end_time - start_time
                                
                                status.update(label=f"✨ Search complete in {elapsed:.2f}s!", state="complete")
                        
                        # Cache results
                        if use_cache:
                            st.session_state.results_cache[cache_key] = ranked
                        
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")
                        with st.expander("🔍 Show error details"):
                            st.exception(e)
                        ranked = None
            
            # Display results
            if ranked:
                # Add to history
                add_to_history(query, len(ranked))
                st.session_state.last_results = ranked
                
                # Results header
                st.divider()
                col_res1, col_res2, col_res3 = st.columns(3)
                with col_res1:
                    st.metric("📊 Total Results", len(ranked))
                with col_res2:
                    avg_score = sum(r.get('score', 0) for r in ranked) / len(ranked) if ranked else 0
                    st.metric("⭐ Avg. Relevance", f"{avg_score:.2%}")
                with col_res3:
                    st.metric("🔍 Query", f'"{query[:20]}..."')
                
                st.divider()
                
                # Display results with enhanced UI
                for i, item in enumerate(ranked, 1):
                    # Calculate color based on score
                    score = item.get('score', 0)
                    if score > 0.7:
                        score_emoji = "🟢"
                        score_color = "#4ade80"
                    elif score > 0.4:
                        score_emoji = "🟡"
                        score_color = "#fbbf24"
                    else:
                        score_emoji = "🔴"
                        score_color = "#f87171"
                    
                    # Create result card
                    with st.expander(
                        f"{score_emoji} **#{i}** - {item['title']}", 
                        expanded=(i <= 3 and not compact_view)
                    ):
                        col_a, col_b = st.columns([3, 1])
                        
                        with col_a:
                            st.markdown(f"**🔗 URL:** [{item['url']}]({item['url']})")
                        
                        with col_b:
                            if show_scores:
                                st.markdown(
                                    f"<div style='text-align: center; padding: 10px; background: {score_color}30; border-radius: 10px;'>"
                                    f"<span style='font-size: 24px; font-weight: bold; color: {score_color};'>{score:.0%}</span><br>"
                                    f"<span style='font-size: 12px;'>Relevance</span>"
                                    f"</div>",
                                    unsafe_allow_html=True
                                )
                        
                        if show_snippets:
                            st.markdown("**📄 Summary:**")
                            st.write(item['summary'])
                        
                        # Action buttons
                        col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
                        with col_btn1:
                            st.link_button("🌐 Visit", item['url'], use_container_width=True)
                        with col_btn2:
                            if st.button("📋 Copy URL", key=f"copy_{i}", use_container_width=True):
                                st.code(item['url'], language=None)
                        with col_btn3:
                            if st.button("🔖 Bookmark", key=f"bookmark_{i}", use_container_width=True):
                                st.toast(f"Bookmarked: {item['title']}")
                        with col_btn4:
                            if st.button("🔄 Similar", key=f"similar_{i}", use_container_width=True):
                                st.info("Feature coming soon!")
                
                # Summary statistics at bottom
                st.divider()
                st.markdown("### 📈 Search Summary")
                col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)
                with col_sum1:
                    high_relevance = len([r for r in ranked if r.get('score', 0) > 0.7])
                    st.metric("🟢 High Relevance", high_relevance)
                with col_sum2:
                    medium_relevance = len([r for r in ranked if 0.4 < r.get('score', 0) <= 0.7])
                    st.metric("🟡 Medium Relevance", medium_relevance)
                with col_sum3:
                    low_relevance = len([r for r in ranked if r.get('score', 0) <= 0.4])
                    st.metric("🔴 Low Relevance", low_relevance)
                with col_sum4:
                    st.metric("💾 Cached", "Yes" if use_cache else "No")
    else:
        st.warning("⚠️ Please enter a search query.")

# Footer
st.divider()
col_footer1, col_footer2, col_footer3, col_footer4 = st.columns(4)
with col_footer1:
    st.caption("🔍 Powered by SerpAPI")
with col_footer2:
    st.caption("🧠 AI Ranking via OpenAI")
with col_footer3:
    st.caption("⚡ Built with Streamlit")
with col_footer4:
    st.caption(f"🕐 {datetime.now().strftime('%H:%M:%S')}")
