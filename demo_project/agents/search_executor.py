"""
Search Executor Agent - Information Gathering Analyst
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from workflow.state_schema import ContentCreationState
from agents.agent_prompts import get_agent_system_prompt
from utils.display import demo_print, agent_thinking, agent_output
from utils.llm_client import get_llm_client
from rich.console import Console
from rich.panel import Panel

console = Console()


class ResearchFindings(BaseModel):
    """Structured output for research findings"""
    key_insights: List[str] = Field(description="5 key insights summary")
    research_summary: str = Field(description="Comprehensive research findings with statistics, trends, and challenges")


def _display_insights(insights: List[str], execution_time: float):
    """Display key insights in a styled panel"""
    agent_output(f"✅ Research data collected and analyzed")
    demo_print(f"   Insights: {len(insights)} key findings identified", "green")
    
    insights_text = "\n".join([f"• {insight}" for insight in insights])
    panel = Panel(
        insights_text,
        title="[bold yellow]💡 Key Insights[/bold yellow]",
        border_style="yellow",
        padding=(1, 2)
    )
    console.print(panel)
    demo_print(f"   Execution time: {execution_time:.2f}s", "cyan")


def search_executor_node(state: ContentCreationState) -> Dict[str, Any]:
    """
    Information Gathering Analyst Agent - Node 3
    
    Collects, analyzes, and synthesizes relevant information from various sources.
    """
    start_time = time.time()
    llm_client = get_llm_client()
    
    demo_print(f"🎭 Search Executor is working...", "blue")
    agent_thinking("Collecting and analyzing information from multiple sources...")
    
    system_prompt = get_agent_system_prompt("search_executor")
    user_prompt = f"""
Execute research plan and gather comprehensive information:

Topic: {state.topic}
Research Queries: {', '.join(state.research_queries)}

Provide:
1. Research summary with statistics, expert insights, trends, and challenges
2. 5 key insights that will be used for content creation"""
    
    findings = llm_client.generate_structured(
        system_prompt,
        user_prompt,
        ResearchFindings,
        "search_executor",
        state.topic,
        temperature=0.5
    )
    
    execution_time = time.time() - start_time
    
    updates = {
        "research_data": findings.research_summary,
        "key_insights": findings.key_insights,
        "current_step": "research_complete"
    }
    
    state.add_agent_execution("search_executor", "Search Executor", updates, execution_time)
    
    _display_insights(findings.key_insights, execution_time)
    
    return updates


if __name__ == "__main__":
    """Test this node independently"""
    from workflow.state_schema import ContentCreationState
    
    print("\n" + "="*70)
    print("🧪 TESTING SEARCH EXECUTOR NODE")
    print("="*70 + "\n")
    
    # Create test state
    state = ContentCreationState(
        topic="Cybersecurity",
        style="Informative and urgent",
    )
    
    state.research_queries = [
        "Latest cybersecurity threats 2025",
        "Cybersecurity market statistics",
        "Data breach cost analysis",
        "Zero trust security implementation",
        "AI in cybersecurity trends"
    ]
    
    # Execute node
    print("▶️  Executing search_executor_node...\n")
    result = search_executor_node(state)
    
    # Apply updates
    for key, value in result.items():
        setattr(state, key, value)
    
    # Display result
    print("\n" + "="*70)
    print("📊 KEY INSIGHTS")
    print("="*70)
    for i, insight in enumerate(state.key_insights, 1):
        print(f"{i}. {insight}")
    print("\n" + "="*70)
    print("📄 RESEARCH SUMMARY")
    print("="*70)
    print(state.research_data[:500] + "..." if len(state.research_data) > 500 else state.research_data)
    print("="*70)
    print(f"✅ Success! Gathered {len(state.key_insights)} key insights")
    print("="*70 + "\n")
