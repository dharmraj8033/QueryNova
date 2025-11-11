from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict

import plotly.graph_objects as go
import streamlit as st
import yaml
from streamlit.components.v1 import html

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.services.knowledge_base import KnowledgeBase
from src.services.search_service import SearchOptions, SearchPayload, SearchService
from src.utils import cache
from src.utils.logger import logger


st.set_page_config(
    page_title="QueryNova - Next-Gen AI Research",
    page_icon=":mag:",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def load_theme() -> Dict[str, Dict[str, str]]:
    theme_path = os.path.join(os.path.dirname(__file__), "theme_config.yaml")
    if not os.path.exists(theme_path):
        return {}
    with open(theme_path, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return data.get("presets", {})


THEMES = load_theme()
DEFAULT_THEME = "dark" if "dark" in THEMES else next(iter(THEMES.keys()), "")


def ensure_state() -> None:
    st.session_state.setdefault("theme", DEFAULT_THEME or "dark")
    st.session_state.setdefault("query", "")
    st.session_state.setdefault("search_results", {})
    st.session_state.setdefault("search_history", [])
    st.session_state.setdefault("logs", [])
    if "knowledge_base" not in st.session_state:
        st.session_state["knowledge_base"] = KnowledgeBase()


def inject_css(theme: Dict[str, str]) -> None:
    st.markdown(
        f"""
        <style>
        :root {{
            --bg: {theme.get('background', '#0B0F1C')};
            --surface: {theme.get('surface', 'rgba(21, 28, 43, 0.65)')};
            --primary: {theme.get('primary', '#7A5AF5')};
            --secondary: {theme.get('secondary', '#2CB1BC')};
            --accent: {theme.get('accent', '#FF6B6B')};
            --text: {theme.get('text', '#F5F6FF')};
            --muted: {theme.get('muted_text', '#A0A8C3')};
            --border: {theme.get('border', 'rgba(122, 90, 245, 0.35)')};
            --shadow: {theme.get('shadow', '0 16px 40px rgba(12, 19, 31, 0.55)')};
        }}
        [data-testid="stAppViewContainer"] {{
            background: var(--bg);
        }}
        [data-testid="stSidebar"] {{
            background: rgba(8, 11, 22, 0.82);
            backdrop-filter: blur(20px);
        }}
        .glass {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 18px;
            box-shadow: var(--shadow);
            padding: 1.25rem 1.5rem;
            backdrop-filter: blur(18px);
        }}
        .result-card {{
            position: relative;
            margin-bottom: 1rem;
        }}
        .result-card::before {{
            content: "";
            position: absolute;
            inset: 0;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(122, 90, 245, 0.16), rgba(44, 177, 188, 0.18));
            opacity: 0;
            transition: opacity .25s ease;
        }}
        .result-card:hover::before {{
            opacity: 1;
        }}
        .result-card > div {{
            position: relative;
        }}
        .insight-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.2rem 0.75rem;
            border-radius: 999px;
            font-size: 0.75rem;
            background: rgba(44, 177, 188, 0.18);
            color: var(--secondary);
        }}
        .reliability-badge {{
            font-size: 0.72rem;
            padding: 0.2rem 0.6rem;
            margin-left: 0.5rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.12);
        }}
        .score-chip {{
            font-size: 0.75rem;
            padding: 0.2rem 0.6rem;
            margin-left: 0.5rem;
            border-radius: 999px;
            background: rgba(122, 90, 245, 0.24);
            color: var(--primary);
        }}
        .log-entry {{
            font-family: "SFMono-Regular", Menlo, monospace;
            font-size: 0.78rem;
            color: var(--muted);
        }}
        .voice-trigger {{
            border: 1px dashed var(--secondary);
            border-radius: 999px;
            padding: 0.4rem 0.9rem;
            color: var(--secondary);
            background: transparent;
            cursor: pointer;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_voice_input(target_key: str) -> None:
    html(
    f"""
    <button class='voice-trigger' onclick="window.queryNovaDictate('{target_key}')">Voice Input</button>
        <script>
        window.queryNovaDictate = function(key) {{
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {{
                alert('Speech recognition not supported in this browser.');
                return;
            }}
            const recognition = new SpeechRecognition();
            recognition.lang = 'en-US';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;
            recognition.onresult = function(event) {{
                window.parent.postMessage({{
                    isStreamlitMessage: true,
                    type: 'STREAMLIT_SET_COMPONENT_VALUE',
                    key,
                    value: event.results[0][0].transcript,
                }}, '*');
            }};
            recognition.start();
        }};
        </script>
        """,
        height=70,
    )


def add_to_history(query: str, count: int) -> None:
    st.session_state.search_history.insert(0, {
        "query": query,
        "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S"),
        "results": count,
    })
    st.session_state.search_history = st.session_state.search_history[:20]


def log_stage(stage: str, meta: Dict[str, Any]) -> None:
    st.session_state.logs.append({
        "stage": stage,
        "meta": meta,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    st.session_state.logs = st.session_state.logs[-250:]


def run_search(query: str, options: SearchOptions) -> Dict[str, Any]:
    service = SearchService(st.session_state.knowledge_base)

    def progress(stage: str, meta: Dict[str, Any]) -> None:
        log_stage(stage, meta)
        if stage in {"complete", "error"}:
            message = "Search complete" if stage == "complete" else "Search error"
            st.toast(message)

    payload = SearchPayload(query=query, options=options)
    try:
        return asyncio.run(service.run(payload, progress=progress))
    except RuntimeError as exc:
        if "asyncio.run()" in str(exc):
            loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(loop)
                return loop.run_until_complete(service.run(payload, progress=progress))
            finally:
                asyncio.set_event_loop(None)
                loop.close()
        raise


def ensure_state_and_theme() -> None:
    ensure_state()
    inject_css(THEMES.get(st.session_state.theme, {}))


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("## Control Center")
        if THEMES:
            current_index = list(THEMES.keys()).index(st.session_state.theme)
            selected = st.radio("Theme", options=list(THEMES.keys()), index=current_index)
            if selected != st.session_state.theme:
                st.session_state.theme = selected
                st.rerun()

        st.markdown("### API keys")
        st.text_input("SerpAPI", value=os.getenv("SERPAPI_API_KEY", ""), type="password")
        st.text_input("OpenAI", value=os.getenv("OPENAI_API_KEY", ""), type="password")

        st.markdown("### Recent searches")
        for item in st.session_state.search_history[:6]:
            if st.button(item["query"][:40], key=f"hist-{item['timestamp']}"):
                st.session_state.query = item["query"]
                st.rerun()

        st.markdown("### Cached snapshots")
        for snapshot in cache.recent_queries(limit=4):
            created_at = snapshot.get("created_at", "")
            try:
                parsed = datetime.fromisoformat(created_at)
                created_display = parsed.astimezone().strftime("%b %d %H:%M")
            except Exception:
                created_display = created_at
            st.caption(f"{snapshot['query']} | {created_display}")

        exports = st.session_state.search_results.get("exports")
        if exports:
            st.markdown("### Export bundles")
            for name, blob in exports.items():
                st.download_button(f"Download {name}", blob, file_name=name)


ensure_state_and_theme()
render_sidebar()

st.title("QueryNova")
st.caption("An AI-native research cockpit for analysts and strategists.")

query_value = st.text_input(
    "Search Query",
    value=st.session_state.query,
    placeholder="Summarize the latest breakthroughs in quantum computing",
    key="query_input",
)

action_cols = st.columns(2)
with action_cols[0]:
    trigger_search = st.button("Launch", use_container_width=True)
with action_cols[1]:
    render_voice_input("query_input")

advanced = st.expander("Advanced options", expanded=False)
with advanced:
    slider_col, toggle_col = st.columns(2)
    with slider_col:
        limit = st.slider("Results", min_value=5, max_value=30, value=12)
    with toggle_col:
        use_cache = st.checkbox("Use cache", value=True)
        include_heatmap = st.checkbox("Heatmap", value=True)
        offline_mode = st.checkbox("Offline mode", value=False)
        include_pdf = st.checkbox("Enable PDF export", value=False, help="Generate PDF reports (may fail for some content unless a TTF font is added)")

    kb_cols = st.columns(2)
    with kb_cols[0]:
        uploaded = st.file_uploader(
            "Custom knowledge",
            type=["pdf", "txt"],
            help="Augment search with proprietary research.",
        )
        if uploaded is not None:
            st.session_state.knowledge_base.ingest_file(uploaded.name, uploaded.read())
            st.toast(f"Ingested {uploaded.name}")
    with kb_cols[1]:
        kb_url = st.text_input("Capture URL")
        if st.button("Import URL") and kb_url:
            try:
                st.session_state.knowledge_base.ingest_url(kb_url)
                st.toast("Knowledge URL imported")
            except Exception as exc:
                st.error(f"Failed to import: {exc}")


if trigger_search and query_value.strip():
    st.session_state.query = query_value.strip()
    options = SearchOptions(
        limit=limit,
        use_cache=use_cache,
        include_heatmap=include_heatmap,
        include_sentiment=True,
        include_summary=True,
        include_suggestions=True,
        include_knowledge=True,
        offline_mode=offline_mode,
        include_pdf=include_pdf,
    )
    result: Dict[str, Any] | None = None
    with st.spinner("Synthesizing intelligence..."):
        try:
            result = run_search(query_value, options)
        except Exception as exc:
            logger.exception("Search failed")
            st.error(f"Search failed: {exc}")
    if result:
        st.session_state.search_results = result
        add_to_history(query_value, len(result.get("ranked", [])))
        for message in result.get("messages", []):
            level = message.get("level", "info")
            text = message.get("text", "")
            notifier = getattr(st, level, st.info)
            notifier(text)
        if result.get("ranked"):
            st.toast("Search complete")
elif trigger_search:
    st.warning("Enter a query to continue.")


search_tab, summary_tab, log_tab, settings_tab = st.tabs([
    "Search",
    "AI Summary",
    "Crawl Log",
    "Settings",
])

with search_tab:
    ranked = st.session_state.search_results.get("ranked", [])
    if not ranked:
        st.info("Ready when you are. Launch a query to populate this workspace.")
    else:
        avg_score = (
            sum(r.get("score", 0) for r in ranked) / len(ranked)
            if ranked
            else 0
        )
        metrics_data = [
            ("Results", str(len(ranked))),
            ("Avg score", f"{avg_score:.0%}"),
            ("High confidence", str(sum(r.get("reliability", 0) > 0.8 for r in ranked))),
            ("Knowledge docs", str(len(st.session_state.knowledge_base.documents))),
        ]
        for row_start in range(0, len(metrics_data), 2):
            row_items = metrics_data[row_start:row_start + 2]
            row_cols = st.columns(len(row_items))
            for col, (label, value) in zip(row_cols, row_items):
                col.metric(label, value)

        for idx, item in enumerate(ranked, 1):
            with st.container():
                st.markdown("<div class='glass result-card'>", unsafe_allow_html=True)
                st.markdown(
                    f"**{idx}. [{item.get('title', 'Untitled')}]({item.get('url')})**",
                )
                if item.get("insight"):
                    st.markdown(
                        f"<span class='insight-badge'>{item['insight']}</span>",
                        unsafe_allow_html=True,
                    )
                st.markdown(
                    (
                        f"<span class='reliability-badge'>Reliability {item.get('reliability', 0):.2f}</span>"
                        f"<span class='score-chip'>Score {item.get('score', 0):.0%}</span>"
                    ),
                    unsafe_allow_html=True,
                )
                st.write(item.get("summary", "No summary available."))
                if item.get("snippets"):
                    st.caption("Custom knowledge context")
                    for snippet in item["snippets"]:
                        st.code(snippet["snippet"])
                st.markdown("</div>", unsafe_allow_html=True)

        suggestions = st.session_state.search_results.get("suggestions", [])
        if suggestions:
            st.markdown("### Suggested refinements")
            suggestions_per_row = 2
            for row_start in range(0, len(suggestions), suggestions_per_row):
                row_items = suggestions[row_start:row_start + suggestions_per_row]
                row_cols = st.columns(len(row_items))
                for col, suggestion in zip(row_cols, row_items):
                    if col.button(suggestion, key=f"suggestion-{row_start}-{suggestion}"):
                        st.session_state.query = suggestion
                        st.rerun()

        if include_heatmap and st.session_state.search_results.get("heatmap"):
            heatmap = st.session_state.search_results["heatmap"]
            fig = go.Figure(
                data=go.Heatmap(
                    z=heatmap["values"],
                    x=heatmap["labels"],
                    y=["Semantic proximity"],
                    colorscale="Viridis",
                )
            )
            fig.update_layout(height=320, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)


with summary_tab:
    summary = st.session_state.search_results.get("summary")
    insights = st.session_state.search_results.get("insights", [])
    sentiment = st.session_state.search_results.get("sentiment")
    if not summary:
        st.info("Run a search to unlock the AI narrative.")
    else:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown("### Executive summary")
        st.write(summary)
        if insights:
            st.markdown("### Insight bullets")
            for insight in insights:
                st.markdown(f"- {insight}")
        if sentiment:
            st.markdown("### Sentiment profile")
            st.json(sentiment)
        st.markdown("</div>", unsafe_allow_html=True)


with log_tab:
    st.markdown("### Live crawl + ranking log")
    for entry in st.session_state.logs[-200:]:
        meta_json = json.dumps(entry["meta"], ensure_ascii=False)
        st.markdown(
            f"<div class='log-entry'>[{entry['timestamp']}] {entry['stage'].upper()} :: {meta_json}</div>",
            unsafe_allow_html=True,
        )


with settings_tab:
    st.markdown("### Workspace settings")
    st.write("Team mode, shared notes, and plugin management are on the roadmap.")
    st.markdown("### Plugin API")
    st.write("Register crawlers or renderers via `src/plugins/registry.py`.")


st.caption("Powered by SerpAPI | OpenAI | QueryNova Knowledge Base")
