"""
Planner Agent - Content Strategy Specialist
"""

import time
from typing import Dict, Any
from workflow.state_schema import ContentCreationState
from agents.agent_prompts import get_agent_system_prompt
from utils.display import demo_print, agent_thinking, agent_output
from utils.llm_client import get_llm_client
from rich.console import Console
from rich.panel import Panel

console = Console()


def _display_strategy_summary(execution_time: float, topic: str, content_outline: str):
    """Display strategy summary with content outline"""
    agent_output(f"✅ Content strategy created for '{topic}'")
    demo_print(f"   Strategy and outline generated", "green")
    
    # Display content outline in a panel
    panel = Panel(
        content_outline,
        title="[bold green]📋 Content Strategy & Outline[/bold green]",
        border_style="green",
        padding=(1, 2)
    )
    console.print(panel)
    demo_print(f"   Execution time: {execution_time:.2f}s", "cyan")


def planner_node(state: ContentCreationState) -> Dict[str, Any]:
    """
    Content Strategy Planner Agent - Node 1
    
    Creates comprehensive content strategy and detailed outline based on the topic.
    """
    start_time = time.time()
    llm_client = get_llm_client()
    
    demo_print(f"🎭 Planner is working...", "blue")
    agent_thinking("Analyzing topic and developing content strategy...")
    
    system_prompt = get_agent_system_prompt("planner")
    user_prompt = f"""
Create comprehensive content strategy for: 
- "{state.topic}"

Requirements:
- Style: {state.style}

Provide detailed outline with goals, structure, tone guidelines, and success metrics."""
    
    content_outline = llm_client.generate_response(
        system_prompt,
        user_prompt,
        "planner",
        state.topic,
        temperature=0.7
    )
    
    execution_time = time.time() - start_time
    
    updates = {
        "content_outline": content_outline,
        "current_step": "content_planning_complete"
    }
    
    state.add_agent_execution("planner", "Planner", updates, execution_time)
    
    _display_strategy_summary(execution_time, state.topic, content_outline)
    
    return updates


if __name__ == "__main__":
    """Test this node independently"""
    from workflow.state_schema import ContentCreationState
    
    print("\n" + "="*70)
    print("🧪 TESTING PLANNER NODE")
    print("="*70 + "\n")
    
    # Create test state
    state = ContentCreationState(
        topic="Machine Learning in Healthcare",
        style="Educational and inspiring"
    )
    
    # Execute node
    print("▶️  Executing planner_node...\n")
    result = planner_node(state)
    
    # Apply updates
    for key, value in result.items():
        setattr(state, key, value)
    
    # Display result
    print("\n" + "="*70)
    print("📋 CONTENT STRATEGY & OUTLINE")
    print("="*70)
    print(state.content_outline)
    print("="*70)
    print(f"✅ Success! Strategy created for '{state.topic}'")
    print("="*70 + "\n")
