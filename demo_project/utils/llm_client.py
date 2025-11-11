"""
LLM Client for Azure OpenAI Integration

Simple client for Azure OpenAI API calls with structured output support.
"""

import os
from typing import Optional, Type, TypeVar
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage



DIRECT_ENV_PATH = "/home/shubham/training/demo_project/.env"
load_dotenv(dotenv_path=DIRECT_ENV_PATH, override=True)


T = TypeVar('T', bound=BaseModel)


class LLMClient:
    """
    Simple LLM client with Azure OpenAI integration
    """
    
    def __init__(self):
        """Initialize Azure OpenAI client"""
        
        self.llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            temperature=0.7,
            max_tokens=2000
        )
    
    def generate_response(
        self, 
        system_prompt: str, 
        user_prompt: str,
        agent_name: str = None,
        topic: str = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate LLM response using Azure OpenAI
        
        Args:
            system_prompt: System message defining agent behavior
            user_prompt: User message with the task
            agent_name: Name of the agent (for logging, optional)
            topic: Content topic (for logging, optional)
            temperature: Optional temperature override
            
        Returns:
            Generated response text
        """
        if temperature is not None:
            self.llm.temperature = temperature
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: Type[T],
        agent_name: str = None,
        topic: str = None,
        temperature: Optional[float] = None
    ) -> T:
        """
        Generate structured LLM response using Pydantic models
        
        Args:
            system_prompt: System message defining agent behavior
            user_prompt: User message with the task
            response_model: Pydantic model for structured output
            agent_name: Name of the agent (for logging, optional)
            topic: Content topic (for logging, optional)
            temperature: Optional temperature override
            
        Returns:
            Structured response matching response_model
        """
        if temperature is not None:
            self.llm.temperature = temperature
        
        structured_llm = self.llm.with_structured_output(response_model)
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        response = structured_llm.invoke(messages)
        return response
        


# Global LLM client instance
_llm_client = None

def get_llm_client() -> LLMClient:
    """Get the global LLM client instance"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client


if __name__ == "__main__":
    # Test the LLM client
    print("🧪 Testing LLM Client...")
    
    client = get_llm_client()
    print("✅ LLM client initialized")
    
    # Test a simple call
    response = client.generate_response(
        "You are a helpful assistant.",
        "Say hello in exactly 5 words.",
        "test",
        "test topic"
    )
    
    print(f"✅ LLM response: {response}")
    print("✅ LLM connection successful!")
    
   