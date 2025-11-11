# 🚀 QueryNova - Deployment Guide

## ✅ Changes Pushed to GitHub

**Repository:** https://github.com/dharmraj8033/QueryNova  
**Branch:** main  
**Commit:** Major Refactor v2.0  

---

## 📦 What Was Deployed

### New Files (33 files changed, 4899 insertions):
- ✅ `src/app_streamlit.py` - Main Streamlit application
- ✅ `src/services/*` - Modular service layer (search, export, knowledge base)
- ✅ `src/utils/secrets.py` - Unified secret management
- ✅ `STREAMLIT_CLOUD_DEPLOY.md` - Deployment instructions
- ✅ `DEPLOYMENT_CHECKLIST.md` - Production verification
- ✅ `QUICKSTART.md` - Quick setup guide
- ✅ `REFACTORING_SUMMARY.md` - Technical documentation

### Updated Files:
- ✅ Fixed OpenAI API calls in `ai_filter.py`, `summarizer.py`
- ✅ Enhanced error handling in `search_service.py`
- ✅ Updated `requirements.txt` (removed fpdf2, added aiohttp)
- ✅ Improved `.gitignore` (excludes cache, test files, secrets)

### Removed:
- ❌ PDF export functionality (focus on core features)
- ❌ Test files and temporary scripts
- ❌ Cached data (for fresh start)

---

## 🎯 Deploy to Streamlit Cloud

### Step 1: Go to Streamlit Cloud
1. Visit: https://share.streamlit.io
2. Sign in with GitHub
3. Click **"New app"**

### Step 2: Configure Deployment
```
Repository: dharmraj8033/QueryNova
Branch: main
Main file path: src/app_streamlit.py
```

### Step 3: Add Secrets
Click **"Advanced settings"** → **"Secrets"**

Paste this (with YOUR actual API keys):
```toml
SERPAPI_API_KEY = "your-serpapi-key-here"
OPENAI_API_KEY = "sk-your-openai-key-here"
```

**Get API Keys:**
- SerpAPI: https://serpapi.com/ (100 free searches/month)
- OpenAI: https://platform.openai.com/api-keys

### Step 4: Deploy
Click **"Deploy"** and wait 2-3 minutes.

Your app will be live at: `https://your-app-name.streamlit.app`

---

## 💻 Run Locally

### Quick Start:
```powershell
# 1. Clone repository
git clone https://github.com/dharmraj8033/QueryNova.git
cd QueryNova

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add API keys to .streamlit/secrets.toml
# Copy the template and add your keys:
# SERPAPI_API_KEY = "your-key"
# OPENAI_API_KEY = "sk-your-key"

# 4. Run the app
streamlit run src/app_streamlit.py
```

Open: http://localhost:8501

---

## 🔑 API Keys Setup

### Option 1: Streamlit Secrets (Recommended for Cloud)
Create `.streamlit/secrets.toml`:
```toml
SERPAPI_API_KEY = "your-serpapi-key-here"
OPENAI_API_KEY = "sk-your-openai-key-here"
```

### Option 2: Environment Variables (Local Development)
Create `.env` file in project root:
```bash
SERPAPI_API_KEY=your-serpapi-key-here
OPENAI_API_KEY=sk-your-openai-key-here
```

**The app automatically loads from either source!**

---

## ⚠️ Important Notes

### OpenAI API Credits
- Your current OpenAI key has **insufficient quota**
- Add credits at: https://platform.openai.com/settings/organization/billing/overview
- Without credits:
  - ✅ Search still works
  - ❌ AI summaries won't work (uses fallback)
  - ✅ App doesn't crash

### SerpAPI Limits
- Free tier: 100 searches/month
- After limit: Upgrade at https://serpapi.com/pricing

### Cache Behavior
- First search: Fetches fresh data
- Repeat searches: Uses cache (faster)
- Clear cache: Restart the app or press 'C' in browser

---

## 🧪 Verify Deployment

After deploying, test these features:

1. **Search**: Try "Python programming"
2. **AI Summary**: Check if summary appears (needs OpenAI credits)
3. **Export**: Download Markdown or JSON
4. **Knowledge Base**: Upload a TXT file
5. **Heatmap**: Verify visualization appears
6. **Suggestions**: Check related queries

---

## 📊 What's Working Now

✅ **Core Features:**
- Web search via SerpAPI
- Async page crawling
- Content ranking
- Sentiment analysis
- Search heatmaps
- Query suggestions
- Knowledge base
- Export (Markdown, JSON, Notion)

✅ **Production Ready:**
- Error handling
- Caching
- Logging
- API key validation
- Graceful fallbacks

---

## 🐛 Troubleshooting

### "Search provider failed"
- Check SerpAPI key in secrets
- Verify key at https://serpapi.com/manage-api-key

### "AI features not working"
- Check OpenAI key has credits
- Add payment method at OpenAI dashboard

### "Module not found"
- Run: `pip install -r requirements.txt`

### "Cache issues"
- Delete `data/query_cache.db`
- Restart the app

---

## 📚 Documentation

- **Full Deployment:** `STREAMLIT_CLOUD_DEPLOY.md`
- **Quick Start:** `QUICKSTART.md`
- **Verification:** `DEPLOYMENT_CHECKLIST.md`
- **Technical Details:** `REFACTORING_SUMMARY.md`

---

## 🎉 Success!

Your QueryNova app is now:
- ✅ **Pushed to GitHub**
- ✅ **Ready for Streamlit Cloud**
- ✅ **Fully documented**
- ✅ **Production-ready**

**Next Steps:**
1. Deploy to Streamlit Cloud (5 minutes)
2. Add API keys in Cloud secrets
3. Share your app URL! 🚀

**Repository:** https://github.com/dharmraj8033/QueryNova
