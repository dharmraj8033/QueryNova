# 📝 QueryNova Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2025-11-10

### 🎉 Major Release - Enhanced Edition

#### ✨ Added
- **Dark Mode Support**: Beautiful dark theme with purple-blue gradients
- **Tabbed Interface**: Organized UI with Search, Advanced, and Export tabs
- **Search History**: Track and re-run your last 10 searches
- **Smart Caching**: Cache search results for faster retrieval
- **Export Features**: Download results in JSON, CSV, or TXT formats
- **Advanced Filters**: 
  - Search type selection (General, News, Academic, Videos)
  - Date range filters
  - Language selection
  - Sort options (Relevance, Date, Score)
- **Display Options**:
  - Toggle snippets visibility
  - Show/hide relevance scores
  - Compact view mode
- **Analytics Dashboard**: 
  - Total searches counter
  - Results statistics
  - Average relevance scores
  - High/Medium/Low relevance categorization
- **Interactive Actions**: Visit, Copy URL, Bookmark, and Similar buttons
- **API Status Indicators**: Real-time API configuration status
- **Performance Metrics**: Search timing and result counts
- **Custom CSS Styling**: Gradient backgrounds, animations, hover effects

#### 🎨 Improved
- Enhanced UI with modern gradient backgrounds
- Color-coded relevance scores (🟢 High, 🟡 Medium, 🔴 Low)
- Better responsive layout with improved spacing
- Animated buttons with smooth transitions
- Enhanced result cards with action buttons
- Improved error handling and user feedback
- Better mobile responsiveness

#### 🔧 Changed
- Updated color scheme to purple-blue gradient
- Reorganized interface with tabbed navigation
- Enhanced sidebar with more information
- Improved search result display

#### 🐛 Fixed
- API key loading issues for Streamlit Cloud deployment
- Import path handling for modules
- Secret management for cloud deployment

#### 📚 Documentation
- Added `FEATURES.md` - Complete feature documentation
- Added `DEPLOYMENT.md` - Deployment guide
- Added `SECRETS_SETUP.md` - API key configuration guide
- Added `CHANGELOG.md` - Version history

---

## [1.0.0] - 2025-11-09

### 🚀 Initial Release

#### Features
- Web search using SerpAPI
- Web page crawling and content extraction
- AI-powered result ranking using OpenAI embeddings
- Multiple interfaces: CLI, Flask API, Streamlit web app
- Docker support
- Basic error handling
- JSON and CSV output formats

#### Components
- Command-line interface (`main.py`)
- Flask REST API (`app_flask.py`)
- Streamlit web interface (`app_streamlit.py`)
- Search module (`modules/search.py`)
- Crawling module (`modules/crawl.py`)
- AI ranking module (`modules/ai_filter.py`)

---

## Future Roadmap

### [2.1.0] - Planned
- [ ] Bookmark management system
- [ ] Similar results finder
- [ ] Search result filtering
- [ ] Custom search engines
- [ ] More export formats (PDF, Markdown)

### [2.2.0] - Planned
- [ ] Multi-language UI support
- [ ] Advanced analytics dashboard
- [ ] Search result comparison
- [ ] Collaborative features
- [ ] API rate limiting

### [3.0.0] - Future
- [ ] Mobile application
- [ ] Browser extension
- [ ] Offline mode
- [ ] Custom AI models
- [ ] Team collaboration features

---

## Contributing

Found a bug or have a feature request? Please open an issue on [GitHub](https://github.com/dharmraj8033/QueryNova/issues).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note**: Dates follow the format YYYY-MM-DD. Version numbers follow [Semantic Versioning](https://semver.org/).
