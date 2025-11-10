# 🚀 Streamlit Cloud Deployment Guide for QueryNova

This guide will help you deploy QueryNova to Streamlit Community Cloud.

## ✅ Prerequisites Checklist

Before deploying, make sure you have:

- [ ] A GitHub account
- [ ] The QueryNova repository pushed to your GitHub account
- [ ] A Streamlit Community Cloud account (sign up at [share.streamlit.io](https://share.streamlit.io))
- [ ] Valid API keys:
  - [ ] SerpAPI key (get from [serpapi.com](https://serpapi.com))
  - [ ] OpenAI API key (get from [platform.openai.com](https://platform.openai.com))

## 📝 Step-by-Step Deployment

### Step 1: Verify GitHub Repository

1. Make sure all changes are committed and pushed:
   ```powershell
   $env:Path += ";C:\Program Files\Git\cmd"
   git status
   git add .
   git commit -m "Prepare for Streamlit Cloud deployment"
   git push origin main
   ```

2. Verify your repository is accessible:
   - Go to https://github.com/dharmraj8033/QueryNova
   - Make sure the repository is **public** (required for free Streamlit Community Cloud)
   - If private, go to Settings → Danger Zone → Change visibility → Make public

### Step 2: Connect to Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)

2. Sign in with your GitHub account

3. Click **"New app"** button

4. Fill in the deployment form:
   - **Repository:** `dharmraj8033/QueryNova`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py` ← **IMPORTANT: Use this file!**
   - **App URL:** Choose a custom URL (e.g., `querynova-search`)

### Step 3: Configure Secrets (API Keys)

Before deploying, you MUST configure your API keys:

1. In the deployment form, click **"Advanced settings"**

2. In the **"Secrets"** section, paste the following (replace with your actual keys):

   ```toml
   SERPAPI_API_KEY = "your_actual_serpapi_key_here"
   OPENAI_API_KEY = "sk-your_actual_openai_key_here"
   ```

3. Click **"Save"**

### Step 4: Deploy!

1. Click **"Deploy!"** button

2. Wait for the deployment to complete (usually 2-5 minutes)

3. Watch the logs for any errors

4. Once deployed, your app will be live at: `https://[your-app-name].streamlit.app`

## 🔧 Troubleshooting

### Issue: "The app's code is not connected to a remote GitHub repository"

**Solutions:**

1. **Verify Git is properly configured:**
   ```powershell
   $env:Path += ";C:\Program Files\Git\cmd"
   git remote -v
   ```
   Should show: `origin  https://github.com/dharmraj8033/QueryNova.git`

2. **Make sure all changes are pushed:**
   ```powershell
   git push origin main
   ```

3. **Check repository visibility:**
   - Repository must be **public** for Streamlit Community Cloud free tier
   - Go to GitHub → Settings → Change repository visibility to Public

4. **Try deploying from Streamlit Cloud instead:**
   - Instead of using the "Deploy" button in the local Streamlit app
   - Go directly to [share.streamlit.io](https://share.streamlit.io)
   - Use the "New app" button there

### Issue: "Module not found" errors

**Solution:** Make sure `requirements.txt` is in the root directory and contains all dependencies:
```
requests
httpx
beautifulsoup4
openai
serpapi
flask
streamlit
python-dotenv
pytest
pytest-asyncio
```

### Issue: "API key not configured" errors

**Solution:** 
1. Go to your Streamlit Cloud dashboard
2. Click on your app → Settings (⚙️ icon)
3. Go to "Secrets" section
4. Add your API keys in TOML format:
   ```toml
   SERPAPI_API_KEY = "your_key"
   OPENAI_API_KEY = "sk-your_key"
   ```
5. Click "Save" and the app will restart automatically

### Issue: Import errors with modules

**Solution:** The new `streamlit_app.py` file in the root directory handles import paths correctly. Make sure you're using this file as the main file path in deployment settings.

## 🎯 Post-Deployment Checklist

After successful deployment:

- [ ] Test the search functionality
- [ ] Verify API keys are working (check sidebar status indicators)
- [ ] Test with different queries
- [ ] Check error handling works correctly
- [ ] Share your app URL with others!

## 📊 Monitoring Your App

### View Logs
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click on your app
3. Click "Manage app" → "Logs" to see real-time logs

### Update Your App
Whenever you push changes to GitHub:
```powershell
git add .
git commit -m "Your changes"
git push origin main
```
Streamlit Cloud will automatically redeploy your app!

### Manage Settings
- Go to app dashboard → Settings (⚙️)
- Update secrets, change branch, or configure other settings
- Changes take effect immediately after restart

## 🆘 Still Having Issues?

1. **Check the file structure:**
   ```
   QueryNova/
   ├── streamlit_app.py        ← Main entry point (NEW FILE)
   ├── requirements.txt        ← Dependencies
   ├── .streamlit/
   │   ├── config.toml        ← Streamlit config
   │   └── secrets.toml.example
   ├── src/
   │   ├── modules/
   │   └── ...
   └── ...
   ```

2. **Verify you're using the correct main file:**
   - Main file path should be: `streamlit_app.py` (in root)
   - NOT `src/app_streamlit.py`

3. **Check GitHub repository:**
   - Repository must be public
   - All files must be pushed
   - Verify at: https://github.com/dharmraj8033/QueryNova

4. **Try the manual deployment method:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Manually enter repository details
   - Don't use the "Deploy" button in local Streamlit app

## 🎉 Success!

Once deployed, your QueryNova app will be accessible at:
```
https://[your-app-name].streamlit.app
```

Share it with the world! 🌍

---

**Need more help?**
- Streamlit Docs: https://docs.streamlit.io/streamlit-community-cloud
- QueryNova Issues: https://github.com/dharmraj8033/QueryNova/issues
