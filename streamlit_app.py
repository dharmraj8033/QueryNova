"""
QueryNova - AI-Powered Search Assistant
Streamlit Cloud Entry Point
"""
import sys
import os

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
    initial_sidebar_state="expanded"
)

def safe_rank_pages(query, pages):
    """Fallback ranking without AI when OpenAI API is not available"""
    try:
        from modules.ai_filter import rank_pages
        return rank_pages(query, pages)
    except Exception as e:
        st.warning(f"AI ranking unavailable: {str(e)[:100]}... Using basic ranking.")
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

# Sidebar with instructions
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/search.png", width=80)
    st.title("About QueryNova")
    st.write("""
    QueryNova is an AI-powered search assistant that:
    
    🔍 **Searches** the web using SerpAPI  
    🕷️ **Crawls** and extracts content  
    🧠 **Ranks** results using AI embeddings  
    
    ### How to Use:
    1. Enter your search query
    2. Click the Search button
    3. View AI-ranked results with summaries
    
    ### Setup:
    - Add API keys in Streamlit Cloud secrets
    - SERPAPI_API_KEY (required)
    - OPENAI_API_KEY (for AI ranking)
    """)
    
    # Check for API keys
    serpapi_key = os.getenv('SERPAPI_API_KEY') or st.secrets.get('SERPAPI_API_KEY', '')
    openai_key = os.getenv('OPENAI_API_KEY') or st.secrets.get('OPENAI_API_KEY', '')
    
    if serpapi_key and serpapi_key != 'your_serpapi_key_here':
        st.success("✅ SerpAPI configured")
    else:
        st.error("❌ SerpAPI key missing")
    
    if openai_key and openai_key != 'sk-your_openai_key_here':
        st.success("✅ OpenAI configured")
    else:
        st.warning("⚠️ OpenAI key missing (basic ranking only)")
    
    st.divider()
    st.caption("Built with ❤️ using Streamlit")

# Main content
st.title("🔍 QueryNova Search")
st.write("AI-powered search with web crawling and intelligent ranking")

# Create columns for better layout
col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input(
        "Enter your search query:", 
        placeholder="e.g., AI in healthcare, Python best practices, etc.",
        label_visibility="collapsed"
    )

with col2:
    search_button = st.button("🚀 Search", type="primary", use_container_width=True)

if search_button:
    if query.strip():
        # Check for API key
        serpapi_key = os.getenv('SERPAPI_API_KEY') or st.secrets.get('SERPAPI_API_KEY', '')
        if not serpapi_key or serpapi_key == 'your_serpapi_key_here':
            st.error("⚠️ SerpAPI key not configured. Please add your API key in the app secrets.")
            st.info("Go to App Settings → Secrets and add: `SERPAPI_API_KEY = \"your_key\"`")
        else:
            with st.spinner("Searching and analyzing results..."):
                try:
                    # Step 1: Search
                    with st.status("Processing your search...", expanded=True) as status:
                        st.write("🔍 Searching the web...")
                        results = search(query)
                        
                        if not results:
                            status.update(label="Search complete", state="error")
                            st.error("No search results found. Please try a different query.")
                        else:
                            st.write(f"✅ Found {len(results)} search results")
                            
                            # Step 2: Crawl
                            st.write("🕷️ Crawling web pages...")
                            urls = [r['link'] for r in results]
                            pages = asyncio.run(crawl_pages(urls))
                            st.write(f"✅ Crawled {len(pages)} pages")
                            
                            # Step 3: Rank
                            st.write("🧠 Ranking results with AI...")
                            ranked = safe_rank_pages(query, pages)
                            
                            status.update(label="Search complete!", state="complete")
                    
                    # Display results
                    if ranked:
                        st.success(f"✅ Found {len(ranked)} relevant results")
                        
                        # Add a separator
                        st.divider()
                        
                        for i, item in enumerate(ranked, 1):
                            # Calculate color based on score
                            score = item.get('score', 0)
                            if score > 0.7:
                                score_color = "🟢"
                            elif score > 0.4:
                                score_color = "🟡"
                            else:
                                score_color = "🔴"
                            
                            with st.expander(f"{score_color} #{i} - {item['title']}", expanded=(i <= 3)):
                                col_a, col_b = st.columns([3, 1])
                                with col_a:
                                    st.markdown(f"**🔗 URL:** [{item['url']}]({item['url']})")
                                with col_b:
                                    st.metric("Relevance Score", f"{score:.2%}")
                                
                                st.markdown("**📄 Summary:**")
                                st.write(item['summary'])
                                
                                # Add a copy button for the URL
                                st.code(item['url'], language=None)
                    else:
                        st.warning("No content could be extracted from the search results.")
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    with st.expander("Show error details"):
                        st.exception(e)
    else:
        st.warning("⚠️ Please enter a search query.")

# Footer
st.divider()
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.caption("🔍 Powered by SerpAPI")
with col_b:
    st.caption("🧠 AI Ranking via OpenAI")
with col_c:
    st.caption("⚡ Built with Streamlit")
