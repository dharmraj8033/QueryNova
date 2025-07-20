import os
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

# API keys
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not SERPAPI_API_KEY:
    raise ValueError("SERPAPI_API_KEY not set in environment")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in environment")
