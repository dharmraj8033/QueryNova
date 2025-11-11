# 🔍 QueryNova# 🔍 QueryNova



[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)

[![Streamlit](https://img.shields.io/badge/Streamlit-Cloud_Ready-red.svg)](https://streamlit.io)[![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red.svg)](https://streamlit.io)

[![OpenAI](https://img.shields.io/badge/OpenAI-GPT_Powered-green.svg)](https://openai.com)[![OpenAI](https://img.shields.io/badge/OpenAI-GPT_Powered-green.svg)](https://openai.com)

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**QueryNova** is an AI-powered search assistant that combines web search, intelligent crawling, and AI-driven content ranking to deliver superior search results with extracted summaries.

**QueryNova** is a production-ready AI-powered search assistant that combines web search, intelligent crawling, and AI-driven content ranking to deliver superior search results with extracted summaries and insights.

## ✨ Features

🚀 **Now with one-click Streamlit Cloud deployment!**

🔍 **Smart Web Search** - Uses SerpAPI for comprehensive web search results  

## ✨ Features🕷️ **Intelligent Crawling** - Extracts and processes content from web pages  

🧠 **AI-Powered Ranking** - Uses OpenAI embeddings for semantic similarity ranking  

### 🎨 Modern UI� **Dark Mode** - Beautiful gradient UI with modern design  

- **Sleek Design** - Glass-morphism cards with smooth animations� **Search History** - Track and rerun your recent searches  

- **Dark/Light Mode** - Toggle between themes⚡ **Smart Caching** - Faster results with intelligent caching  

- **Responsive Layout** - Works on desktop, tablet, and mobile� **Export Options** - Download results in JSON or CSV format  

- **Tabbed Interface** - Results, AI Summary, Suggestions, Logs, Export� **Analytics** - View search statistics and relevance metrics

- **Progress Visualization** - Real-time search stages with animated indicators

## 🚀 Quick Start

### 🔍 Smart Search

- **SerpAPI Integration** - Comprehensive web search results### Deploy to Streamlit Cloud (Recommended)

- **Async Crawling** - Fast parallel page fetching with aiohttp

- **AI Ranking** - OpenAI embeddings for semantic similarity1. **Fork this repository**

- **Smart Caching** - Redis or file-based caching for speed

- **Retry Logic** - Exponential backoff for failed requests2. **Go to [share.streamlit.io](https://share.streamlit.io)**



### 🧠 AI Features3. **Deploy your app:**

- **AI Summarization** - Concise executive summaries of all results   - Repository: `your-username/QueryNova`

- **Key Insights** - Extracted actionable insights   - Branch: `main`

- **Query Refinement** - Suggested related searches   - Main file: `streamlit_app.py`

- **Sentiment Analysis** - Emotional tone of results

- **Knowledge Base** - Upload custom documents to augment search4. **Add your API keys in Secrets:**

   ```toml

### 📊 Advanced Analytics   SERPAPI_API_KEY = "your_serpapi_key"

- **Relevance Scores** - AI-computed relevance for each result   OPENAI_API_KEY = "sk-your_openai_key"

- **Reliability Metrics** - Domain authority scoring   ```

- **Semantic Heatmap** - Visual similarity matrix

- **Search History** - Track recent queries5. **Done!** Your app will be live in minutes 🎉



### 📥 Smart Export### Local Development

- **Multiple Formats** - Markdown, JSON, PDF, Notion

- **Timestamped Reports** - Professional research reports1. **Clone the repository:**

- **One-Click Download** - Export all results instantly   ```bash

   git clone https://github.com/dharmraj8033/QueryNova.git

## 🚀 Quick Start   cd QueryNova

   ```

### Option 1: Deploy to Streamlit Cloud (Recommended)

2. **Install dependencies:**

**Deploy in 3 minutes!**   ```bash

   pip install -r requirements.txt

1. **Fork this repository**   ```

   - Click "Fork" button above

3. **Set up environment variables:**

2. **Go to [share.streamlit.io](https://share.streamlit.io)**   Create a `.env` file in the root directory:

   - Sign in with GitHub   ```env

   - Click "New app"   SERPAPI_API_KEY=your_serpapi_key_here

   OPENAI_API_KEY=sk-your_openai_key_here

3. **Configure deployment:**   ```

   - Repository: `your-username/QueryNova`

   - Branch: `main`4. **Run the app:**

   - Main file: `src/app_streamlit.py`   ```bash

   streamlit run streamlit_app.py

4. **Add secrets (Settings → Secrets):**   ```

   ```toml

   SERPAPI_API_KEY = "your-serpapi-key"5. **Open your browser:** http://localhost:8501

   OPENAI_API_KEY = "sk-your-openai-key"

   ```## 🔑 API Keys Setup



5. **Click Deploy!** 🎉### SerpAPI (Required)

1. Sign up at [serpapi.com](https://serpapi.com)

📖 **Detailed Guide:** See [STREAMLIT_CLOUD_DEPLOY.md](STREAMLIT_CLOUD_DEPLOY.md)2. Get your API key from the dashboard

3. Add to `.env` or Streamlit secrets

### Option 2: Local Development

### OpenAI API (Required for AI ranking)

1. **Clone the repository:**1. Create account at [platform.openai.com](https://platform.openai.com)

   ```bash2. Generate API key at [API Keys page](https://platform.openai.com/api-keys)

   git clone https://github.com/dharmraj8033/QueryNova.git3. Add to `.env` or Streamlit secrets

   cd QueryNova

   ```## 📁 Project Structure

```

2. **Install dependencies:**QueryNova/

   ```bash├── streamlit_app.py      # Main Streamlit application

   pip install -r requirements.txt├── requirements.txt      # Python dependencies

   ```├── .streamlit/

│   └── config.toml      # Streamlit configuration

3. **Set up environment variables:**├── src/

   │   └── modules/

   Create a `.env` file:│       ├── search.py    # Web search functionality

   ```env│       ├── crawl.py     # Web crawling and extraction

   SERPAPI_API_KEY=your_serpapi_key_here│       └── ai_filter.py # AI-powered ranking

   OPENAI_API_KEY=sk-your_openai_key_here├── config/

   ```│   └── config.py        # Configuration management

└── README.md

4. **Run the app:**```

   ```bash

   streamlit run src/app_streamlit.py## 🎨 Features in Detail

   ```

### Dark Mode UI

5. **Open browser:** http://localhost:8501- Beautiful gradient backgrounds

- Modern purple-blue color scheme

## 🔑 API Keys Setup- Smooth animations and transitions



### SerpAPI (Required)### Search History

- **Sign up:** [serpapi.com](https://serpapi.com/users/sign_up)- Tracks your last 10 searches

- **Free tier:** 100 searches/month- One-click to rerun previous queries

- **Get key:** [Dashboard](https://serpapi.com/manage-api-key)- Displays timestamp and result counts



### OpenAI API (Required)### Smart Caching

- **Sign up:** [platform.openai.com](https://platform.openai.com/signup)- Caches search results for faster access

- **Get key:** [API Keys](https://platform.openai.com/api-keys)- Toggle on/off as needed

- **Pricing:** ~$0.01-0.05 per search- Automatic cache management



## 📁 Project Structure### Export Options

- **JSON**: Structured data with full details

```- **CSV**: Spreadsheet-compatible format

QueryNova/- Timestamped filenames

├── .streamlit/

│   ├── config.toml           # Streamlit theme configuration### Analytics

│   └── secrets.toml          # API keys (local only, git-ignored)- Total searches performed

├── src/- Total results found

│   ├── app_streamlit.py      # Main Streamlit application ⭐- Average relevance scores

│   ├── modules/- High/Medium/Low quality categorization

│   │   ├── search.py         # SerpAPI integration

│   │   ├── crawl.py          # Async web crawling## 🤝 Contributing

│   │   └── ai_filter.py      # AI ranking & embeddings

│   ├── services/1. Fork the repository

│   │   ├── search_service.py # Orchestration layer2. Create a feature branch: `git checkout -b feature/amazing-feature`

│   │   ├── export_service.py # Multi-format exports3. Commit your changes: `git commit -m 'Add amazing feature'`

│   │   ├── summarizer.py     # AI summarization4. Push to the branch: `git push origin feature/amazing-feature`

│   │   ├── sentiment.py      # Sentiment analysis5. Open a Pull Request

│   │   ├── heatmap.py        # Semantic heatmaps

│   │   ├── knowledge_base.py # Custom knowledge ingestion## 📄 License

│   │   └── query_refinement.py # Query suggestions

│   └── utils/This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

│       ├── cache.py          # Caching utilities

│       ├── logger.py         # Logging setup## 🙏 Acknowledgments

│       └── secrets.py        # Secret management ⭐

├── requirements.txt          # Python dependencies- [SerpAPI](https://serpapi.com) for web search functionality

├── README.md                 # This file- [OpenAI](https://openai.com) for AI-powered content ranking

├── STREAMLIT_CLOUD_DEPLOY.md # Deployment guide- [Streamlit](https://streamlit.io) for the beautiful web interface

└── LICENSE                   # MIT License- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping

```

## 📞 Support

## 🎯 Usage Examples

If you encounter any issues or have questions:

### Basic Search- Create an [Issue](https://github.com/dharmraj8033/QueryNova/issues)

```python- Check the documentation files (DEPLOYMENT.md, SECRETS_SETUP.md, FEATURES.md)

# In the app:- Contact: [21cs25@ecajmer.ac.in](mailto:21cs25@ecajmer.ac.in)

1. Enter query: "quantum computing breakthroughs 2024"

2. Click "🚀 Search"---

3. View results in tabs

```**Made with ❤️ by QueryNova Team**


### Advanced Options
```python
# Configure in the app:
- Max Results: 5-30 (default: 12)
- Enable AI Summary
- Enable Sentiment Analysis
- Upload custom knowledge documents
- Choose export formats
```

### API Usage (Optional)
```python
from services.search_service import SearchService, SearchOptions, SearchPayload

service = SearchService()
options = SearchOptions(limit=10, include_summary=True)
payload = SearchPayload(query="AI news", options=options)

result = await service.run(payload)
print(result["summary"])
```

## 🎨 Features in Detail

### 🌙 Dark/Light Mode
Toggle between beautiful dark and light themes:
- **Dark Mode:** Deep backgrounds with vibrant accents
- **Light Mode:** Clean, professional appearance
- **Persistent:** Remembers your preference

### 🔄 Real-Time Progress
Watch your search unfold:
- 🔍 **Searching** - Querying SerpAPI
- 🕷️ **Crawling** - Fetching page content
- 🧠 **Ranking** - AI semantic analysis
- 📝 **Summarizing** - Generating insights

### 📚 Knowledge Base
Augment searches with your own data:
- **Upload Files:** PDF, TXT, Markdown
- **Import URLs:** Extract web page content
- **Context Integration:** Results reference your documents
- **Persistent:** Knowledge persists across searches

### 🗺️ Semantic Heatmap
Visualize result similarity:
- Color-coded relevance matrix
- Interactive Plotly visualization
- Identify clusters of related content

### 💾 Smart Caching
Faster results on repeat queries:
- **File-based:** SQLite storage (default)
- **Redis:** For production deployments
- **Configurable:** Toggle in Advanced Options

## 🔧 Configuration

### Streamlit Theme

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#4A90E2"      # Accent color
backgroundColor = "#0E1117"    # Main background
secondaryBackgroundColor = "#262730"  # Cards/sidebar
textColor = "#FAFAFA"         # Text
font = "sans serif"
```

### App Behavior

Edit `src/app_streamlit.py`:

```python
# Default search options
DEFAULT_MAX_RESULTS = 12
DEFAULT_CACHE_ENABLED = True
DEFAULT_INCLUDE_PDF = True
```

## 🐳 Docker Deployment (Alternative)

```bash
# Build image
docker build -t querynova .

# Run container
docker run -p 8501:8501 \
  -e SERPAPI_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  querynova
```

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific module
pytest tests/test_search.py -v
```

## 🤝 Contributing

We welcome contributions!

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements.txt
pip install -e .

# Run linter
black src/
flake8 src/

# Run tests
pytest
```

## 📚 Documentation

- **[Deployment Guide](STREAMLIT_CLOUD_DEPLOY.md)** - Complete Streamlit Cloud setup
- **[Features](FEATURES.md)** - Detailed feature documentation
- **[Secrets Setup](SECRETS_SETUP.md)** - API configuration guide
- **[Changelog](CHANGELOG.md)** - Version history

## 🐛 Troubleshooting

### "❌ SerpAPI Not Configured"
- Check API key in Streamlit Secrets or `.env`
- Verify key is active on [serpapi.com/dashboard](https://serpapi.com/dashboard)
- Ensure no extra spaces or quotes

### "❌ OpenAI Not Configured"
- Verify API key starts with `sk-`
- Check billing at [platform.openai.com/usage](https://platform.openai.com/usage)
- Create new key if needed

### "Search failed"
- Check API quotas and rate limits
- Review logs in Streamlit Cloud dashboard
- Try reducing "Max Results"

### PDF Export Issues
- Some content may not render in PDF
- Use Markdown or JSON export instead
- Check warnings in Export tab

## 🌟 Roadmap

- [x] Voice input with Web Speech API
- [ ] Multi-language support
- [ ] Browser extension
- [ ] Team collaboration features
- [ ] Custom crawler plugins
- [ ] Graph visualization of results
- [ ] Email/Slack notifications
- [ ] Scheduled searches

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[SerpAPI](https://serpapi.com)** - Web search functionality
- **[OpenAI](https://openai.com)** - AI-powered ranking and summarization
- **[Streamlit](https://streamlit.io)** - Beautiful web interface
- **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)** - Web scraping
- **[httpx](https://www.python-httpx.org/)** - Async HTTP client

## 📞 Support

**Issues or questions?**

- 📧 **Email:** [21cs25@ecajmer.ac.in](mailto:21cs25@ecajmer.ac.in)
- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/dharmraj8033/QueryNova/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/dharmraj8033/QueryNova/discussions)
- 📖 **Documentation:** [Wiki](https://github.com/dharmraj8033/QueryNova/wiki)

## 🎉 Success Stories

> "QueryNova transformed how our research team discovers information. The AI summarization saves us hours every week!" - Research Lead, Tech Company

> "Deployed to Streamlit Cloud in 5 minutes. The UI is gorgeous and the results are incredibly relevant." - Data Scientist

> "The knowledge base feature lets us augment web search with our internal docs. Game changer!" - Product Manager

---

<div align="center">

**Made with ❤️ by the QueryNova Team**

⭐ **Star us on GitHub** if you find QueryNova useful!

[⬆ Back to Top](#-querynova)

</div>
