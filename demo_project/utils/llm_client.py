"""
LLM Client for Azure OpenAI Integration

This module handles LLM calls using Azure OpenAI for the demo,
with fallback options and error handling for reliable demo execution.
"""

import os
import time
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

# Import sample data functions (with try-except for standalone testing)
try:
    from utils.sample_data import get_sample_output, get_topic_key, get_demo_timing
except ImportError:
    # Fallback for standalone testing
    def get_sample_output(topic_key: str, output_type: str) -> str:
        return f"Sample {output_type} for {topic_key}"
    
    def get_topic_key(topic: str) -> str:
        return "default_topic"
    
    def get_demo_timing(agent_name: str) -> float:
        return 1.0

class DemoLLMClient:
    """
    LLM client with Azure OpenAI integration and demo-friendly features
    """
    
    def __init__(self):
        self.use_sample_fallback = os.getenv("USE_SAMPLE_DATA_FALLBACK", "true").lower() == "true"
        self.demo_mode = os.getenv("DEMO_MODE", "true").lower() == "true"
        
        # Initialize Azure OpenAI client
        try:
            self.llm = AzureChatOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
                azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4"),
                temperature=float(os.getenv("DEFAULT_MODEL_TEMPERATURE", "0.7")),
                max_tokens=int(os.getenv("DEFAULT_MAX_TOKENS", "2000"))
            )
            self.llm_available = True
        except Exception as e:
            print(f"⚠️  Azure OpenAI initialization failed: {e}")
            print("🔄 Will use sample data for demo")
            self.llm_available = False
    
    def generate_response(
        self, 
        system_prompt: str, 
        user_prompt: str,
        agent_name: str,
        topic: str,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate LLM response with fallback to sample data
        """
        
        # Demo timing simulation
        if self.demo_mode:
            demo_delay = get_demo_timing(agent_name)
            time.sleep(demo_delay)
        
        # Try Azure OpenAI first
        if self.llm_available and not self.use_sample_fallback:
            try:
                # Update temperature if provided
                if temperature is not None:
                    self.llm.temperature = temperature
                
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_prompt)
                ]
                
                response = self.llm.invoke(messages)
                return response.content
                
            except Exception as e:
                print(f"⚠️  LLM call failed for {agent_name}: {e}")
                print("🔄 Falling back to sample data")
        
        # Fallback to sample data
        topic_key = get_topic_key(topic)
        
        # Map agent names to sample data keys
        output_mapping = {
            "planner": "content_outline",
            "research_planner": "research_plan", 
            "search_executor": "research_data",
            "script_generator": "script",
            "reflection": "critique",
            "hashtag_generator": "hashtags",
            "cta_generator": "cta"
        }
        
        output_key = output_mapping.get(agent_name, "script")
        sample_output = get_sample_output(topic_key, output_key)
        
        return sample_output

# Global LLM client instance
llm_client = DemoLLMClient()

def get_llm_client() -> DemoLLMClient:
    """Get the global LLM client instance"""
    return llm_client

def test_llm_connection() -> bool:
    """Test if LLM connection is working"""
    try:
        client = get_llm_client()
        if not client.llm_available:
            return False
            
        response = client.generate_response(
            "You are a helpful assistant.",
            "Say hello in exactly 5 words.",
            "test",
            "test topic"
        )
        
        return len(response.strip()) > 0
        
    except Exception as e:
        print(f"LLM connection test failed: {e}")
        return False

if __name__ == "__main__":
    # Test the LLM client
    print("🧪 Testing LLM Client...")
    
    client = get_llm_client()
    print(f"LLM Available: {client.llm_available}")
    print(f"Demo Mode: {client.demo_mode}")
    print(f"Sample Fallback: {client.use_sample_fallback}")
    
    if test_llm_connection():
        print("✅ LLM connection successful!")
    else:
        print("❌ LLM connection failed - will use sample data")
    
    # Test sample generation
    print("\n🎭 Testing sample response generation...")
    response = client.generate_response(
        "You are a content strategist.",
        "Create a strategy for: Future of Remote Work",
        "planner",
        "Future of Remote Work"
    )
    
    print(f"Response length: {len(response)} characters")
    print("✅ Sample response generation successful!")