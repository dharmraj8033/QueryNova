# ✅ QueryNova Deployment Checklist

Use this checklist to ensure successful deployment of QueryNova v2.0 to Streamlit Cloud.

## Pre-Deployment

### 1. Repository Setup
- [ ] Fork repository to your GitHub account
- [ ] Ensure all code is committed and pushed
- [ ] Verify `.gitignore` excludes secrets
- [ ] Check that `.streamlit/secrets.toml` is git-ignored
- [ ] Review `requirements.txt` for all dependencies

### 2. API Keys Acquisition
- [ ] Sign up for SerpAPI account
- [ ] Obtain SerpAPI key from dashboard
- [ ] Verify SerpAPI free tier (100 searches/month)
- [ ] Sign up for OpenAI account
- [ ] Generate OpenAI API key
- [ ] Add billing information to OpenAI (if needed)
- [ ] Test both API keys locally (optional)

### 3. Local Testing (Optional but Recommended)
- [ ] Clone repository locally
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Create `.env` with API keys
- [ ] Run locally: `streamlit run src/app_streamlit.py`
- [ ] Test basic search functionality
- [ ] Verify all tabs work (Results, Summary, Suggestions, Logs, Export)
- [ ] Test dark/light mode toggle
- [ ] Upload test document to Knowledge Base
- [ ] Export results in multiple formats

## Streamlit Cloud Deployment

### 4. Account Setup
- [ ] Go to [share.streamlit.io](https://share.streamlit.io)
- [ ] Sign in with GitHub account
- [ ] Grant Streamlit access to repositories
- [ ] Verify email (if required)

### 5. App Creation
- [ ] Click "New app" button
- [ ] Select repository: `your-username/QueryNova`
- [ ] Choose branch: `main` (or your default branch)
- [ ] Set main file path: `src/app_streamlit.py`
- [ ] Choose custom app URL (optional)
- [ ] Click "Advanced settings"
- [ ] Verify Python version: 3.10 or higher
- [ ] Click "Deploy"

### 6. Secrets Configuration
- [ ] Wait for initial deployment
- [ ] Click "Settings" or "⚙️" icon
- [ ] Navigate to "Secrets" section
- [ ] Paste configuration:
```toml
SERPAPI_API_KEY = "your-actual-serpapi-key"
OPENAI_API_KEY = "sk-your-actual-openai-key"
```
- [ ] Click "Save"
- [ ] Wait for app to reboot (~30 seconds)

## Post-Deployment Verification

### 7. API Status Check
- [ ] Open deployed app URL
- [ ] Check sidebar under "🔑 API Status"
- [ ] Verify "✅ SerpAPI Connected"
- [ ] Verify "✅ OpenAI Connected"
- [ ] If ❌ appears, review secrets configuration

### 8. Basic Functionality Tests
- [ ] Enter test query: "latest technology news"
- [ ] Click "🚀 Search" button
- [ ] Wait for results (10-30 seconds expected)
- [ ] Verify results appear in Results tab
- [ ] Check AI Summary tab for generated summary
- [ ] Review Suggestions tab for related queries
- [ ] Inspect Logs tab for search process
- [ ] Test Export tab downloads

### 9. UI/UX Tests
- [ ] Toggle Dark/Light mode
- [ ] Verify theme changes apply
- [ ] Test on mobile/tablet (responsive design)
- [ ] Try different screen sizes
- [ ] Check all buttons and interactions
- [ ] Verify animations and transitions work
- [ ] Test metric cards display correctly

### 10. Advanced Features
- [ ] Upload a test document (TXT/PDF)
- [ ] Verify Knowledge Base shows document
- [ ] Run search that references uploaded content
- [ ] Check knowledge snippets in results
- [ ] Import content from URL
- [ ] Test voice input (Chrome/Edge only)
- [ ] Verify search history populates
- [ ] Click history item to re-run search
- [ ] Test caching (repeat same query)
- [ ] Try offline mode with cached data

### 11. Export Functionality
- [ ] Export results as Markdown
- [ ] Download and verify Markdown format
- [ ] Export as JSON
- [ ] Verify JSON structure
- [ ] Try PDF export (may have warnings)
- [ ] Check Notion export payload
- [ ] Verify all downloads work

## Performance & Monitoring

### 12. Performance Checks
- [ ] Measure search time (should be 10-30 seconds)
- [ ] Test with different result counts (5, 10, 20)
- [ ] Verify app doesn't crash with 30 results
- [ ] Check memory usage in Streamlit dashboard
- [ ] Test concurrent searches (if expecting users)

### 13. Error Handling
- [ ] Test with invalid/empty query
- [ ] Try search when APIs are rate-limited
- [ ] Verify graceful error messages appear
- [ ] Check logs in Streamlit dashboard
- [ ] Test with special characters in query
- [ ] Try uploading unsupported file types

### 14. API Quota Monitoring
- [ ] Check SerpAPI dashboard for usage
- [ ] Monitor OpenAI usage dashboard
- [ ] Set up billing alerts (OpenAI)
- [ ] Plan for quota upgrades if needed
- [ ] Document typical costs per search

## Documentation & Sharing

### 15. Documentation Review
- [ ] Read [README.md](README.md) thoroughly
- [ ] Review [STREAMLIT_CLOUD_DEPLOY.md](STREAMLIT_CLOUD_DEPLOY.md)
- [ ] Check [QUICKSTART.md](QUICKSTART.md)
- [ ] Update any custom documentation
- [ ] Add deployment URL to README (optional)

### 16. Sharing & Promotion
- [ ] Share deployment URL with team
- [ ] Add URL to GitHub repository description
- [ ] Create demo video/screenshots (optional)
- [ ] Write blog post about deployment (optional)
- [ ] Share on social media (optional)
- [ ] Add to personal portfolio

## Maintenance & Updates

### 17. Ongoing Monitoring
- [ ] Check app daily for first week
- [ ] Monitor API usage weekly
- [ ] Review Streamlit logs for errors
- [ ] Set up uptime monitoring (optional)
- [ ] Plan for regular dependency updates

### 18. Update Process
- [ ] Document update procedure
- [ ] Test updates locally before pushing
- [ ] Push to GitHub main branch
- [ ] Verify auto-deployment works
- [ ] Manual reboot if needed

### 19. Backup & Recovery
- [ ] Document secrets configuration separately
- [ ] Keep API keys in secure password manager
- [ ] Export sample results for testing
- [ ] Document custom configurations
- [ ] Plan for disaster recovery

## Troubleshooting

### Common Issues Checklist

#### "❌ API Not Configured"
- [ ] Verify secrets.toml syntax (TOML format)
- [ ] Check for extra spaces in API keys
- [ ] Ensure keys don't have quotes inside quotes
- [ ] Reboot app after secrets change
- [ ] Check Streamlit logs for errors

#### "Search Failed"
- [ ] Verify API keys are active
- [ ] Check SerpAPI dashboard for quota
- [ ] Check OpenAI billing status
- [ ] Test APIs with curl/postman
- [ ] Review rate limits
- [ ] Reduce max results temporarily

#### "PDF Export Issues"
- [ ] This is expected for some content
- [ ] Use Markdown export instead
- [ ] Check export warnings
- [ ] Review FPDF errors in logs
- [ ] Consider disabling PDF by default

#### "Slow Performance"
- [ ] Reduce max results (5-10)
- [ ] Check Streamlit Cloud region
- [ ] Monitor concurrent users
- [ ] Review crawling timeout settings
- [ ] Consider caching strategies

## Success Criteria

Your deployment is successful when:

- ✅ App loads without errors
- ✅ Both API status indicators show ✅
- ✅ Basic search returns 10+ results in <30 seconds
- ✅ AI Summary generates correctly
- ✅ All tabs are accessible
- ✅ Exports download successfully
- ✅ Dark/Light mode toggles work
- ✅ Knowledge Base accepts uploads
- ✅ Search history persists
- ✅ No critical errors in logs

## Final Steps

- [ ] Bookmark your deployment URL
- [ ] Add URL to GitHub About section
- [ ] Star the original repository
- [ ] Consider contributing improvements
- [ ] Share feedback with developers
- [ ] Help others in discussions

---

## Quick Commands Reference

### Local Development
```bash
# Run app
streamlit run src/app_streamlit.py

# Different port
streamlit run src/app_streamlit.py --server.port 8502

# Debug mode
streamlit run src/app_streamlit.py --logger.level=debug
```

### Streamlit Cloud
```bash
# Force reboot via CLI (if installed)
streamlit cloud reboot your-app-name

# View logs
streamlit cloud logs your-app-name
```

### Testing APIs
```bash
# Test SerpAPI
curl "https://serpapi.com/search?q=test&api_key=YOUR_KEY"

# Test OpenAI
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_KEY"
```

---

## Support Resources

- **Documentation:** [STREAMLIT_CLOUD_DEPLOY.md](STREAMLIT_CLOUD_DEPLOY.md)
- **Issues:** [GitHub Issues](https://github.com/dharmraj8033/QueryNova/issues)
- **Email:** 21cs25@ecajmer.ac.in
- **Streamlit Forum:** [discuss.streamlit.io](https://discuss.streamlit.io)

---

**🎉 Congratulations on deploying QueryNova!**

*This checklist ensures a smooth, production-ready deployment.*

*Last Updated: November 11, 2025*
