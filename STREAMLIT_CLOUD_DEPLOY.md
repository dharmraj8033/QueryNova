# 🚀 Streamlit Cloud Deployment Guide

This guide will walk you through deploying QueryNova to Streamlit Cloud for free, no-code deployment directly from GitHub.

## 📋 Prerequisites

Before you begin, make sure you have:

1. **GitHub Account** - [Sign up here](https://github.com/join)
2. **Streamlit Cloud Account** - [Sign up here](https://share.streamlit.io/signup)
3. **API Keys**:
   - **SerpAPI Key** - [Get it here](https://serpapi.com/users/sign_up)
   - **OpenAI API Key** - [Get it here](https://platform.openai.com/signup)

## 🎯 Step-by-Step Deployment

### Step 1: Fork the Repository

1. Go to the QueryNova repository
2. Click the "Fork" button in the top right
3. Wait for GitHub to create your fork

### Step 2: Sign in to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in with GitHub"
3. Authorize Streamlit to access your GitHub account

### Step 3: Create New App

1. Click "New app" button
2. Fill in the deployment form:
   - **Repository:** `your-username/QueryNova`
   - **Branch:** `main`
   - **Main file path:** `src/app_streamlit.py`
   - **App URL:** Choose a custom URL (e.g., `querynova-yourname`)

3. Click "Advanced settings" (Optional)
   - **Python version:** 3.10 or higher
   - **Secrets:** We'll configure this in the next step

### Step 4: Configure Secrets

This is the most important step - configuring your API keys securely.

1. After creating the app (or from the app dashboard), click "⚙️ Settings"
2. Navigate to the "Secrets" section
3. Paste the following configuration, replacing with your actual API keys:

```toml
# Streamlit Cloud Secrets Configuration

# SerpAPI Key - Get yours at https://serpapi.com/
SERPAPI_API_KEY = "your-actual-serpapi-key-here"

# OpenAI API Key - Get yours at https://platform.openai.com/api-keys
OPENAI_API_KEY = "sk-your-actual-openai-key-here"
```

4. Click "Save"

### Step 5: Deploy!

1. Click "Deploy!" button
2. Wait for the deployment to complete (usually 2-5 minutes)
3. Your app will be live at: `https://your-app-name.streamlit.app`

## 🔑 Getting API Keys

### SerpAPI Key

1. Go to [serpapi.com](https://serpapi.com/users/sign_up)
2. Sign up for a free account
3. Verify your email
4. Navigate to [Dashboard](https://serpapi.com/manage-api-key)
5. Copy your API key
6. **Free tier includes:** 100 searches/month

### OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com/signup)
2. Sign up or sign in
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Name it (e.g., "QueryNova")
6. Copy the key immediately (you won't see it again!)
7. **Important:** Add credit to your account or use free trial credits

## ✅ Verification

After deployment, verify everything works:

### 1. Check API Status
- Open your deployed app
- Look at the sidebar under "🔑 API Status"
- You should see:
  - ✅ SerpAPI Connected
  - ✅ OpenAI Connected

### 2. Test Search
- Enter a simple query: "latest technology news"
- Click "🚀 Search"
- You should see results within 10-30 seconds

### 3. Check Features
- Try different tabs: Results, AI Summary, Suggestions, Logs, Export
- Toggle dark/light mode
- Upload a test document to Knowledge Base
- Export results in different formats

## 🔧 Troubleshooting

### Problem: "❌ SerpAPI Not Configured"

**Solutions:**
1. Verify your API key is correct in Streamlit Secrets
2. Make sure there are no extra spaces or quotes
3. Check your SerpAPI dashboard for quota limits
4. Try regenerating the API key

### Problem: "❌ OpenAI Not Configured"

**Solutions:**
1. Verify your API key starts with `sk-`
2. Check if you have billing enabled on OpenAI
3. Ensure you haven't exceeded rate limits
4. Try creating a new API key

### Problem: "Search failed" or Timeout Errors

**Solutions:**
1. **Check API Credits:**
   - SerpAPI: Visit [Dashboard](https://serpapi.com/dashboard)
   - OpenAI: Visit [Usage](https://platform.openai.com/usage)

2. **Verify Internet Access:**
   - Streamlit Cloud should have internet access by default

3. **Check Logs:**
   - In Streamlit Cloud dashboard, click "☰ Manage app"
   - View logs for detailed error messages

### Problem: App Crashes or Restarts

**Solutions:**
1. **Check Memory Usage:**
   - Large result sets can use significant memory
   - Reduce "Max Results" in Advanced Options

2. **Review Logs:**
   - Look for Python exceptions in the Streamlit Cloud logs

3. **Clear Cache:**
   - In your app, the cache is automatically managed
   - Can manually clear by restarting the app

### Problem: PDF Export Not Working

**Solutions:**
1. This is expected for complex content
2. Use Markdown or JSON export instead
3. PDF generation has limitations with special characters
4. Check export warnings in the Export tab

## 🎨 Customization

### Change Theme Colors

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#YOUR_COLOR"      # Accent color
backgroundColor = "#YOUR_COLOR"    # Main background
secondaryBackgroundColor = "#YOUR_COLOR"  # Sidebar/cards
textColor = "#YOUR_COLOR"         # Text color
```

### Adjust App Settings

Edit the file at the top of `src/app_streamlit.py`:

```python
st.set_page_config(
    page_title="Your Custom Title",
    page_icon="🔍",  # Change emoji
    layout="wide",
)
```

## 📊 Monitoring Usage

### SerpAPI Usage
- Dashboard: [serpapi.com/dashboard](https://serpapi.com/dashboard)
- **Free Tier:** 100 searches/month
- **Paid Plans:** From $50/month for 5,000 searches

### OpenAI Usage
- Dashboard: [platform.openai.com/usage](https://platform.openai.com/usage)
- **Pricing:** Pay-as-you-go
- **Typical Cost:** ~$0.01-0.05 per search (with embeddings + summarization)

## 🔄 Updating Your App

### Method 1: Git Push (Automatic)

1. Make changes to your code locally
2. Commit and push to GitHub:
```bash
git add .
git commit -m "Your update message"
git push origin main
```
3. Streamlit Cloud auto-detects changes and redeploys (1-2 minutes)

### Method 2: Manual Reboot

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Find your app
3. Click "⚙️ Settings" → "Reboot app"

## 🌐 Custom Domain (Optional)

Streamlit Cloud provides a default URL, but you can use a custom domain:

1. In Streamlit Cloud settings, go to "General"
2. Under "Custom subdomain", enter your preferred name
3. For full custom domain (e.g., `querynova.com`):
   - This requires a paid Streamlit Cloud plan
   - Follow [Streamlit's custom domain guide](https://docs.streamlit.io/streamlit-community-cloud/manage-your-app#custom-subdomains)

## 🔐 Security Best Practices

1. **Never Commit API Keys:**
   - Always use Streamlit Secrets
   - Add `.env` to `.gitignore`

2. **Rotate Keys Regularly:**
   - Change API keys every 3-6 months
   - Immediately rotate if leaked

3. **Monitor Usage:**
   - Set up billing alerts on OpenAI
   - Check SerpAPI usage weekly

4. **Rate Limiting:**
   - QueryNova has built-in retry logic
   - Consider implementing user quotas for public deployments

## 📚 Additional Resources

- **Streamlit Documentation:** [docs.streamlit.io](https://docs.streamlit.io)
- **Streamlit Cloud Docs:** [docs.streamlit.io/streamlit-community-cloud](https://docs.streamlit.io/streamlit-community-cloud)
- **SerpAPI Docs:** [serpapi.com/docs](https://serpapi.com/docs)
- **OpenAI API Docs:** [platform.openai.com/docs](https://platform.openai.com/docs)

## 🆘 Getting Help

If you encounter issues:

1. **Check Logs:**
   - Streamlit Cloud dashboard → Manage app → View logs

2. **GitHub Issues:**
   - [Create an issue](https://github.com/dharmraj8033/QueryNova/issues)

3. **Streamlit Community:**
   - [Streamlit Forum](https://discuss.streamlit.io)

4. **Contact:**
   - Email: 21cs25@ecajmer.ac.in

## 🎉 Success!

Your QueryNova instance should now be:
- ✅ Deployed on Streamlit Cloud
- ✅ Accessible via a public URL
- ✅ Connected to SerpAPI and OpenAI
- ✅ Ready for AI-powered searches

**Share your deployment URL and start exploring!** 🚀

---

*Last updated: November 2025*
*QueryNova v2.0 - Streamlit Cloud Edition*
