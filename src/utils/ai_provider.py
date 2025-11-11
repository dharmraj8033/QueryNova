"""
AI Provider - Google Gemini Integration
Provides unified interface for Gemini AI (embeddings and text generation).
"""
from __future__ import annotations

from typing import List, Optional, Dict, Any
from src.utils.secrets import get_secret
from src.utils.logger import logger


class AIProvider:
    """Google Gemini AI provider for embeddings and text generation."""
    
    def __init__(self):
        self.provider = None
        self.client = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Google Gemini AI provider."""
        gemini_key = get_secret("GEMINI_API_KEY") or get_secret("GOOGLE_API_KEY")
        if gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                self.client = genai
                self.provider = "gemini"
                logger.info("Using Google Gemini AI provider")
                return
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini: {e}")
        
        logger.warning("No Gemini API key configured. AI features will be limited.")
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Get text embedding from Gemini."""
        if not self.client:
            return None
        
        try:
            result = self.client.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        
        except Exception as e:
            logger.error(f"Embedding failed with Gemini: {e}")
            return None
    
    def generate_text(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 400,
        temperature: float = 0.7
    ) -> Optional[str]:
        """Generate text completion using Gemini."""
        if not self.client:
            return None
        
        try:
            model = self.client.GenerativeModel('gemini-pro')
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = model.generate_content(
                full_prompt,
                generation_config={
                    'temperature': temperature,
                    'max_output_tokens': max_tokens,
                }
            )
            return response.text
        
        except Exception as e:
            logger.error(f"Text generation failed with Gemini: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if any AI provider is available."""
        return self.client is not None
    
    def get_provider_name(self) -> str:
        """Get the name of the current provider."""
        return self.provider or "none"


# Global singleton instance
_ai_provider = None


def get_ai_provider() -> AIProvider:
    """Get the global AI provider instance."""
    global _ai_provider
    if _ai_provider is None:
        _ai_provider = AIProvider()
    return _ai_provider
