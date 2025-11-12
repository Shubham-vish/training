"""
Research Planner Agent - Research Strategy Specialist
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


class ResearchPlan(BaseModel):
    """Structured output for research planning"""
    research_objectives: List[str] = Field(description="3-5 key research objectives")
    research_queries: List[str] = Field(description="5 specific actionable research queries")
    information_sources: List[str] = Field(description="Target information sources")
    key_areas: List[str] = Field(description="Key research areas to investigate")


def _display_research_queries(queries: List[str], execution_time: float):
    """Display research queries in a styled panel"""
    agent_output(f"✅ Research strategy developed")
    demo_print(f"   Queries: {len(queries)} targeted searches planned", "green")
    
    queries_text = "\n".join([f"{i}. {query}" for i, query in enumerate(queries, 1)])
    panel = Panel(
        queries_text,
        title="[bold cyan]Research Queries[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(panel)
    demo_print(f"   Execution time: {execution_time:.2f}s", "cyan")


def research_planner_node(state: ContentCreationState) -> Dict[str, Any]:
    """
    Research Strategy Specialist Agent - Node 2
    
    Designs targeted research approaches and identifies key information needs.
    """
    start_time = time.time()
    llm_client = get_llm_client()
    
    demo_print(f"🎭 Research Planner is working...", "blue")
    agent_thinking("Developing research strategy and identifying information needs...")
    
    # Get research plan with structured output
    system_prompt = get_agent_system_prompt("research_planner")
    user_prompt = f"""
Create comprehensive research strategy for:

Topic: {state.topic}
Content Outline: {state.content_outline}

Provide: 3-5 objectives, 5 specific queries, information sources, and key areas."""
    
    plan = llm_client.generate_structured(
        system_prompt,
        user_prompt,
        ResearchPlan,
        "research_planner",
        state.topic,
        temperature=0.6
    )
    
    execution_time = time.time() - start_time
    
    updates = {
        "research_plan": f"Objectives: {', '.join(plan.research_objectives[:3])}",
        "research_queries": plan.research_queries,
        "current_step": "research_planning_complete"
    }
    
    state.add_agent_execution("research_planner", "Research Planner", updates, execution_time)
    
    _display_research_queries(plan.research_queries, execution_time)
    
    return updates


if __name__ == "__main__":
    """Test this node independently"""
    from workflow.state_schema import ContentCreationState
    
    print("\n" + "="*70)
    print("🧪 TESTING RESEARCH PLANNER NODE")
    print("="*70 + "\n")
    
    # Create test state
    state = ContentCreationState(
        topic="Quantum Computing",
        style="Technical but accessible",
    )
    
    state.content_outline = """
    Goal: Explain quantum computing fundamentals
    Structure: Introduction → Key Concepts → Applications → Future
    """
    
    # Execute node
    print("▶️  Executing research_planner_node...\n")
    result = research_planner_node(state)
    
    # Apply updates
    for key, value in result.items():
        setattr(state, key, value)
    
    # Display result
    print("\n" + "="*70)
    print("📋 RESEARCH QUERIES")
    print("="*70)
    queries_text= "\n"
    for i, query in enumerate(state.research_queries, 1):
        print(f"{i}. {query}")
        queries_text+= f"{query}\n"
    print("="*70)
    print(f"✅ Success! Generated {len(state.research_queries)} research queries")
    print("="*70 + "\n")
    console.print(Panel(
        queries_text, 
        title="[bold cyan]🔍 Research Queries[/bold cyan]", 
        border_style="cyan",
        padding=(1, 2),
        style="cyan"
    ))
    
