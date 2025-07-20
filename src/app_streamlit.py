import streamlit as st
import asyncio
from modules.search import search
from modules.crawl import crawl_pages

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

st.title("🔍 QueryNova Search")
st.write("AI-powered search with web crawling and intelligent ranking")

query = st.text_input("Enter your search query:", placeholder="e.g., AI in healthcare")

if st.button("🚀 Search", type="primary"):
    if query.strip():
        with st.spinner("Searching and analyzing results..."):
            try:
                # Step 1: Search
                st.info("🔍 Searching the web...")
                results = search(query)
                
                if not results:
                    st.error("No search results found. Please try a different query.")
                else:
                    st.success(f"Found {len(results)} search results")
                    
                    # Step 2: Crawl
                    st.info("🕷️ Crawling web pages...")
                    urls = [r['link'] for r in results]
                    pages = asyncio.run(crawl_pages(urls))
                    
                    # Step 3: Rank
                    st.info("🧠 Ranking results...")
                    ranked = safe_rank_pages(query, pages)
                    
                    # Display results
                    if ranked:
                        st.success(f"✅ Analysis complete! Found {len(ranked)} results")
                        
                        for i, item in enumerate(ranked, 1):
                            with st.expander(f"#{i} - {item['title']} (Score: {item['score']:.2f})"):
                                st.write(f"**URL:** [{item['url']}]({item['url']})")
                                st.write(f"**Summary:** {item['summary']}")
                    else:
                        st.warning("No content could be extracted from the search results.")
                        
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a search query.")
