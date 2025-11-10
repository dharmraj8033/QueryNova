import os
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

# Try to load from Streamlit secrets if available (for Streamlit Cloud deployment)
try:
    import streamlit as st
    SERPAPI_API_KEY = st.secrets.get('SERPAPI_API_KEY', os.getenv('SERPAPI_API_KEY'))
    OPENAI_API_KEY = st.secrets.get('OPENAI_API_KEY', os.getenv('OPENAI_API_KEY'))
except (ImportError, FileNotFoundError, KeyError):
    # Fallback to environment variables if Streamlit is not available or secrets not configured
    SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Only raise errors if keys are truly missing (not placeholder values)
if not SERPAPI_API_KEY or SERPAPI_API_KEY == 'your_serpapi_key_here':
    print("Warning: SERPAPI_API_KEY not properly configured")
    
if not OPENAI_API_KEY or OPENAI_API_KEY == 'sk-your_openai_key_here':
    print("Warning: OPENAI_API_KEY not properly configured")
