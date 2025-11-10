# 🔍 QueryNova

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT_Powered-green.svg)](https://openai.com)

**QueryNova** is an AI-powered search assistant that combines web search, intelligent crawling, and AI-driven content ranking to deliver superior search results with extracted summaries.

## ✨ Features

🔍 **Smart Web Search** - Uses SerpAPI for comprehensive web search results  
🕷️ **Intelligent Crawling** - Extracts and processes content from web pages  
🧠 **AI-Powered Ranking** - Uses OpenAI embeddings for semantic similarity ranking  
� **Dark Mode** - Beautiful gradient UI with modern design  
� **Search History** - Track and rerun your recent searches  
⚡ **Smart Caching** - Faster results with intelligent caching  
� **Export Options** - Download results in JSON or CSV format  
� **Analytics** - View search statistics and relevance metrics

## 🚀 Quick Start

### Deploy to Streamlit Cloud (Recommended)

1. **Fork this repository**

2. **Go to [share.streamlit.io](https://share.streamlit.io)**

3. **Deploy your app:**
   - Repository: `your-username/QueryNova`
   - Branch: `main`
   - Main file: `streamlit_app.py`

4. **Add your API keys in Secrets:**
   ```toml
   SERPAPI_API_KEY = "your_serpapi_key"
   OPENAI_API_KEY = "sk-your_openai_key"
   ```

5. **Done!** Your app will be live in minutes 🎉

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dharmraj8033/QueryNova.git
   cd QueryNova
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   SERPAPI_API_KEY=your_serpapi_key_here
   OPENAI_API_KEY=sk-your_openai_key_here
   ```

4. **Run the app:**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open your browser:** http://localhost:8501

## 🔑 API Keys Setup

### SerpAPI (Required)
1. Sign up at [serpapi.com](https://serpapi.com)
2. Get your API key from the dashboard
3. Add to `.env` or Streamlit secrets

### OpenAI API (Required for AI ranking)
1. Create account at [platform.openai.com](https://platform.openai.com)
2. Generate API key at [API Keys page](https://platform.openai.com/api-keys)
3. Add to `.env` or Streamlit secrets

## 📁 Project Structure
```
QueryNova/
├── streamlit_app.py      # Main Streamlit application
├── requirements.txt      # Python dependencies
├── .streamlit/
│   └── config.toml      # Streamlit configuration
├── src/
│   └── modules/
│       ├── search.py    # Web search functionality
│       ├── crawl.py     # Web crawling and extraction
│       └── ai_filter.py # AI-powered ranking
├── config/
│   └── config.py        # Configuration management
└── README.md
```

## 🎨 Features in Detail

### Dark Mode UI
- Beautiful gradient backgrounds
- Modern purple-blue color scheme
- Smooth animations and transitions

### Search History
- Tracks your last 10 searches
- One-click to rerun previous queries
- Displays timestamp and result counts

### Smart Caching
- Caches search results for faster access
- Toggle on/off as needed
- Automatic cache management

### Export Options
- **JSON**: Structured data with full details
- **CSV**: Spreadsheet-compatible format
- Timestamped filenames

### Analytics
- Total searches performed
- Total results found
- Average relevance scores
- High/Medium/Low quality categorization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [SerpAPI](https://serpapi.com) for web search functionality
- [OpenAI](https://openai.com) for AI-powered content ranking
- [Streamlit](https://streamlit.io) for the beautiful web interface
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping

## 📞 Support

If you encounter any issues or have questions:
- Create an [Issue](https://github.com/dharmraj8033/QueryNova/issues)
- Check the documentation files (DEPLOYMENT.md, SECRETS_SETUP.md, FEATURES.md)
- Contact: [21cs25@ecajmer.ac.in](mailto:21cs25@ecajmer.ac.in)

---

**Made with ❤️ by QueryNova Team**
