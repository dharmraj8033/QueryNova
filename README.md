# QueryNova

QueryNova is a Python-based AI-powered search assistant that:

1. Takes a user query via CLI, web app (Flask), or Streamlit interface.
2. Uses a search API (SerpAPI) to fetch top web results.
3. Crawls and extracts additional data from each result.
4. Uses OpenAI GPT-4 to analyze and rank relevancy of links.
5. Returns a ranked list of links with summaries.
6. Handles errors gracefully, respects robots.txt, and uses polite crawling.
7. Supports async requests for performance.
8. Saves output in JSON, CSV, or database.
9. Optional web dashboard with clickable links.

## Requirements
- Python 3.10+
- Libraries: requests, httpx, BeautifulSoup4, openai, serpapi, flask, streamlit

## Setup

1. Clone the repo:

   ```bash
   git clone <repo_url>
   cd QueryNova
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv; .\\venv\\Scripts\\Activate.ps1
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the `config/` directory with:

   ```env
   SERPAPI_API_KEY=your_serpapi_key
   OPENAI_API_KEY=your_openai_key
   ```

## Usage

### CLI

```bash
cd src
python main.py --query "AI in healthcare"
```

### Flask Web App

```powershell
cd src
$Env:FLASK_APP="app_flask.py"
flask run
```

### Streamlit

```bash
cd src
streamlit run app_streamlit.py
```

## Testing

```bash
pytest
```

## Docker

```bash
docker build -t querynova .
```
