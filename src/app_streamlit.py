"""
QueryNova - AI-Powered Search Assistant
Modern Streamlit Cloud-Ready Application
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import plotly.graph_objects as go
import streamlit as st
from streamlit.components.v1 import html

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.knowledge_base import KnowledgeBase
from services.search_service import SearchOptions, SearchPayload, SearchService
from utils import cache
from utils.logger import logger

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="QueryNova - AI-Powered Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================


def initialize_session_state() -> None:
    """Initialize all session state variables."""
    defaults = {
        "theme_mode": "dark",
        "query": "",
        "search_results": {},
        "search_history": [],
        "logs": [],
        "current_stage": None,
        "progress_messages": [],
    }
    
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)
    
    # Initialize knowledge base once
    if "knowledge_base" not in st.session_state:
        st.session_state["knowledge_base"] = KnowledgeBase()


# ============================================================================
# MODERN UI STYLING
# ============================================================================


def inject_modern_css() -> None:
    """Inject modern, responsive CSS with dark/light mode support."""
    
    # Theme colors
    if st.session_state.theme_mode == "dark":
        colors = {
            "bg_primary": "#0E1117",
            "bg_secondary": "#262730",
            "bg_tertiary": "#1E1E2E",
            "text_primary": "#FAFAFA",
            "text_secondary": "#A0A8C3",
            "accent_primary": "#4A90E2",
            "accent_secondary": "#2CB1BC",
            "accent_danger": "#FF6B6B",
            "border": "rgba(74, 144, 226, 0.3)",
            "shadow": "0 8px 32px rgba(0, 0, 0, 0.4)",
        }
    else:
        colors = {
            "bg_primary": "#FFFFFF",
            "bg_secondary": "#F5F7FA",
            "bg_tertiary": "#E8EBF0",
            "text_primary": "#1A1A1A",
            "text_secondary": "#6B7280",
            "accent_primary": "#4A90E2",
            "accent_secondary": "#2CB1BC",
            "accent_danger": "#FF6B6B",
            "border": "rgba(74, 144, 226, 0.2)",
            "shadow": "0 4px 16px rgba(0, 0, 0, 0.1)",
        }
    
    st.markdown(
        f"""
        <style>
        /* Global Styles */
        :root {{
            --bg-primary: {colors['bg_primary']};
            --bg-secondary: {colors['bg_secondary']};
            --bg-tertiary: {colors['bg_tertiary']};
            --text-primary: {colors['text_primary']};
            --text-secondary: {colors['text_secondary']};
            --accent-primary: {colors['accent_primary']};
            --accent-secondary: {colors['accent_secondary']};
            --accent-danger: {colors['accent_danger']};
            --border: {colors['border']};
            --shadow: {colors['shadow']};
        }}
        
        /* App Container */
        [data-testid="stAppViewContainer"] {{
            background: var(--bg-primary);
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background: var(--bg-tertiary);
            border-right: 1px solid var(--border);
        }}
        
        /* Glass Card Effect */
        .glass-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: var(--shadow);
            backdrop-filter: blur(10px);
            margin-bottom: 1rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .glass-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(74, 144, 226, 0.2);
        }}
        
        /* Result Card */
        .result-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }}
        
        .result-card::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .result-card:hover::before {{
            opacity: 1;
        }}
        
        .result-card:hover {{
            border-color: var(--accent-primary);
            transform: translateX(4px);
        }}
        
        /* Badges */
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .badge-primary {{
            background: rgba(74, 144, 226, 0.2);
            color: var(--accent-primary);
        }}
        
        .badge-success {{
            background: rgba(44, 177, 188, 0.2);
            color: var(--accent-secondary);
        }}
        
        .badge-warning {{
            background: rgba(255, 193, 7, 0.2);
            color: #FFC107;
        }}
        
        .badge-danger {{
            background: rgba(255, 107, 107, 0.2);
            color: var(--accent-danger);
        }}
        
        /* Progress Indicator */
        .progress-stage {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1rem;
            background: var(--bg-secondary);
            border-left: 3px solid var(--accent-primary);
            border-radius: 8px;
            margin-bottom: 0.5rem;
            animation: slideIn 0.3s ease;
        }}
        
        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateX(-20px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}
        
        .progress-spinner {{
            width: 16px;
            height: 16px;
            border: 2px solid var(--border);
            border-top-color: var(--accent-primary);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        
        /* Metric Cards */
        .metric-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        }}
        
        .metric-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent-primary);
            margin-bottom: 0.25rem;
        }}
        
        .metric-label {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        /* Log Entry */
        .log-entry {{
            font-family: 'Courier New', monospace;
            font-size: 0.8rem;
            padding: 0.5rem 0.75rem;
            background: var(--bg-tertiary);
            border-left: 2px solid var(--accent-secondary);
            border-radius: 4px;
            margin-bottom: 0.25rem;
            color: var(--text-secondary);
        }}
        
        /* Buttons */
        .stButton > button {{
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
        }}
        
        /* History Item */
        .history-item {{
            background: var(--bg-secondary);
            padding: 0.75rem;
            border-radius: 8px;
            border-left: 3px solid var(--accent-primary);
            margin-bottom: 0.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .history-item:hover {{
            background: var(--bg-tertiary);
            transform: translateX(4px);
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.5rem;
            background: var(--bg-tertiary);
            border-radius: 12px;
            padding: 0.5rem;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
        }}
        
        /* Voice Button */
        .voice-button {{
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        
        .voice-button:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(74, 144, 226, 0.4);
        }}
        
        /* Suggestion Chips */
        .suggestion-chip {{
            display: inline-block;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: 0.5rem 1rem;
            margin: 0.25rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .suggestion-chip:hover {{
            background: var(--accent-primary);
            color: white;
            transform: translateY(-2px);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# PROGRESS VISUALIZATION
# ============================================================================


def show_progress_stage(stage: str, message: str) -> None:
    """Display animated progress indicator."""
    emoji_map = {
        "searching": "🔍",
        "crawling": "🕷️",
        "ranking": "🧠",
        "summarizing": "📝",
        "complete": "✅",
        "error": "❌",
    }
    
    emoji = emoji_map.get(stage, "⚙️")
    
    st.markdown(
        f"""
        <div class="progress-stage">
            <div class="progress-spinner"></div>
            <div>
                <strong>{emoji} {stage.title()}</strong> - {message}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
# VOICE INPUT
# ============================================================================


def render_voice_input() -> Optional[str]:
    """Render voice input button with Web Speech API."""
    voice_html = """
    <button class="voice-button" onclick="startVoiceRecognition()">
        🎤 Voice Search
    </button>
    
    <script>
    function startVoiceRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            alert('Voice recognition is not supported in your browser. Please use Chrome or Edge.');
            return;
        }
        
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        
        recognition.onstart = function() {
            console.log('Voice recognition started. Speak now.');
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: transcript
            }, '*');
        };
        
        recognition.onerror = function(event) {
            console.error('Voice recognition error:', event.error);
            alert('Voice recognition error: ' + event.error);
        };
        
        recognition.start();
    }
    </script>
    """
    
    result = html(voice_html, height=50)
    return result


# ============================================================================
# HISTORY MANAGEMENT
# ============================================================================


def add_to_history(query: str, result_count: int) -> None:
    """Add search to history."""
    history_entry = {
        "query": query,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "result_count": result_count,
    }
    
    # Remove duplicate if exists
    st.session_state.search_history = [
        h for h in st.session_state.search_history if h["query"] != query
    ]
    
    # Add to beginning
    st.session_state.search_history.insert(0, history_entry)
    
    # Keep only last 20
    st.session_state.search_history = st.session_state.search_history[:20]


# ============================================================================
# LOGGING
# ============================================================================


def log_stage(stage: str, meta: Dict[str, Any]) -> None:
    """Log search stage progress."""
    log_entry = {
        "stage": stage,
        "meta": meta,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    st.session_state.logs.append(log_entry)
    
    # Keep last 500 logs
    st.session_state.logs = st.session_state.logs[-500:]
    
    # Update progress messages
    if stage in ["searching", "crawling", "ranking", "summarizing"]:
        st.session_state.current_stage = stage
        message = f"{stage.title()} - {meta.get('count', 0)} items"
        st.session_state.progress_messages.append(message)


# ============================================================================
# SEARCH EXECUTION
# ============================================================================


def run_search(query: str, options: SearchOptions) -> Dict[str, Any]:
    """Execute search with progress tracking."""
    service = SearchService(st.session_state.knowledge_base)
    
    # Progress callback
    def progress_callback(stage: str, meta: Dict[str, Any]) -> None:
        log_stage(stage, meta)
    
    payload = SearchPayload(query=query, options=options)
    
    try:
        # Handle async in Streamlit
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(
            service.run(payload, progress=progress_callback)
        )
        return result
        
    except Exception as exc:
        logger.exception("Search failed")
        raise


# ============================================================================
# SIDEBAR
# ============================================================================


def render_sidebar() -> None:
    """Render modern sidebar with controls and history."""
    with st.sidebar:
        # Header
        st.markdown("# ⚙️ Control Center")
        
        # Theme Toggle
        st.markdown("### 🎨 Appearance")
        theme_col1, theme_col2 = st.columns(2)
        
        with theme_col1:
            if st.button("🌙 Dark", use_container_width=True, disabled=st.session_state.theme_mode == "dark"):
                st.session_state.theme_mode = "dark"
                st.rerun()
        
        with theme_col2:
            if st.button("☀️ Light", use_container_width=True, disabled=st.session_state.theme_mode == "light"):
                st.session_state.theme_mode = "light"
                st.rerun()
        
        st.divider()
        
        # API Status
        st.markdown("### 🔑 API Status")
        from utils.secrets import get_secret
        
        serpapi_key = get_secret("SERPAPI_API_KEY")
        openai_key = get_secret("OPENAI_API_KEY")
        
        if serpapi_key:
            st.success("✅ SerpAPI Connected")
        else:
            st.error("❌ SerpAPI Not Configured")
            with st.expander("How to configure"):
                st.code("""
# In Streamlit Cloud:
# Go to App Settings > Secrets
# Add:
SERPAPI_API_KEY = "your-key"

# Locally, create .env:
SERPAPI_API_KEY=your-key
                """)
        
        if openai_key:
            st.success("✅ OpenAI Connected")
        else:
            st.error("❌ OpenAI Not Configured")
        
        st.divider()
        
        # Search History
        st.markdown("### 📜 Recent Searches")
        
        if st.session_state.search_history:
            for idx, item in enumerate(st.session_state.search_history[:5]):
                query_text = item["query"][:40] + ("..." if len(item["query"]) > 40 else "")
                
                if st.button(
                    f"🔍 {query_text}",
                    key=f"history_{idx}",
                    help=f"{item['result_count']} results - {item['timestamp']}",
                    use_container_width=True
                ):
                    st.session_state.query = item["query"]
                    st.rerun()
        else:
            st.info("No recent searches")
        
        st.divider()
        
        # Cache Info
        st.markdown("### 💾 Cache")
        cached_queries = list(cache.recent_queries(limit=3))
        
        if cached_queries:
            st.caption(f"{len(cached_queries)} cached queries")
            for snapshot in cached_queries:
                st.caption(f"• {snapshot.get('query', '')[:30]}")
        else:
            st.caption("No cached data")
        
        st.divider()
        
        # Knowledge Base
        st.markdown("### 📚 Knowledge Base")
        kb = st.session_state.knowledge_base
        
        if kb.has_documents:
            st.success(f"✅ {len(kb.documents)} documents")
            
            for doc in kb.documents[:3]:
                st.caption(f"📄 {doc.get('name', 'Unknown')}")
        else:
            st.info("No custom knowledge")
        
        st.divider()
        
        # App Info
        st.markdown("### ℹ️ About")
        st.caption("**QueryNova** v2.0")
        st.caption("AI-Powered Search Assistant")
        st.caption("Built with Streamlit Cloud")


# ============================================================================
# MAIN APP
# ============================================================================


def validate_api_keys() -> None:
    """Validate API keys are configured and show helpful warnings if not."""
    from utils.secrets import get_secret
    
    serpapi_key = get_secret("SERPAPI_API_KEY")
    openai_key = get_secret("OPENAI_API_KEY")
    
    issues = []
    warnings = []
    
    if not serpapi_key:
        issues.append("🔴 **SerpAPI Key Missing** - Web search will not work")
    
    if not openai_key:
        issues.append("🔴 **OpenAI Key Missing** - AI features will not work")
    else:
        # Check if OpenAI key has quota
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            # Quick test with minimal tokens
            client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=1
            )
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "insufficient_quota" in error_str or "quota" in error_str.lower():
                warnings.append("💳 **OpenAI Quota Exceeded** - AI features will use fallback mode")
                warnings.append("Add credits at: https://platform.openai.com/settings/organization/billing/overview")
    
    if issues:
        st.sidebar.error("⚠️ **Configuration Issues**")
        for issue in issues:
            st.sidebar.warning(issue)
        
        with st.sidebar.expander("📋 How to Fix"):
            st.markdown("""
            **Add your API keys to `.streamlit/secrets.toml`:**
            
            ```toml
            SERPAPI_API_KEY = "your-key-here"
            OPENAI_API_KEY = "sk-your-key-here"
            ```
            
            **Get API Keys:**
            - [SerpAPI](https://serpapi.com/) (100 free searches/month)
            - [OpenAI](https://platform.openai.com/api-keys)
            
            **Then restart the app.**
            """)
    
    if warnings:
        for warning in warnings:
            st.sidebar.warning(warning)


def main():
    """Main application entry point."""
    
    # Initialize
    initialize_session_state()
    
    # Validate API Keys on startup
    validate_api_keys()
    
    inject_modern_css()
    render_sidebar()
    
    # Header
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem;">
                🔍 QueryNova
            </h1>
            <p style="font-size: 1.2rem; color: var(--text-secondary);">
                AI-Powered Search & Research Assistant
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Search Input
    col1, col2 = st.columns([5, 1])
    
    with col1:
        query_input = st.text_input(
            "Search Query",
            value=st.session_state.query,
            placeholder="Ask anything... e.g., Latest developments in quantum computing",
            label_visibility="collapsed",
            key="main_query_input",
        )
    
    with col2:
        render_voice_input()
    
    # Action Buttons
    search_col, clear_col = st.columns([3, 1])
    
    with search_col:
        search_clicked = st.button("🚀 Search", type="primary", use_container_width=True)
    
    with clear_col:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.query = ""
            st.session_state.search_results = {}
            st.session_state.logs = []
            st.rerun()
    
    # Advanced Options
    with st.expander("⚙️ Advanced Options", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            max_results = st.slider("Max Results", 5, 30, 12, help="Number of search results to retrieve")
            use_cache = st.checkbox("Use Cache", value=True, help="Serve from cache if available")
        
        with col2:
            include_summary = st.checkbox("AI Summary", value=True, help="Generate AI summary")
            include_sentiment = st.checkbox("Sentiment Analysis", value=True)
            include_heatmap = st.checkbox("Semantic Heatmap", value=True)
        
        with col3:
            include_suggestions = st.checkbox("Query Suggestions", value=True)
            include_knowledge = st.checkbox("Use Knowledge Base", value=True)
            offline_mode = st.checkbox("Offline Mode", value=False, help="Use only cached data")
        
        # PDF Export disabled - focus on core features (Markdown/JSON work perfectly)
        include_pdf = False
        
        # Knowledge Base Upload
        st.markdown("#### 📚 Upload Custom Knowledge")
        upload_col1, upload_col2 = st.columns(2)
        
        with upload_col1:
            uploaded_file = st.file_uploader(
                "Upload Document",
                type=["txt", "pdf", "md"],
                help="Augment search with your own documents",
            )
            
            if uploaded_file:
                try:
                    content = uploaded_file.read()
                    st.session_state.knowledge_base.ingest_file(uploaded_file.name, content)
                    st.success(f"✅ Ingested {uploaded_file.name}")
                except Exception as e:
                    st.error(f"❌ Failed to ingest: {e}")
        
        with upload_col2:
            kb_url = st.text_input("Or Import from URL", placeholder="https://example.com/article")
            
            if st.button("Import URL", use_container_width=True) and kb_url:
                try:
                    st.session_state.knowledge_base.ingest_url(kb_url)
                    st.success("✅ URL content imported")
                except Exception as e:
                    st.error(f"❌ Import failed: {e}")
    
    # Execute Search
    if search_clicked and query_input.strip():
        st.session_state.query = query_input.strip()
        st.session_state.progress_messages = []
        st.session_state.current_stage = None
        
        # Create options
        options = SearchOptions(
            limit=max_results,
            use_cache=use_cache,
            include_summary=include_summary,
            include_sentiment=include_sentiment,
            include_heatmap=include_heatmap,
            include_suggestions=include_suggestions,
            include_knowledge=include_knowledge,
            offline_mode=offline_mode,
            include_pdf=include_pdf,
        )
        
        # Progress container
        progress_container = st.container()
        
        with progress_container:
            with st.spinner("🔍 Initializing search..."):
                try:
                    result = run_search(st.session_state.query, options)
                    st.session_state.search_results = result
                    
                    # Add to history
                    ranked_count = len(result.get("ranked", []))
                    add_to_history(st.session_state.query, ranked_count)
                    
                    # Show messages
                    for msg in result.get("messages", []):
                        level = msg.get("level", "info")
                        text = msg.get("text", "")
                        
                        if level == "error":
                            st.error(text)
                        elif level == "warning":
                            st.warning(text)
                        else:
                            st.info(text)
                    
                    if ranked_count > 0:
                        st.success(f"✅ Search complete! Found {ranked_count} results")
                    
                except Exception as e:
                    st.error(f"❌ Search failed: {str(e)}")
                    logger.exception("Search execution failed")
    
    elif search_clicked:
        st.warning("⚠️ Please enter a search query")
    
    # ========================================================================
    # RESULTS DISPLAY
    # ========================================================================
    
    st.divider()
    
    # Check if we have results
    if st.session_state.search_results:
        results = st.session_state.search_results
        ranked = results.get("ranked", [])
        
        # Metrics Row
        if ranked:
            metrics_cols = st.columns(4)
            
            with metrics_cols[0]:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-value">{len(ranked)}</div>
                        <div class="metric-label">Results</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            
            with metrics_cols[1]:
                avg_score = sum(r.get("score", 0) for r in ranked) / len(ranked) if ranked else 0
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-value">{avg_score:.0%}</div>
                        <div class="metric-label">Avg Relevance</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            
            with metrics_cols[2]:
                high_conf = sum(1 for r in ranked if r.get("reliability", 0) > 0.8)
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-value">{high_conf}</div>
                        <div class="metric-label">High Quality</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            
            with metrics_cols[3]:
                kb_docs = len(st.session_state.knowledge_base.documents)
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-value">{kb_docs}</div>
                        <div class="metric-label">KB Docs</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tabbed Interface
        tab_results, tab_summary, tab_suggestions, tab_logs, tab_export = st.tabs([
            "🔍 Results",
            "🧠 AI Summary",
            "💡 Suggestions",
            "📋 Logs",
            "📥 Export"
        ])
        
        # TAB 1: Search Results
        with tab_results:
            if not ranked:
                st.info("No results found. Try adjusting your query or check API configuration.")
            else:
                for idx, item in enumerate(ranked, 1):
                    # Result Card
                    st.markdown(
                        f"""
                        <div class="result-card">
                            <h3 style="margin-bottom: 0.5rem;">
                                {idx}. <a href="{item.get('url', '#')}" target="_blank" style="color: var(--accent-primary); text-decoration: none;">
                                    {item.get('title', 'Untitled')}
                                </a>
                            </h3>
                        """,
                        unsafe_allow_html=True,
                    )
                    
                    # Badges
                    badge_html = ""
                    score = item.get("score", 0)
                    reliability = item.get("reliability", 0)
                    
                    if score >= 0.8:
                        badge_html += '<span class="badge badge-success">High Relevance</span>'
                    elif score >= 0.5:
                        badge_html += '<span class="badge badge-primary">Medium Relevance</span>'
                    else:
                        badge_html += '<span class="badge badge-warning">Low Relevance</span>'
                    
                    badge_html += f'<span class="badge badge-primary">Score: {score:.0%}</span>'
                    badge_html += f'<span class="badge badge-success">Reliability: {reliability:.0%}</span>'
                    
                    st.markdown(badge_html, unsafe_allow_html=True)
                    
                    # Summary
                    summary = item.get("summary", "No summary available")
                    st.markdown(f"**Summary:** {summary}")
                    
                    # Insight
                    insight = item.get("insight", "")
                    if insight:
                        st.markdown(f"💡 **Insight:** {insight}")
                    
                    # Knowledge Snippets
                    snippets = item.get("snippets", [])
                    if snippets:
                        with st.expander("📚 Knowledge Base Context"):
                            for snippet in snippets:
                                st.code(snippet.get("snippet", ""), language="text")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Heatmap
                if results.get("heatmap"):
                    st.markdown("### 🗺️ Semantic Similarity Heatmap")
                    heatmap_data = results["heatmap"]
                    
                    fig = go.Figure(
                        data=go.Heatmap(
                            z=[heatmap_data["values"]],
                            x=heatmap_data["labels"],
                            y=["Relevance"],
                            colorscale="Viridis",
                            showscale=True,
                        )
                    )
                    
                    fig.update_layout(
                        height=250,
                        margin=dict(l=10, r=10, t=30, b=10),
                        xaxis=dict(tickangle=-45),
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        
        # TAB 2: AI Summary
        with tab_summary:
            summary = results.get("summary")
            insights = results.get("insights", [])
            sentiment = results.get("sentiment")
            
            if not summary and not insights:
                st.info("No AI summary available. Enable 'AI Summary' in advanced options.")
            else:
                st.markdown("### 📝 Executive Summary")
                
                if summary:
                    st.markdown(
                        f"""
                        <div class="glass-card">
                            <p style="font-size: 1.1rem; line-height: 1.6;">{summary}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                
                if insights:
                    st.markdown("### 💡 Key Insights")
                    for insight in insights:
                        st.markdown(f"- {insight}")
                
                if sentiment:
                    st.markdown("### 😊 Sentiment Analysis")
                    
                    sent_cols = st.columns(3)
                    
                    with sent_cols[0]:
                        pos = sentiment.get("positive", 0)
                        st.metric("Positive", f"{pos:.1%}")
                    
                    with sent_cols[1]:
                        neu = sentiment.get("neutral", 0)
                        st.metric("Neutral", f"{neu:.1%}")
                    
                    with sent_cols[2]:
                        neg = sentiment.get("negative", 0)
                        st.metric("Negative", f"{neg:.1%}")
        
        # TAB 3: Suggestions
        with tab_suggestions:
            suggestions = results.get("suggestions", [])
            
            if not suggestions:
                st.info("No query suggestions available.")
            else:
                st.markdown("### 🔎 Related Searches")
                st.caption("Click to search:")
                
                for suggestion in suggestions:
                    if st.button(suggestion, key=f"suggest_{suggestion}", use_container_width=True):
                        st.session_state.query = suggestion
                        st.rerun()
        
        # TAB 4: Logs
        with tab_logs:
            st.markdown("### 📋 Search Process Log")
            
            if not st.session_state.logs:
                st.info("No logs available")
            else:
                for log in reversed(st.session_state.logs[-50:]):
                    stage = log.get("stage", "unknown")
                    meta = json.dumps(log.get("meta", {}))
                    timestamp = log.get("timestamp", "")
                    
                    st.markdown(
                        f"""
                        <div class="log-entry">
                            [{timestamp}] <strong>{stage.upper()}</strong>: {meta}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        
        # TAB 5: Export
        with tab_export:
            st.markdown("### 📥 Export Results")
            
            exports = results.get("exports", {})
            
            if not exports:
                st.info("No export bundles available")
            else:
                export_cols = st.columns(len(exports))
                
                for idx, (name, content) in enumerate(exports.items()):
                    with export_cols[idx]:
                        file_icon = "📄"
                        if name.endswith(".pdf"):
                            file_icon = "📕"
                        elif name.endswith(".json"):
                            file_icon = "📊"
                        elif name.endswith(".md"):
                            file_icon = "📝"
                        
                        st.download_button(
                            f"{file_icon} {name}",
                            data=content,
                            file_name=name,
                            use_container_width=True,
                        )
                
                # Copy to clipboard
                st.markdown("#### 📋 Copy Summary")
                if summary:
                    st.code(summary, language="text")
    
    else:
        # Empty State
        st.markdown(
            """
            <div style="text-align: center; padding: 4rem 2rem;">
                <h2 style="color: var(--text-secondary); margin-bottom: 1rem;">
                    Ready to explore
                </h2>
                <p style="font-size: 1.1rem; color: var(--text-secondary);">
                    Enter a query above to start your AI-powered search journey
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style="text-align: center; padding: 1rem; color: var(--text-secondary);">
            <p>Powered by <strong>SerpAPI</strong> × <strong>OpenAI</strong> × <strong>Streamlit Cloud</strong></p>
            <p style="font-size: 0.875rem;">QueryNova v2.0 - AI-Powered Research Assistant</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
