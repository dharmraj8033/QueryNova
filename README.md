# 🔍 QueryNova

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT_Powered-green.svg)](https://openai.com)

**QueryNova** is an AI-powered search assistant that combines web search, intelligent crawling, and AI-driven content ranking to deliver superior search results with extracted summaries.

## ✨ Features

🔍 **Smart Web Search** - Uses SerpAPI for comprehensive web search results  
🕷️ **Intelligent Crawling** - Extracts and processes content from web pages  
🧠 **AI-Powered Ranking** - Uses OpenAI embeddings for semantic similarity ranking  
🌐 **Multiple Interfaces** - CLI, Flask API, and Streamlit web app  
🐳 **Docker Ready** - One-command deployment with Docker  
⚡ **Async Processing** - High-performance async web crawling  
📊 **Multiple Formats** - Output in JSON, CSV, or web interface  
🛡️ **Error Handling** - Graceful fallbacks and comprehensive error handling

## 🚀 Quick Start with Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dharmraj8033/QueryNova.git
   cd QueryNova
   ```

2. **Set up your API keys:**
   ```bash
   cp config/.env.example config/.env
   # Edit config/.env and add your API keys:
   # SERPAPI_API_KEY=your_serpapi_key
   # OPENAI_API_KEY=sk-your_openai_key
   ```

3. **Run with Docker:**
   ```bash
   # Build the image
   docker build -t querynova .
   
   # Start Streamlit web app
   docker run --env-file config/.env -p 8501:8501 querynova streamlit run src/app_streamlit.py --server.address=0.0.0.0
   ```

4. **Open your browser:** http://localhost:8501

## 🛠️ Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dharmraj8033/QueryNova.git
   cd QueryNova
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp config/.env.example config/.env
   # Edit config/.env with your API keys
   ```

## 🎯 Usage Examples

### 🖥️ Command Line Interface
```bash
cd src

# Basic search
python main.py --query "machine learning tutorials"

# JSON output
python main.py --query "Python best practices" --json

# CSV output  
python main.py --query "Docker vs Kubernetes" --csv
```

### 🌐 Streamlit Web App (Recommended)
```bash
cd src
streamlit run app_streamlit.py
```
Then visit: http://localhost:8501

### 🔌 Flask API
```bash
cd src
python app_flask.py
```
API endpoint: http://localhost:5000/search

**Example API usage:**
```bash
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "artificial intelligence trends"}'
```

## 🐳 Docker Deployment

### Quick Start
```bash
# Build and run Streamlit app
docker build -t querynova .
docker run --env-file config/.env -p 8501:8501 querynova streamlit run src/app_streamlit.py --server.address=0.0.0.0
```

### Other Docker Options
```bash
# Flask API
docker run --env-file config/.env -p 5000:5000 querynova python src/app_flask.py

# CLI
docker run --env-file config/.env querynova python src/main.py --query "your search" --json
```

## 🔑 API Keys Setup

### SerpAPI (Required)
1. Sign up at [serpapi.com](https://serpapi.com)
2. Get your API key from the dashboard
3. Add to `config/.env`: `SERPAPI_API_KEY=your_key_here`

### OpenAI API (Required for AI ranking)
1. Create account at [platform.openai.com](https://platform.openai.com)
2. Generate API key at [API Keys page](https://platform.openai.com/api-keys)
3. Add to `config/.env`: `OPENAI_API_KEY=sk-your_key_here`

## 🧪 Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_search.py

# Run with coverage
pytest --cov=src tests/
```

## 📁 Project Structure
```
QueryNova/
├── src/
│   ├── modules/
│   │   ├── search.py      # Web search functionality
│   │   ├── crawl.py       # Web crawling and extraction
│   │   └── ai_filter.py   # AI-powered ranking
│   ├── app_streamlit.py   # Streamlit web interface
│   ├── app_flask.py       # Flask API
│   └── main.py           # CLI application
├── config/
│   ├── config.py         # Configuration management
│   └── .env.example      # Environment variables template
├── tests/                # Test files
├── Dockerfile           # Docker configuration
└── requirements.txt     # Python dependencies
```

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
- Check the [Documentation](README.md)
- Contact: [21cs25@ecajmer.ac.in](mailto:21cs25@ecajmer.ac.in)
