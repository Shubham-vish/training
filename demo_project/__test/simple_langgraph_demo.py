"""
Simple LangChain Demo - Sequential Workflow

Demonstrates a basic LangChain workflow with two steps:
1. Step 1: Analyze a topic
2. Step 2: Write content based on analysis
"""

import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
DIRECT_ENV_PATH = "/home/shubham/training/demo_project/.env"
load_dotenv(dotenv_path=DIRECT_ENV_PATH, override=True)


# Initialize LLM
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    temperature=0.7,
    max_tokens=500
)


def step1_analyze_topic(topic: str) -> str:
    """
    Step 1: Analyzes the topic and provides key points
    """
    print(f"\n🔍 Step 1: Analyzing topic '{topic}'...")
    
    messages = [
        SystemMessage(content="You are an expert analyst. Provide 3 key points about the given topic."),
        HumanMessage(content=f"Analyze this topic: {topic}")
    ]
    
    response = llm.invoke(messages)
    analysis = response.content
    
    print(f"✅ Analysis complete!")
    print(f"📊 Analysis:\n{analysis}\n")
    
    return analysis


def step2_write_content(topic: str, analysis: str) -> str:
    """
    Step 2: Writes a short paragraph based on the analysis
    """
    print(f"\n✍️  Step 2: Writing content based on analysis...")
    
    messages = [
        SystemMessage(content="You are a skilled writer. Write a short, engaging paragraph (3-4 sentences) based on the analysis provided."),
        HumanMessage(content=f"Topic: {topic}\n\nAnalysis: {analysis}\n\nWrite a short paragraph:")
    ]
    
    response = llm.invoke(messages)
    content = response.content
    
    print(f"✅ Content written!")
    print(f"📝 Content:\n{content}\n")
    
    return content


# Main execution
if __name__ == "__main__":
    print("=" * 70)
    print("🚀 SIMPLE LANGCHAIN DEMO - SEQUENTIAL WORKFLOW")
    print("=" * 70)
    
    # Define topic
    topic = "Artificial Intelligence"
    
    print(f"\n📌 Starting workflow with topic: '{topic}'")
    print("-" * 70)
    
    # Execute Step 1: Analyze
    analysis = step1_analyze_topic(topic)
    
    # Execute Step 2: Write
    content = step2_write_content(topic, analysis)
    
    # Display final results
    print("\n" + "=" * 70)
    print("🎉 WORKFLOW COMPLETE - FINAL RESULTS")
    print("=" * 70)
    print(f"\n📌 Topic: {topic}")
    print(f"\n📊 Analysis:\n{analysis}")
    print(f"\n📝 Final Content:\n{content}")
    print("\n" + "=" * 70)
