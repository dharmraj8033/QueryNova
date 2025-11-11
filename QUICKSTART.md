# 🚀 QueryNova - Quick Start Guide

## ⚡ FASTEST WAY TO RUN (No Setup Required)

```powershell
# 1. Navigate to project
cd v:\Code\QueryNova

# 2. Run the safe launcher (validates everything automatically)
python run.py
```

That's it! The app will:
- ✅ Check all dependencies
- ✅ Validate API keys  
- ✅ Test connections
- ✅ Launch the app at http://localhost:8501

---

# 🚀 QueryNova - Quick Start Guide (LEGACY)

Get QueryNova running in under 5 minutes!

## ⚡ Fastest Method: Streamlit Cloud

### Prerequisites
- GitHub account
- SerpAPI key ([get free](https://serpapi.com/users/sign_up))
- OpenAI API key ([get here](https://platform.openai.com/api-keys))

### Steps

1. **Fork Repository**
   ```
   Go to: https://github.com/dharmraj8033/QueryNova
   Click: Fork button
   ```

2. **Deploy on Streamlit**
   ```
   Go to: https://share.streamlit.io
   Click: "New app"
   Select your fork: your-username/QueryNova
   Branch: main
   Main file: src/app_streamlit.py
   Click: Deploy!
   ```

3. **Add Secrets**
   ```
   In Streamlit dashboard:
   Settings → Secrets → Add:
   
   SERPAPI_API_KEY = "your-actual-key"
   OPENAI_API_KEY = "sk-your-actual-key"
   ```

4. **Done! 🎉**
   Your app is live at: `https://your-app.streamlit.app`

## 💻 Local Development

### Using Python (5 minutes)

```bash
# 1. Clone
git clone https://github.com/dharmraj8033/QueryNova.git
cd QueryNova

# 2. Install
pip install -r requirements.txt

# 3. Configure
echo "SERPAPI_API_KEY=your-key" > .env
echo "OPENAI_API_KEY=sk-your-key" >> .env

# 4. Run
streamlit run src/app_streamlit.py
```

### Using Docker (3 minutes)

```bash
# 1. Pull & Run
docker run -p 8501:8501 \
  -e SERPAPI_API_KEY=your-key \
  -e OPENAI_API_KEY=sk-your-key \
  querynova/app:latest

# Or build locally:
docker build -t querynova .
docker run -p 8501:8501 --env-file .env querynova
```

## 🔑 Getting API Keys

### SerpAPI (30 seconds)
1. Visit [serpapi.com/users/sign_up](https://serpapi.com/users/sign_up)
2. Sign up with email
3. Verify email
4. Copy key from dashboard
5. **Free: 100 searches/month**

### OpenAI (1 minute)
1. Visit [platform.openai.com/signup](https://platform.openai.com/signup)
2. Sign up/login
3. Go to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy immediately (can't view again!)
6. **Add billing or use free trial**

## ✅ Verify Setup

1. **Check API Status**
   - Open app
   - Check sidebar: should show ✅ for both APIs

2. **Run Test Search**
   ```
   Query: "latest AI news"
   Click: 🚀 Search
   Expected: 10-12 results in ~15 seconds
   ```

3. **Test Features**
   - Switch to Dark mode
   - Try exporting results
   - Upload a test document
   - View AI summary

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| API not configured | Check secrets/env file for typos |
| Search fails | Verify API keys are active and have quota |
| Slow performance | Reduce "Max Results" to 5-10 |
| PDF export fails | Normal - use Markdown instead |
| Port 8501 in use | Use different port: `streamlit run src/app_streamlit.py --server.port 8502` |

## 🎯 First Search Examples

Try these queries to explore features:

1. **Basic Search**
   ```
   "quantum computing breakthroughs 2024"
   ```

2. **With Knowledge Base**
   ```
   Upload a PDF about your company
   Query: "product features comparison"
   ```

3. **Research Mode**
   ```
   Enable: AI Summary + Sentiment + Heatmap
   Query: "impact of AI on healthcare"
   Max Results: 20
   ```

## 📚 Next Steps

- Read [STREAMLIT_CLOUD_DEPLOY.md](STREAMLIT_CLOUD_DEPLOY.md) for detailed deployment
- Check [FEATURES.md](FEATURES.md) for all capabilities
- Join our [Discussions](https://github.com/dharmraj8033/QueryNova/discussions)

## 🎉 You're Ready!

Start searching and let QueryNova's AI enhance your research workflow!

---

**Need help?** Open an [issue](https://github.com/dharmraj8033/QueryNova/issues) or email 21cs25@ecajmer.ac.in
