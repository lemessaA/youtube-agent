from abc import ABC, abstractmethod
from typing import Optional
import logging
from groq import Groq
import os

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self, model_name: str = None):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = model_name or os.getenv("GROQ_MODEL", "llama3-8b-8192")
        self.temperature = float(os.getenv("GROQ_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("GROQ_MAX_TOKENS", "1024"))
        
        if not self.api_key:
            logger.warning("GROQ_API_KEY not found in environment variables")
            self.client = None
        else:
            try:
                self.client = Groq(api_key=self.api_key)
                # Test connection
                test_response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=10,
                    temperature=0.1
                )
                logger.info(f"Connected to Groq with model: {self.model_name}")
            except Exception as e:
                logger.warning(f"Failed to connect to Groq: {e}")
                self.client = None
        
        self.system_prompt = ""
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        pass
    
    def invoke_llm(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.client:
            return "LLM not available. Please configure GROQ_API_KEY and check your connection."
        
        try:
            messages = [
                {"role": "system", "content": system_prompt or self.get_system_prompt()},
                {"role": "user", "content": prompt}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling Groq API: {e}")
            return f"Error: {e}"