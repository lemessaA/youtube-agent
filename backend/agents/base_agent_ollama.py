from abc import ABC, abstractmethod
from typing import Optional
import logging
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, SystemMessage
import os

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self, model_name: str = None):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model_name = model_name or os.getenv("OLLAMA_MODEL", "kimi-k2.5:cloud")
        self.temperature = float(os.getenv("OLLAMA_TEMPERATURE", "0.7"))
        self.llm = Ollama(model=self.model_name, base_url=self.base_url, temperature=self.temperature)
        try:
            self.llm.invoke("test")
            logger.info(f"Connected to Ollama with model: {self.model_name}")
        except Exception as e:
            logger.warning(f"Failed to connect to Ollama: {e}")
            self.llm = None
        self.system_prompt = ""
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        pass
    
    def invoke_llm(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.llm:
            return "LLM not available. Please configure Ollama and pull the required model."
        try:
            messages = [SystemMessage(content=system_prompt or self.get_system_prompt()), HumanMessage(content=prompt)]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Error: {e}"
