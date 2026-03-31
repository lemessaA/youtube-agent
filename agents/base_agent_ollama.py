from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, SystemMessage
import os

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self, model_name: str = None):
        # Get Ollama configuration from environment
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model_name = model_name or os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        self.temperature = float(os.getenv("OLLAMA_TEMPERATURE", "0.7"))
        
        # Initialize Ollama LLM
        self.llm = Ollama(
            model=self.model_name,
            base_url=self.base_url,
            temperature=self.temperature
        )
        
        # Test connection
        try:
            self.llm.invoke("test")
            logger.info(f"Connected to Ollama with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            raise ConnectionError(f"Cannot connect to Ollama at {self.base_url}. Make sure Ollama is running and the model is pulled.")
        
        self.system_prompt = ""
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        pass
    
    def invoke_llm(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        try:
            messages = [
                SystemMessage(content=system_prompt or self.get_system_prompt()),
                HumanMessage(content=prompt)
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error invoking LLM: {e}")
            raise
    
    def parse_response(self, response: str) -> Dict[str, Any]:
        try:
            import json
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].strip()
            else:
                json_str = response.strip()
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            return {"raw_response": response}
    
    def check_ollama_connection(self) -> bool:
        """Check if Ollama is accessible"""
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama connection check failed: {e}")
            return False
    
    def list_available_models(self) -> List[str]:
        """List available models in Ollama"""
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model["name"] for model in models]
            return []
        except Exception as e:
            logger.error(f"Failed to list Ollama models: {e}")
            return []
    
    def pull_model(self, model_name: str) -> bool:
        """Pull a model from Ollama"""
        try:
            import requests
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                timeout=300  # 5 minutes timeout for pulling
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to pull model {model_name}: {e}")
            return False
