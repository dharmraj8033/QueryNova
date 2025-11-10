# 🔐 How to Add API Keys to Streamlit Cloud

## The Problem
You're getting `401 Unauthorized` error because Streamlit Cloud is using placeholder keys instead of your real API keys.

## The Solution - Configure Secrets in Streamlit Cloud

### Step 1: Go to Your App Settings
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Find your QueryNova app in the dashboard
3. Click the **⚙️ (Settings)** icon or three dots menu
4. Select **"Settings"**

### Step 2: Add Your Secrets
1. In the left sidebar, click on **"Secrets"**
2. You'll see a text editor
3. **Paste the following** (replace with your ACTUAL API keys):

```toml
SERPAPI_API_KEY = "paste_your_real_serpapi_key_here"
OPENAI_API_KEY = "sk-paste_your_real_openai_key_here"
```

**IMPORTANT:** 
- Remove the placeholder text `your_serpapi_key_here`
- Use your REAL API keys from:
  - SerpAPI: https://serpapi.com/manage-api-key
  - OpenAI: https://platform.openai.com/api-keys

### Step 3: Save and Restart
1. Click **"Save"** button
2. Your app will automatically restart
3. Wait for the reboot to complete (30-60 seconds)

### Step 4: Test Your App
1. Go to your app URL: `https://your-app-name.streamlit.app`
2. Check the sidebar - it should show:
   - ✅ SerpAPI configured
   - ✅ OpenAI configured
3. Try a search query
4. If it works, you're done! 🎉

## Example of Correct Secrets Format

```toml
# This is what it should look like (with your real keys):
SERPAPI_API_KEY = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
OPENAI_API_KEY = "sk-proj-AbCdEfGhIjKlMnOpQrStUvWxYz1234567890"
```

## Common Mistakes to Avoid

❌ **Don't do this:**
```toml
SERPAPI_API_KEY = your_serpapi_key_here  # Missing quotes
OPENAI_API_KEY = "sk-your_openai_key_here"  # Placeholder key
```

✅ **Do this:**
```toml
SERPAPI_API_KEY = "your_actual_key_from_serpapi_dashboard"
OPENAI_API_KEY = "sk-your_actual_key_from_openai_dashboard"
```

## Troubleshooting

### Still getting 401 error?
1. **Check if secrets were saved:**
   - Go back to Settings → Secrets
   - Verify your keys are there
   - Make sure there are no extra spaces or quotes

2. **Restart the app manually:**
   - Click the three dots menu (⋮)
   - Select "Reboot app"
   - Wait for restart to complete

3. **Check your API keys are valid:**
   - Test SerpAPI: https://serpapi.com/manage-api-key
   - Test OpenAI: https://platform.openai.com/usage
   - Make sure keys have credits/quota available

4. **View app logs:**
   - In Streamlit Cloud dashboard
   - Click "Manage app" → "Logs"
   - Look for error messages

### Getting import errors instead?
Make sure you've pushed the latest code changes:
```powershell
$env:Path += ";C:\Program Files\Git\cmd"
git add .
git commit -m "Fix API key loading for Streamlit Cloud"
git push origin main
```

## Video Guide
For visual instructions, watch: [Streamlit Secrets Tutorial](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)

---

**Need your API keys?**
- 🔑 SerpAPI: https://serpapi.com/manage-api-key
- 🔑 OpenAI: https://platform.openai.com/api-keys
