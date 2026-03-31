from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self, model_name: str = "gpt-4"):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
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
