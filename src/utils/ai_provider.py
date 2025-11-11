"""
AI Provider abstraction layer - supports OpenAI and Google Gemini.
Automatically selects the best available provider based on configured API keys.
"""
from __future__ import annotations

from typing import List, Optional, Dict, Any
from src.utils.secrets import get_secret
from src.utils.logger import logger


class AIProvider:
    """Unified interface for AI providers (OpenAI, Gemini)."""
    
    def __init__(self):
        self.provider = None
        self.client = None
        self._initialize()
    
    def _initialize(self):
        """Initialize the best available AI provider."""
        # Try Gemini first (free tier is generous)
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
        
        # Fallback to OpenAI
        openai_key = get_secret("OPENAI_API_KEY")
        if openai_key:
            try:
                import openai
                self.client = openai.OpenAI(api_key=openai_key)
                self.provider = "openai"
                logger.info("Using OpenAI AI provider")
                return
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI: {e}")
        
        logger.warning("No AI provider configured. AI features will be limited.")
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Get text embedding from the configured provider."""
        if not self.client:
            return None
        
        try:
            if self.provider == "gemini":
                # Gemini embeddings
                result = self.client.embed_content(
                    model="models/embedding-001",
                    content=text,
                    task_type="retrieval_document"
                )
                return result['embedding']
            
            elif self.provider == "openai":
                # OpenAI embeddings
                response = self.client.embeddings.create(
                    input=text,
                    model="text-embedding-3-small"
                )
                return response.data[0].embedding
        
        except Exception as e:
            logger.error(f"Embedding failed with {self.provider}: {e}")
            return None
    
    def generate_text(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 400,
        temperature: float = 0.7
    ) -> Optional[str]:
        """Generate text completion from the configured provider."""
        if not self.client:
            return None
        
        try:
            if self.provider == "gemini":
                # Gemini text generation
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
            
            elif self.provider == "openai":
                # OpenAI chat completion
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Text generation failed with {self.provider}: {e}")
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
